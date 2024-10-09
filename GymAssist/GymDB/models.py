from django.db import models


class permissions(models.Model):
    permission_id = models.IntegerField()
    role = models.BigIntegerField()
    can_view_schedule = models.BigIntegerField()
    can_edit_schedule = models.BigIntegerField()
    can_reset_pswds = models.BigIntegerField()
    can_create_e_account = models.BigIntegerField()
    can_edit_e_account = models.BigIntegerField()

class Gym(models.Model):
    gym_id = models.BigIntegerField()
    owner_id = models.ForeignKey('Owner', on_delete=models.CASCADE)

class Instructor(models.Model):
    instructor_id=models.IntegerField(primary_key=True)
    user_id=models.ForeignKey('Staff', on_delete=models.CASCADE)
    role = models.ManyToManyField(permissions)
    rate = models.IntegerField()
    gym_id=models.ForeignKey('Gym', on_delete=models.CASCADE)

class Pass(models.Model):
    user_id = models.BigIntegerField()
    password = models.CharField(max_length=255)

class Owner(models.Model):
    owner_id=models.BigIntegerField(primary_key=True)
    gym_id = models.ForeignKey('Gym', on_delete=models.CASCADE)
    user_id = models.ForeignKey('Pass', on_delete=models.CASCADE)

class Staff(models.Model):
    class position(models.TextChoices):
        JANITORIAL = 'JA', ('Janitorial')

    user_id = models.IntegerField()
    username = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    account = models.CharField(
        max_length = 2,
        choices = position,
        default = position.JANITORIAL
        )


class Employee(models.Model):
    employee_id = models.IntegerField()
    user_id = models.ForeignKey('Staff', on_delete=models.CASCADE)
    role = models.ManyToManyField(permissions)
    owner_id = models.ForeignKey('Owner', on_delete=models.CASCADE)
    salary = models.BigIntegerField()

#class Salary(models.Model):
    #user_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    #salary = models.FloatField()