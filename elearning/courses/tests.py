from courses import models
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
TITLE_COURSE = "Test Course"
TITLE_UNIT = "Test Unit"
DESCRIPTION_COURSE = "This is a test course"
DESCRIPTION_UNIT = "This is a test unit"
class CourseModelTests(TestCase):
    def test_course_str(self):
        course = models.Course(title=TITLE_COURSE, description=DESCRIPTION_COURSE)
        self.assertEqual(str(course), TITLE_COURSE)


class UnitModelTests(TestCase):
    def test_unit_str(self):
        unit = models.Unit(title=TITLE_UNIT, description=DESCRIPTION_UNIT)
        self.assertEqual(str(unit), TITLE_UNIT)


class IndexPageTests(TestCase):
    def setUp(self):
        self.category = models.Course.objects.create(
            title=TITLE_COURSE,
            description=DESCRIPTION_COURSE,
        )
    
    def tearDown(self) -> None:
        self.category.delete()
    
    def test_template_index_used(self):
        res = self.client.get(reverse("index"))
        self.assertTemplateUsed(res, "courses/index.html")
    
    def test_category_rendered(self):
        res = self.client.get(reverse("index"))
        self.assertIn(bytes(TITLE_COURSE, encoding='utf8'), res.content)
