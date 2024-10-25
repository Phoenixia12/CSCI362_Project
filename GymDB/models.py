from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password


class Permissions(models.Model):
    permission_id = models.AutoField(primary_key=True)  # Use AutoField for permissions
    role = models.CharField(max_length=255)  # String roles for flexibility
    can_view_schedule = models.BooleanField(default=False)
    can_edit_schedule = models.BooleanField(default=False)
    can_reset_pswds = models.BooleanField(default=False)
    can_create_e_account = models.BooleanField(default=False)
    can_edit_e_account = models.BooleanField(default=False)

    def __str__(self):
        return self.role


# Optimized Gym model
class Gym(models.Model):
    gym_id = models.AutoField(primary_key=True)  # Use AutoField for gym ID
    name = models.CharField(max_length=255, default="Unknown Gym")
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE, related_name="gyms",null = True)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


# Optimized Instructor model
class Instructor(models.Model):
    instructor_id = models.AutoField(primary_key=True)  # Use AutoField for instructor ID
    user = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='instructors')
    roles = models.ManyToManyField(Permissions)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='instructors', null=True)

    def __str__(self):
        return f"Instructor {self.instructor_id}"


# Use Django's User model for gym goers
class GymGoer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='goers', null=True)
    membership_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.gym.name}"

    class Meta:
        verbose_name = "Gym Goer"
        verbose_name_plural = "Gym Goers"


class Staff(models.Model):
    class Position(models.TextChoices):
        JANITORIAL = 'JA', ('Janitorial')
        RECEPTION = 'RE', ('Receptionist')
        TRAINER = 'TR', ('Trainer')

    user_id = models.AutoField(primary_key=True)  # Use AutoField for staff ID
    username = models.CharField(max_length=128)
    email = models.EmailField(max_length=128, unique=True)
    account = models.CharField(
        max_length=2,
        choices=Position.choices,
        default=Position.JANITORIAL
    )

    def __str__(self):
        return self.username

    class Meta:
        indexes = [models.Index(fields=['email'])]


# Centralized Password Model using Django’s built-in password hashing
class Pass(models.Model):
    user = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='password')
    hashed_password = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.hashed_password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.hashed_password)


class ClassEvent(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='class_events')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['start_time']


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)  # Use AutoField for employee ID
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employees')  # Changed to User
    roles = models.ManyToManyField(Permissions, blank=True)  # Use blank=True for optional roles
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE, related_name='employees', null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Allow null or blank
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='employees', null=True)

    def __str__(self):
        return f"Employee {self.employee_id} - {self.user.username}"

    def save(self, *args, **kwargs):
        # Set the default role or any other logic before saving
        super().save(*args, **kwargs)  # Save the instance first
        # You can handle roles or other logic here if needed


class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)  # AutoField for owner ID
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='owners', null=True)

    def __str__(self):
        return f"Owner {self.owner_id}"
