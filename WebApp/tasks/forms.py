from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UsernameField
from .models import Assignment

class NoValidationPasswordField(forms.CharField):
    """A password field that doesn't enforce any validation."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', forms.PasswordInput)
        kwargs.setdefault('strip', False)
        super().__init__(*args, **kwargs)
        self.validators = []  # Remove all validators

class UserRegistrationForm(forms.ModelForm):
    """Custom registration form with no password validation."""
    username = UsernameField(
        label='Username',
        max_length=150,
        required=True,
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        help_text="Enter a valid email address"
    )
    password1 = NoValidationPasswordField(
        label='Password',
        required=True,
    )
    password2 = NoValidationPasswordField(
        label='Confirm Password',
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        # Only check if passwords match, no other validation
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'due_date', 'description', 'assignees']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'assignees': forms.CheckboxSelectMultiple(),
        }

class AssignmentStatusForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['status']