from courses import models
from django import forms


class CourseForm(forms.ModelForm):

    class Meta:
        model = models.Course
        fields = ['title', 'description']


class LessonForm(forms.ModelForm):

    class Meta:
        model = models.Lesson
        fields = ['title', 'description']


class UnitForm(forms.ModelForm):

    class Meta:
        model = models.Unit
        fields = ['title', 'description']

