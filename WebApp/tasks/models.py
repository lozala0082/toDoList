from django.db import models
from django.contrib.auth.models import User

class Assignment(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    name = models.CharField(max_length=200)
    due_date = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_assignments')
    assignees = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_completion_percentage(self):
        """Calculate the percentage of completed subtasks"""
        subtasks = self.subtasks.all()
        if not subtasks.exists():
            # If no subtasks, base on assignment status
            if self.status == 'Completed':
                return 100
            elif self.status == 'In Progress':
                return 50
            else:
                return 0

        total = subtasks.count()
        completed = subtasks.filter(is_completed=True).count()
        if total == 0:
            return 0
        return int((completed / total) * 100)

    def update_status_from_subtasks(self):
        """Update the assignment status based on subtask completion"""
        subtasks = self.subtasks.all()
        if not subtasks.exists():
            # If no subtasks, don't change the status
            return

        total = subtasks.count()
        completed = subtasks.filter(is_completed=True).count()

        # Determine the new status based on completion
        if completed == 0:
            new_status = 'Not Started'
        elif completed == total:
            new_status = 'Completed'
        else:
            new_status = 'In Progress'

        # Only update if the status has changed
        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=['status'])


class SubTask(models.Model):
    """Model for subtasks within an assignment"""
    name = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='subtasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Override save to update parent assignment status"""
        super().save(*args, **kwargs)
        # Update the parent assignment's status based on subtask completion
        self.assignment.update_status_from_subtasks()