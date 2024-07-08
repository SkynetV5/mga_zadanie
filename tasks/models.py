from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Task(models.Model):
    STATUS_TASK = [('Nowy','Nowy'), ('W toku','W toku'), ('Rozwiazany','Rozwiazany')]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20,choices=STATUS_TASK, default='Nowy')
    assigned_user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.name