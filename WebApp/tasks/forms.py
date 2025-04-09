from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UsernameField
from django.forms import formset_factory, BaseFormSet
from .models import Assignment, SubTask

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

class SubTaskForm(forms.ModelForm):
    """Form for creating/editing a subtask"""
    class Meta:
        model = SubTask
        fields = ['name', 'is_completed']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mdc-text-field__input', 'placeholder': 'Enter subtask name'}),
        }

    def __init__(self, *args, **kwargs):
        # Get the is_new parameter and remove it from kwargs
        is_new = kwargs.pop('is_new', True)
        super().__init__(*args, **kwargs)

        # Store is_new as an attribute so it can be set after initialization
        self.is_new = is_new

        # If this is a new subtask (not editing), hide the completed field
        if self.is_new:
            self.fields['is_completed'].widget = forms.HiddenInput()
            self.fields['is_completed'].initial = False

class BaseSubTaskFormSet(BaseFormSet):
    """Base formset for handling multiple subtasks"""
    def clean(self):
        """Validate that there are no duplicate subtask names"""
        if any(self.errors):
            return

        names = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                name = form.cleaned_data.get('name')

                if name and name in names:
                    duplicates = True
                    form.add_error('name', 'Subtasks must have unique names')

                names.append(name)

        if duplicates:
            raise forms.ValidationError('Please fix the duplicate subtask names')

# Create a formset for subtasks
SubTaskFormSet = formset_factory(
    SubTaskForm,
    formset=BaseSubTaskFormSet,
    extra=1,
    can_delete=True
)

# Custom formset for new subtasks (without completed checkbox)
class NewSubTaskFormSet(BaseSubTaskFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pass is_new=True to each form to hide the completed checkbox
        for form in self.forms:
            form.is_new = True

# Create a formset for new subtasks
NewSubTaskFormSet = formset_factory(
    SubTaskForm,
    formset=NewSubTaskFormSet,
    extra=1,
    can_delete=True
)

class AssignmentForm(forms.ModelForm):
    """Form for creating/editing an assignment with optional advanced mode"""
    advanced_mode = forms.BooleanField(
        required=False,
        initial=False,
        label='Enable Advanced Mode',
        help_text='Add subtasks and track progress',
        widget=forms.CheckboxInput(attrs={'class': 'mdc-checkbox__native-control'})
    )

    class Meta:
        model = Assignment
        fields = ['name', 'due_date', 'description', 'status', 'assignees']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'assignees': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        # Set default status to 'Not Started' for new assignments
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        if 'status' not in kwargs.get('initial', {}):
            kwargs['initial']['status'] = 'Not Started'

        super().__init__(*args, **kwargs)
        self.subtask_formset = None

        # Hide the status field for new assignments - they always start as 'Not Started'
        if not self.instance.pk:  # This is a new assignment
            self.fields['status'].widget = forms.HiddenInput()
            self.fields['status'].initial = 'Not Started'

        # If this is an existing assignment with subtasks, enable advanced mode by default
        if self.instance.pk and hasattr(self.instance, 'subtasks') and self.instance.subtasks.exists():
            self.fields['advanced_mode'].initial = True
            # Disable status field for assignments with subtasks (status is auto-determined)
            self.fields['status'].disabled = True
            self.fields['status'].help_text = 'Status is automatically determined by subtask completion'

    def is_valid(self):
        """Override to validate both the form and formset if advanced mode is enabled"""
        valid = super().is_valid()

        if self.cleaned_data.get('advanced_mode') and self.subtask_formset:
            return valid and self.subtask_formset.is_valid()

        return valid

    def clean(self):
        """Custom clean method to ensure all required fields are present"""
        cleaned_data = super().clean()

        # Make sure due_date is present
        if 'due_date' not in cleaned_data or not cleaned_data['due_date']:
            self.add_error('due_date', 'Due date is required')

        # Make sure name is present
        if 'name' not in cleaned_data or not cleaned_data['name']:
            self.add_error('name', 'Name is required')

        # Print debug info
        print("Form data:", self.data)
        print("Cleaned data:", cleaned_data)

        return cleaned_data

    def save(self, commit=True):
        """Save the assignment and its subtasks if advanced mode is enabled"""
        assignment = super().save(commit=commit)

        # Save subtasks if advanced mode is enabled and we have a formset
        if self.cleaned_data.get('advanced_mode') and self.subtask_formset and commit:
            # Delete existing subtasks if this is an update
            if assignment.pk:
                assignment.subtasks.all().delete()

            # Save new subtasks
            for subtask_form in self.subtask_formset.forms:
                if subtask_form.cleaned_data and not subtask_form.cleaned_data.get('DELETE', False):
                    subtask = subtask_form.save(commit=False)
                    subtask.assignment = assignment
                    subtask.save()

        return assignment

class AssignmentStatusForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['status']