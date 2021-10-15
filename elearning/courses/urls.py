from django.urls import path
from courses import views

urlpatterns = [
    path('', views.index, name="index"),
    path('course/add-course', views.CourseFormView.as_view(), name="add_course"),
    path('course/<slug:course_title_slug>', views.course_page, name="course"),
    path('<slug:course_title_slug>/add_unit', views.UnitFormView.as_view(), name="add_unit"),
    path('unit/<uuid:id>', views.unit_page, name="unit"),
    path('unit/<uuid:id>/add_lesson', views.LessonFormView.as_view(), name="add_lesson"),
    path('lesson/<slug:lesson_title_slug>', views.lesson_page, name="lesson")
]

