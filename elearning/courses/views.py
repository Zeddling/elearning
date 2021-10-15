from django.urls.base import reverse
from courses import models, forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView


# Create your views here.
class CourseFormView(FormView):
    form_class = forms.CourseForm
    template_name = 'courses/add_course.html'
    course_title_slug = None

    def form_valid(self, form):
        #   Get form data
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        
        #   Create course
        course = models.Course.objects.create(
            title = title,
            description = description,
        )

        #   Get slug from course
        self.course_title_slug = course.slug
        
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('course', args=[self.course_title_slug])


class LessonFormView(FormView):
    form_class = forms.LessonForm
    template_name = 'courses/add_lesson.html'
    #   URL parameter for lesson
    slug_lesson = None
    
    def form_valid(self, form):
        #   Get form data
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        
        #   Create lesson
        lesson = models.Lesson.objects.create(
            title = title,
            description = description,
            unit = models.Unit.objects.get(id=self.kwargs['id'])
        )

        #   Get slug from lesson
        self.slug_lesson = lesson.slug
        
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('lesson', args=[self.slug_lesson])


class UnitFormView(FormView):
    form_class = forms.UnitForm
    template_name = 'courses/add_unit.html'
    unit_id = None

    #   Add course field to unit on valid
    def form_valid(self, form):
        #   Get form data
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        unit = models.Unit.objects.create(
            title = title,
            description = description,
            course = models.Course.objects.get(slug=self.kwargs['course_title_slug'])
        )

        self.unit_id = unit.id
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('unit', args=[self.unit_id])
        
       
def course_page(request, course_title_slug):
    context_dict = {}
    course = models.Course.objects.get(slug=course_title_slug)
    context_dict['course'] = course
    context_dict['units'] = models.Unit.objects.filter(course=course)
    return render(request, "courses/course.html", context_dict)

def index(request):
    context_dict = {}
    context_dict["courses"] = models.Course.objects.all()
    return render(request, "courses/index.html", context_dict)

#   id refers to the unit id where the lesson belongs
def lesson_page(request, lesson_title_slug):
    context_dict = {}
    context_dict['lesson'] = models.Lesson.objects.get(slug=lesson_title_slug)
    return render(request, "courses/lesson.html", context_dict)

def unit_page(request, id):
    context_dict = {}
    unit = models.Unit.objects.get(id=id)
    context_dict['unit'] = unit
    return render(request, "courses/unit.html", context_dict)
