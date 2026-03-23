from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from attendance.services.punch_service import PunchService
from attendance.models import AttendanceRecord


User = get_user_model()


class PunchServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )

    def test_punch_in_success(self):
        record = PunchService.punch_in(self.user)

        self.assertIsNotNone(record.clock_in)
        self.assertEqual(record.user, self.user)

    def test_punch_in_duplicate(self):
        PunchService.punch_in(self.user)

        with self.assertRaises(ValueError):
            PunchService.punch_in(self.user)

    def test_punch_out_without_in(self):
        with self.assertRaises(ValueError):
            PunchService.punch_out(self.user)

    def test_punch_out_success(self):
        PunchService.punch_in(self.user)
        record = PunchService.punch_out(self.user)

        self.assertIsNotNone(record.clock_out)