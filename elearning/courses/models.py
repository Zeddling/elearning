from django.db import models
import uuid


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256, unique=True, default='')
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class Unit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(to=Course, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, unique=True, default='')
    description = models.TextField()

    def __str__(self) -> str:
        return self.title

