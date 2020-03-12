from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from course.models import Course, CourseInstance, CourseModule, \
    LearningObjectCategory
from deviations.models import DeadlineRuleDeviation, MaxSubmissionsRuleDeviation
from exercise.exercise_models import ExerciseWithAttachment
from userprofile.models import User
from course.cache.students import CachedStudent


class DeviationsTest(TestCase):
    def setUp(self):
        self.user = User(username="testUser", first_name="First", last_name="Last")
        self.user.set_password("testPassword")
        self.user.save()

        self.course = Course.objects.create(
            name="test course",
            code="123456",
            url="Course-Url"
        )

        self.today = timezone.now()
        self.tomorrow = self.today + timedelta(days=1)
        self.two_days_from_now = self.today + timedelta(days=2)

        self.course_instance = CourseInstance.objects.create(
            instance_name="Fall 2011 day 1",
            starting_time=self.today,
            ending_time=self.tomorrow,
            course=self.course,
            url="T-00.1000_d1"
        )

        self.course_module = CourseModule.objects.create(
            name="test module",
            url="test-module",
            points_to_pass=15,
            course_instance=self.course_instance,
            opening_time=self.today,
            closing_time=self.tomorrow
        )

        self.learning_object_category = LearningObjectCategory.objects.create(
            name="test category",
            course_instance=self.course_instance,
            points_to_pass=5
        )

        self.exercise_with_attachment = ExerciseWithAttachment.objects.create(
            name="test exercise 3",
            course_module=self.course_module,
            category=self.learning_object_category,
            max_points=50,
            points_to_pass=50,
            max_submissions=0,
            files_to_submit="test1.txt|test2.txt|img.png",
            content="test_instructions"
        )

        self.deadline_rule_deviation = DeadlineRuleDeviation.objects.create(
            exercise=self.exercise_with_attachment,
            submitter=self.user.userprofile,
            extra_minutes=1440  # One day
        )
        self.max_submissions_rule_deviation = MaxSubmissionsRuleDeviation.objects.create(
            exercise=self.exercise_with_attachment,
            submitter=self.user.userprofile,
            extra_submissions=1
        )

    def test_deadline_rule_deviation_extra_time(self):
        self.assertEqual(timedelta(days=1), self.deadline_rule_deviation.get_extra_time())

    def test_deadline_rule_deviation_new_deadline(self):
        self.assertEqual(self.two_days_from_now, self.deadline_rule_deviation.get_new_deadline())

    def test_deadline_rule_deviation_normal_deadline(self):
        self.assertEqual(self.tomorrow, self.deadline_rule_deviation.get_normal_deadline())

    def test_student_cache_content(self):
        try:
            self.assertEqual(self.two_days_from_now, CachedStudent(
                    self.course_instance, self.user
                ).data['dl_deviations'][self.exercise_with_attachment.id][0])
        except KeyError:
            raise AssertionError("No deviation info in Cached Student.")

    def test_student_cache_changes(self):
        DeadlineRuleDeviation.objects.filter(submitter=self.user.userprofile).delete()
        try:
            # Cache shouldn't contain data of deviations to the student
            CachedStudent(self.course_instance, self.user
                ).data['dl_deviations'][self.exercise_with_attachment.id]
            raise AssertionError("Cache not emptied.")
        except AssertionError as e:
            raise e
        except KeyError:
            pass

    def test_max_submissions_rule_deviation_extra_time(self):
        self.assertEqual(1, self.max_submissions_rule_deviation.extra_submissions)

    def test_student_cache_content(self):
        try:
            self.assertEqual(1, CachedStudent(
                    self.course_instance, self.user
                ).data['submission_deviations'][self.exercise_with_attachment.id])
        except KeyError:
            raise AssertionError("No deviation info in Cached Student.")

    def test_student_cache_changes(self):
        MaxSubmissionsRuleDeviation.objects.filter(submitter=self.user.userprofile).delete()
        try:
            # Cache shouldn't contain data of deviations to the student
            CachedStudent(self.course_instance, self.user
                ).data['submission_deviations'][self.exercise_with_attachment.id]
            raise AssertionError("Cache not emptied.")
        except AssertionError as e:
            raise e
        except KeyError:
            pass
