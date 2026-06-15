from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import date



class Profile(models.Model):
    ROLE_CHOICES = (
    ('admin', 'Администратор'),
    ('manager', 'Менеджер'),
    ('senior', 'Старший инженер-программист'),
    ('junior', 'Младший программист'),
)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    STATUS_CHOICES = (
        ('Новый', 'Новый'),
        ('В работе', 'В работе'),
        ('Завершён', 'Завершён'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def clean(self):
        if self.start_date < now().date():
            raise ValidationError(
                'Дата начала не может быть меньше сегодняшней.'
            )

    def __str__(self):
        return self.title


class Task(models.Model):

    CATEGORY_CHOICES = (
        ('PHP', 'PHP'),
        ('C#', 'C#'),
        ('SQL', 'SQL'),
    )

    PRIORITY_CHOICES = (
        ('Низкая', 'Низкая'),
        ('Средняя', 'Средняя'),
        ('Высокая', 'Высокая'),
    )

    STATUS_CHOICES = (
        ('Новая', 'Новая'),
        ('В работе', 'В работе'),
        ('Завершена', 'Завершена'),
        ('Просрочена', 'Просрочена'),  
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='PHP'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Низкая'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Новая'
    )

    deadline = models.DateField()


    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    def clean(self):
        if self.deadline < now().date():
            raise ValidationError(
                'Дата дедлайна не может быть меньше сегодняшней.'
            )

    def is_overdue(self):
        if self.status == 'Завершена':
            return False
        return self.deadline < date.today()
    
    def update_overdue_status(self):
        if self.is_overdue() and self.status != 'Завершена':
            self.status = 'Просрочена'
            self.save()
            return True
        return False

    def __str__(self):
        return self.title
