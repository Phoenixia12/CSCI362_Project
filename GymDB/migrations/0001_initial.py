# Generated by Django 5.0.9 on 2024-10-22 20:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gym',
            fields=[
                ('gym_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='Unknown Gym', max_length=255)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('permission_id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=255)),
                ('can_view_schedule', models.BooleanField(default=False)),
                ('can_edit_schedule', models.BooleanField(default=False)),
                ('can_reset_pswds', models.BooleanField(default=False)),
                ('can_create_e_account', models.BooleanField(default=False)),
                ('can_edit_e_account', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GymGoer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_date', models.DateField(auto_now_add=True, null=True)),
                ('gym', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goers', to='GymDB.gym')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Gym Goer',
                'verbose_name_plural': 'Gym Goers',
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('owner_id', models.AutoField(primary_key=True, serialize=False)),
                ('gym', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owners', to='GymDB.gym')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='gym',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gyms', to='GymDB.owner'),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('salary', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to=settings.AUTH_USER_MODEL)),
                ('gym', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='GymDB.gym')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='GymDB.owner')),
                ('roles', models.ManyToManyField(blank=True, to='GymDB.permissions')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=128, unique=True)),
                ('account', models.CharField(choices=[('JA', 'Janitorial'), ('RE', 'Receptionist'), ('TR', 'Trainer')], default='JA', max_length=2)),
            ],
            options={
                'indexes': [models.Index(fields=['email'], name='GymDB_staff_email_0ba400_idx')],
            },
        ),
        migrations.CreateModel(
            name='Pass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashed_password', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='password', to='GymDB.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('instructor_id', models.AutoField(primary_key=True, serialize=False)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('gym', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instructors', to='GymDB.gym')),
                ('roles', models.ManyToManyField(to='GymDB.permissions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructors', to='GymDB.staff')),
            ],
        ),
        migrations.CreateModel(
            name='ClassEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_events', to='GymDB.staff')),
            ],
            options={
                'ordering': ['start_time'],
            },
        ),
    ]
