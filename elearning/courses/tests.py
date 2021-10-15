from courses import models
from django.test import TestCase
from django.urls import reverse
from django_webtest import WebTest

# Test constants
TITLE_COURSE = "Test Course"
TITLE_COURSE_SLUG = "test-course"
TITLE_LESSON = "Test Lesson"
TITLE_LESSON_SLUG = "test-lesson"
TITLE_UNIT = "Test Unit"
DESCRIPTION_COURSE = "This is a test course"
DESCRIPTION_LESSON = "This is a test lesson"
DESCRIPTION_UNIT = "This is a test unit"


class CourseModelTests(TestCase):
    def test_course_str(self):
        course = models.Course(title=TITLE_COURSE, description=DESCRIPTION_COURSE)
        self.assertEqual(str(course), TITLE_COURSE)
    
    def test_on_save_slug_set(self):
        category = models.Course.objects.create(title=TITLE_COURSE, description=DESCRIPTION_COURSE)
        self.assertEqual(category.slug, TITLE_COURSE_SLUG)


class CourseFormTests(WebTest):
    def test_course_form_vaid_on_submit_redirects_successfully(self):
        form = self.app.get(reverse('add_course')).form
        form['title'] = TITLE_COURSE
        form['description'] = DESCRIPTION_COURSE
        res = form.submit().follow()
        self.assertEqual(res.status_code, 200)


class CourseFormPageTests(TestCase):
    def test_form_page_template_used(self):
        res = self.client.get(reverse('add_course'))
        self.assertTemplateUsed(res, "courses/add_course.html")

    def test_form_rendered(self):
        res = self.client.get(reverse('add_course'))
        self.assertIn(b'label', res.content)


class CoursePageTests(TestCase):
    def setUp(self):
        self.course = models.Course.objects.create(
            title=TITLE_COURSE,
            description=DESCRIPTION_COURSE,
        )
        self.unit = models.Unit.objects.create(
            course = self.course,
            title = TITLE_UNIT,
            description = DESCRIPTION_UNIT
        )
    
    def tearDown(self) -> None:
        self.course.delete()
        self.unit.delete()
    
    def test_course_template_used(self):
        res = self.client.get(reverse("course", args=[TITLE_COURSE_SLUG]))
        self.assertTemplateUsed(res, "courses/course.html")
    
    def test_units_listed(self):
       res = self.client.get(reverse("course", args=[TITLE_COURSE_SLUG]))
       self.assertIn(bytes(TITLE_UNIT, encoding='utf8'), res.content)


class IndexPageTests(TestCase):
    def setUp(self):
        self.course = models.Course.objects.create(
            title=TITLE_COURSE,
            description=DESCRIPTION_COURSE,
        )
    
    def tearDown(self) -> None:
        self.course.delete()
    
    def test_template_index_used(self):
        res = self.client.get(reverse("index"))
        self.assertTemplateUsed(res, "courses/index.html")
    
    def test_course_rendered(self):
        res = self.client.get(reverse("index"))
        self.assertIn(bytes(TITLE_COURSE, encoding='utf8'), res.content)


class LessonModelTests(TestCase):
    def setUp(self):
        self.course = models.Course.objects.create(
            title=TITLE_COURSE,
            description=DESCRIPTION_COURSE,
        )
        self.unit = models.Unit.objects.create(
            course = self.course,
            title = TITLE_UNIT,
            description = DESCRIPTION_UNIT
        )
    
    def tearDown(self) -> None:
        self.course.delete()
        self.unit.delete()
    def test_lesson_str(self):
        lesson = models.Lesson(title=TITLE_LESSON, description=DESCRIPTION_LESSON)
        self.assertEqual(str(lesson), TITLE_LESSON)
    
    def test_slug_created_on_save(self):
        lesson = models.Lesson.objects.create(
            title=TITLE_LESSON, 
            description=DESCRIPTION_LESSON,
            unit = self.unit
        )
        self.assertEqual(lesson.slug, TITLE_LESSON_SLUG)


class LessonFormTests(WebTest):
    def setUp(self):
        self.course = models.Course.objects.create(
            title=TITLE_COURSE,
            description=DESCRIPTION_COURSE,
        )
        self.unit = models.Unit.objects.create(
            course = self.course,
            title = TITLE_UNIT,
            description = DESCRIPTION_UNIT
        )
    
    def tearDown(self) -> None:
        self.course.delete()
        self.unit.delete()
    
    def test_form_valid_submit_status_200(self):
        #   Test form submit valid
        form = self.app.get(reverse('add_lesson', args=[self.unit.id])).form
        form['title'] = TITLE_LESSON
        form['description'] = DESCRIPTION_LESSON
        res = form.submit().follow()
        self.assertEqual(res.status_code, 200)
    
    def test_form_valid_submit_unit_and_course_properly_saved(self):
        #   Save form
        form = self.app.get(reverse('add_lesson', args=[self.unit.id])).form
        form['title'] = TITLE_LESSON
        form['description'] = DESCRIPTION_LESSON
        form.submit().follow()

        #   Test lesson exists
        lesson = models.Lesson.objects.get(title=TITLE_LESSON)
        self.assertIsNotNone(lesson)

        #   Test unit set
        self.assertEqual(TITLE_LESSON, str(lesson.title))


class LessonFormPageTests(TestCase):
    def setUp(self):
        self.course = models.Course.objects.create(
            title=TITLE_COURSE,
            description=DESCRIPTION_COURSE,
        )
        self.unit = models.Unit.objects.create(
            course = self.course,
            title = TITLE_UNIT,
            description = DESCRIPTION_UNIT
        )
        self.lesson = models.Lesson.objects.create(
            title=TITLE_LESSON, 
            description=DESCRIPTION_LESSON
        )
    
    def tearDown(self) -> None:
        self.course.delete()
        self.unit.delete()
        self.lesson.delete()
    
    def test_form_page_template_used(self):
        res = self.client.get(reverse('add_lesson', args=[self.unit.id]))
        self.assertTemplateUsed(res, "courses/add_lesson.html")

    def test_form_rendered(self):
        res = self.client.get(reverse('add_lesson', args=[self.unit.id]))
        self.assertIn(b'label', res.content)


class LessonPageTests(TestCase):
    def setUp(self):
        self.course = models.Course.objects.create(
            title=TITLE_COURSE,
            description=DESCRIPTION_COURSE,
        )
        self.unit = models.Unit.objects.create(
            course = self.course,
            title = TITLE_UNIT,
            description = DESCRIPTION_UNIT
        )
        self.lesson = models.Lesson.objects.create(
            title=TITLE_LESSON, 
            description=DESCRIPTION_LESSON
        )
    
    def tearDown(self) -> None:
        self.course.delete()
        self.unit.delete()
        self.lesson.delete()
    
    def test_template_lesson_used(self):
        res = self.client.get(reverse('lesson', args=[TITLE_LESSON_SLUG]))
        self.assertTemplateUsed(res, "courses/lesson.html")
    
    def test_lesson_info_displayed(self):
        res = self.client.get(reverse('lesson', args=[TITLE_LESSON_SLUG]))
        self.assertIn(bytes(TITLE_LESSON, encoding="utf8"), res.content)


class UnitModelTests(TestCase):
    def test_unit_str(self):
        unit = models.Unit(title=TITLE_UNIT, description=DESCRIPTION_UNIT)
        self.assertEqual(str(unit), TITLE_UNIT)


class UnitFormTests(WebTest):
    def setUp(self):
        self.course = models.Course.objects.create(
            title=TITLE_COURSE,
            description=DESCRIPTION_COURSE,
        )
    
    def tearDown(self) -> None:
        self.course.delete()
    
    def test_form_valid_submit_status_200(self):
        #   Test form submit valid
        form = self.app.get(reverse('add_unit', args=[TITLE_COURSE_SLUG])).form
        form['title'] = TITLE_UNIT
        form['description'] = DESCRIPTION_UNIT
        res = form.submit().follow()
        self.assertEqual(res.status_code, 200)
    
    def test_form_valid_submit_unit_and_course_properly_saved(self):
        #   Save form
        form = self.app.get(reverse('add_unit', args=[TITLE_COURSE_SLUG])).form
        form['title'] = TITLE_UNIT
        form['description'] = DESCRIPTION_UNIT
        res = form.submit().follow()

        #   Test unit exists
        unit = models.Unit.objects.get(title=TITLE_UNIT)
        self.assertIsNotNone(unit)

        #   Test course set
        self.assertEqual(TITLE_COURSE, str(unit.course))


class UnitFormPageTests(TestCase):
    def setUp(self):
        self.course = models.Course.objects.create(
            title=TITLE_COURSE,
            description=DESCRIPTION_COURSE,
        )
    
    def tearDown(self) -> None:
        self.course.delete()
    
    def test_form_page_template_used(self):
        res = self.client.get(reverse('add_unit', args=[TITLE_COURSE_SLUG]))
        self.assertTemplateUsed(res, "courses/add_unit.html")

    def test_form_rendered(self):
        res = self.client.get(reverse('add_unit', args=[TITLE_COURSE_SLUG]))
        self.assertIn(b'label', res.content)


class UnitPageTests(TestCase):
    def setUp(self):
        self.course = models.Course.objects.create(
            title=TITLE_COURSE,
            description=DESCRIPTION_COURSE,
        )
        self.unit = models.Unit.objects.create(
            course = self.course,
            title = TITLE_UNIT,
            description = DESCRIPTION_UNIT
        )
    
    def tearDown(self) -> None:
        self.course.delete()
        self.unit.delete()
    
    def test_unit_template_used(self):
        res = self.client.get(reverse('unit', args=[self.unit.id]))
        self.assertTemplateUsed(res, 'courses/unit.html')
    
    def test_unit_info_rendered(self):
        res = self.client.get(reverse('unit', args=[self.unit.id]))
        self.assertIn(bytes(TITLE_UNIT, encoding='utf8'), res.content)
        self.assertIn(bytes(DESCRIPTION_UNIT, encoding='utf8'), res.content)

