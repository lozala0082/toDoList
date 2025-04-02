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
            due_date__date=today
        ).order_by('due_date')

        context['weekly_assignments'] = base_queryset.filter(
            due_date__date__gte=week_start,
            due_date__date__lt=week_start + timedelta(days=7)
        ).order_by('due_date')

        context['monthly_assignments'] = base_queryset.filter(
            due_date__date__gte=month_start,
            due_date__date__lt=month_start + timedelta(days=32)
        ).order_by('due_date')

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
    if request.method == 'POST':
        form = AssignmentStatusForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment status updated successfully!')
            return redirect('assignment-detail', pk=pk)
    else:
        form = AssignmentStatusForm(instance=assignment)
    return render(request, 'tasks/update_status.html', {'form': form, 'assignment': assignment})

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