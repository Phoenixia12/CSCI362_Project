from django import forms
from django.db import models
from django.contrib.auth.models import User
from GymDB.models import GymGoer, Instructor, Employee, Owner, Gym, Staff, Permissions, ClassEvent
from django.contrib import messages

# User registration with role selection
class UserRoleForm(forms.Form):
    
    ROLE_CHOICES = [
        ('owner', 'Gym Owner'),
        ('employee', 'Gym Employee'),
        ('instructor', 'Instructor'),
        ('gym_goer', 'Gym Goer'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=False)

# Form for Gym Owners
class GymOwnerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Owner
        fields = []  # Fields are handled manually in the view

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Password confirmation check
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        # Create the User instance (Owner)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password=self.cleaned_data['password']
        )
        
        # Create the Owner instance and associate the User
        owner = Owner( user=user)  # Link the user to the owner
        if commit:
            owner.save()
        return user

# Form for Gym creation (used in Owner registration or management)
class GymForm(forms.ModelForm):
    class Meta:
        model = Gym
        fields = ['name', 'location']

# Form for Gym Employees
class GymEmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Employee  # Specify your Employee model here
        fields = []  # Fields are handled manually in the view

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Password confirmation check
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        # Create the User instance (Employee)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password=self.cleaned_data['password']
        )
        
        # Create the Employee instance and associate the User and gym
        employee = Employee(user=user, gym=self.cleaned_data['gym'])  # Link the user and gym to the employee
        if commit:
            employee.save()
        return employee

# Form for Instructors
class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['gym', 'roles', 'rate']  # Include gym (not gym_id) and other relevant fields

    gym = forms.ModelChoiceField(queryset=Gym.objects.all(), required=True)
    roles = forms.ModelMultipleChoiceField(queryset=Permissions.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
    
# Form for Gym Goers
class GymGoerForm(forms.ModelForm):
    class Meta:
        model = GymGoer
        # Exclude auto-populated fields
        exclude = ['membership_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
from GymDB.models import ClassEvent

class ClassEventForm(forms.ModelForm):
    class Meta:
        model = ClassEvent
        fields = ['title', 'start_time', 'end_time', 'description']