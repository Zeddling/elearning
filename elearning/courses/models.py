from django.db import models
from django.template.defaultfilters import slugify
import uuid


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256, unique=True, default='')
    description = models.TextField()
    slug = models.SlugField(unique=True, default='')

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)


class Unit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(to=Course, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, unique=True, default='')
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=256, unique=True, default='')
    description = models.TextField()
    unit = models.ForeignKey(to=Unit, null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, default='')

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Lesson, self).save(*args, **kwargs)
