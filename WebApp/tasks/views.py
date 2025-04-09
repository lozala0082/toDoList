from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
import json
from .models import Assignment, SubTask
from .forms import AssignmentForm, AssignmentStatusForm, UserRegistrationForm, SubTaskFormSet, NewSubTaskFormSet

def is_admin(user):
    return user.is_staff

class HomeView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = 'tasks/home.html'
    context_object_name = 'assignments'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_staff:
            return Assignment.objects.all()
        return Assignment.objects.filter(assignees=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)

        base_queryset = self.get_queryset()

        context['today_assignments'] = base_queryset.filter(
            due_date__year=today.year,
            due_date__month=today.month,
            due_date__day=today.day
        ).order_by('due_date')

        # Get assignments due this week, excluding today
        context['weekly_assignments'] = base_queryset.filter(
            due_date__gte=week_start,
            due_date__lt=week_start + timedelta(days=7)
        ).exclude(
            due_date__year=today.year,
            due_date__month=today.month,
            due_date__day=today.day
        ).order_by('due_date')

        # Get the IDs of assignments already shown in today and weekly sections
        # to avoid duplication in the monthly section
        today_and_weekly_ids = list(context['today_assignments'].values_list('id', flat=True)) + \
                              list(context['weekly_assignments'].values_list('id', flat=True))

        # Get all assignments for this month
        month_end = (month_start.replace(month=month_start.month % 12 + 1, day=1) if month_start.month < 12
                    else month_start.replace(year=month_start.year + 1, month=1, day=1)) - timedelta(days=1)

        context['monthly_assignments'] = base_queryset.filter(
            due_date__gte=month_start,
            due_date__lte=month_end
        ).exclude(id__in=today_and_weekly_ids).order_by('due_date')

        # Get assignments due beyond this month (future months)
        # First, collect all IDs from today, weekly, and monthly sections to avoid duplication
        all_current_ids = today_and_weekly_ids + list(context['monthly_assignments'].values_list('id', flat=True))

        # Filter assignments due after the end of the current month
        context['future_assignments'] = base_queryset.filter(
            due_date__gt=month_end
        ).exclude(id__in=all_current_ids).order_by('due_date')

        # Calculate statistics for progress indicators by status
        all_assignments = base_queryset.all()
        total_assignments = all_assignments.count()

        # Count assignments by status
        completed_assignments = all_assignments.filter(status='Completed').count()
        in_progress_assignments = all_assignments.filter(status='In Progress').count()
        not_started_assignments = all_assignments.filter(status='Not Started').count()

        # Add counts to context
        context['total_assignments'] = total_assignments
        context['completed_assignments'] = completed_assignments
        context['in_progress_assignments'] = in_progress_assignments
        context['not_started_assignments'] = not_started_assignments

        # Calculate completion percentage
        if total_assignments > 0:
            context['completion_percentage'] = int((completed_assignments / total_assignments) * 100)
        else:
            context['completion_percentage'] = 0

        # Force refresh of the context data to ensure it's up-to-date
        context['refresh_timestamp'] = timezone.now().timestamp()

        return context

class AssignmentDetailView(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = 'tasks/assignment_detail.html'
    context_object_name = 'assignment'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Assignment.objects.all()
        return Assignment.objects.filter(assignees=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add subtasks to context
        context['subtasks'] = self.object.subtasks.all().order_by('created_at')
        return context

class AssignmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'tasks/assignment_form.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['subtask_formset'] = NewSubTaskFormSet(self.request.POST, prefix='subtasks')
        else:
            context['subtask_formset'] = NewSubTaskFormSet(prefix='subtasks')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        subtask_formset = context['subtask_formset']

        # Set the creator
        form.instance.creator = self.request.user

        # For new assignments, always set status to 'Not Started'
        if not form.instance.pk:
            form.instance.status = 'Not Started'

        # Check for status_backup field (used when status field is readonly)
        status_backup = self.request.POST.get('status_backup')
        if status_backup and form.cleaned_data.get('advanced_mode'):
            form.instance.status = status_backup

        # Check if advanced mode is enabled
        if form.cleaned_data.get('advanced_mode'):
            if subtask_formset.is_valid():
                # Attach the formset to the form for saving in form.save()
                form.subtask_formset = subtask_formset

                # For advanced mode, status will be determined by subtasks
                # We'll set it initially based on whether any subtasks are marked completed
                has_completed = False
                has_subtasks = False

                for subtask_form in subtask_formset:
                    if subtask_form.cleaned_data and not subtask_form.cleaned_data.get('DELETE', False):
                        has_subtasks = True
                        if subtask_form.cleaned_data.get('is_completed', False):
                            has_completed = True

                if has_subtasks:
                    if has_completed:
                        form.instance.status = 'In Progress'
                    else:
                        form.instance.status = 'Not Started'
            else:
                return self.form_invalid(form)

        # Add a success message
        messages.success(self.request, 'Assignment created successfully!')
        print('Assignment created successfully, message added to session')

        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff

    def form_invalid(self, form):
        # Add debug information to help identify the issue
        print("Form validation errors:", form.errors)

        # If there's a subtask formset, check its errors too
        context = self.get_context_data()
        if 'subtask_formset' in context:
            subtask_formset = context['subtask_formset']
            if not subtask_formset.is_valid():
                print("Subtask formset errors:", subtask_formset.errors)

        return super().form_invalid(form)

class AssignmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'tasks/assignment_form.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['subtask_formset'] = SubTaskFormSet(self.request.POST, prefix='subtasks')
        else:
            # Pre-populate with existing subtasks
            subtask_data = [
                {'name': subtask.name, 'is_completed': subtask.is_completed}
                for subtask in self.object.subtasks.all()
            ]
            context['subtask_formset'] = SubTaskFormSet(
                initial=subtask_data,
                prefix='subtasks'
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        subtask_formset = context['subtask_formset']

        # Check if advanced mode is enabled
        if form.cleaned_data.get('advanced_mode'):
            if subtask_formset.is_valid():
                # Attach the formset to the form for saving in form.save()
                form.subtask_formset = subtask_formset
            else:
                return self.form_invalid(form)

        # Add a success message
        messages.success(self.request, 'Assignment updated successfully!')
        print('Assignment updated successfully, message added to session')

        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff

    def form_invalid(self, form):
        # Add debug information to help identify the issue
        print("Form validation errors:", form.errors)

        # If there's a subtask formset, check its errors too
        context = self.get_context_data()
        if 'subtask_formset' in context:
            subtask_formset = context['subtask_formset']
            if not subtask_formset.is_valid():
                print("Subtask formset errors:", subtask_formset.errors)

        return super().form_invalid(form)

class AssignmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Assignment
    template_name = 'tasks/assignment_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_staff

@login_required
def update_status(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    # Check if user is authorized (either staff or assignee)
    if not (request.user.is_staff or assignment.assignees.filter(id=request.user.id).exists()):
        messages.error(request, 'You are not authorized to update this assignment.')
        return redirect('assignment-detail', pk=pk)

    if request.method == 'POST':
        form = AssignmentStatusForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment status updated successfully!')
            return redirect('assignment-detail', pk=pk)
    else:
        form = AssignmentStatusForm(instance=assignment)

    # Add status choices to context
    return render(request, 'tasks/update_status.html', {
        'form': form,
        'assignment': assignment,
        'status_choices': Assignment.STATUS_CHOICES
    })

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                # Add a success message that will be displayed on the login page
                messages.success(request, 'Account created successfully! You can now log in.')
                # Print to console for debugging
                print('Registration successful, message added to session')
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Error creating account: {str(e)}")
                print(f'Registration error: {str(e)}')
    else:
        form = UserRegistrationForm()

    return render(request, 'tasks/register_form.html', {'form': form})

@login_required
def update_subtask(request, pk):
    """API endpoint to update a subtask's completion status"""
    subtask = get_object_or_404(SubTask, pk=pk)
    assignment = subtask.assignment

    # Check if user is authorized (either staff or assignee)
    if not (request.user.is_staff or assignment.assignees.filter(id=request.user.id).exists()):
        return JsonResponse({'error': 'Not authorized'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            is_completed = data.get('is_completed', False)

            # Update the subtask
            subtask.is_completed = is_completed
            subtask.save()

            # Get the updated assignment after status change
            assignment.refresh_from_db()

            # Return updated completion percentage and status
            return JsonResponse({
                'success': True,
                'is_completed': subtask.is_completed,
                'completion_percentage': assignment.get_completion_percentage(),
                'assignment_status': assignment.status
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)