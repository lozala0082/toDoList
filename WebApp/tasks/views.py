from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from .models import Assignment
from .forms import AssignmentForm, AssignmentStatusForm, UserRegistrationForm

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

        context['weekly_assignments'] = base_queryset.filter(
            due_date__gte=week_start,
            due_date__lt=week_start + timedelta(days=7)
        ).order_by('due_date')

        # Get the monthly assignments, excluding those already in today or weekly lists
        today_and_weekly_ids = list(context['today_assignments'].values_list('id', flat=True)) + \
                              list(context['weekly_assignments'].values_list('id', flat=True))

        # Get all assignments for this month
        month_end = (month_start.replace(month=month_start.month % 12 + 1, day=1) if month_start.month < 12
                    else month_start.replace(year=month_start.year + 1, month=1, day=1)) - timedelta(days=1)

        context['monthly_assignments'] = base_queryset.filter(
            due_date__gte=month_start,
            due_date__lte=month_end
        ).exclude(id__in=today_and_weekly_ids).order_by('due_date')

        # Get assignments due beyond this month
        all_current_ids = today_and_weekly_ids + list(context['monthly_assignments'].values_list('id', flat=True))

        context['future_assignments'] = base_queryset.filter(
            due_date__gt=month_end
        ).exclude(id__in=all_current_ids).order_by('due_date')

        return context

class AssignmentDetailView(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = 'tasks/assignment_detail.html'
    context_object_name = 'assignment'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Assignment.objects.all()
        return Assignment.objects.filter(assignees=self.request.user)

class AssignmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'tasks/assignment_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff

class AssignmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'tasks/assignment_form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_staff

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

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'tasks/register.html', {'form': form})