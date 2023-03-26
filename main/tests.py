from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import *

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        User.objects.create(name='Test User', email='testuser@example.com', password='password123')

    def test_user_name(self):
        user = User.objects.get(id=1)
        name_label = user._meta.get_field('name').verbose_name
        self.assertEqual(name_label, 'User Name')

    def test_user_email(self):
        user = User.objects.get(id=1)
        email_label = user._meta.get_field('email').verbose_name
        self.assertEqual(email_label, 'User Email')

    def test_user_password(self):
        user = User.objects.get(id=1)
        self.assertTrue(user.password.startswith('pbkdf2_sha256'))

    def test_date_created(self):
        user = User.objects.get(id=1)
        date_created_label = user._meta.get_field('date_created').verbose_name
        self.assertEqual(date_created_label, 'Date Created')
        self.assertLess(user.date_created, timezone.now())

    def test_date_modified(self):
        user = User.objects.get(id=1)
        date_modified_label = user._meta.get_field('date_modified').verbose_name
        self.assertEqual(date_modified_label, 'Date Modified')
        user.save()
        self.assertGreater(user.date_modified, user.date_created)

class MatchModelTestCase(TestCase):
    def setUp(self):
        self.team_1 = Team.objects.create(name='Team 1')
        self.team_2 = Team.objects.create(name='Team 2')
        self.match = Match.objects.create(team_1=self.team_1, team_2=self.team_2)

    def test_match_id_is_generated_on_create(self):
        self.assertIsNotNone(self.match.matchid)

    def test_match_teams_are_set_correctly(self):
        self.assertEqual(self.match.team_1, self.team_1)
        self.assertEqual(self.match.team_2, self.team_2)

    def test_match_string_representation(self):
        expected_str = f"{self.match.matchid}"
        self.assertEqual(str(self.match), expected_str)

class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Test Team", point=10)
        
    def test_team_creation(self):
        self.assertEqual(self.team.__str__(), self.team.teamid)
        self.assertEqual(self.team.name, "Test Team")
        self.assertEqual(self.team.point, 10)
        
    def test_team_id_generation(self):
        team_count = Team.objects.count()
        new_team = Team.objects.create(name="New Team", point=5)
        new_team_id = "TID" + str(team_count+2).zfill(6)
        self.assertEqual(new_team.teamid, new_team_id)

class UploadModelTest(TestCase):

    def setUp(self):
        self.file = SimpleUploadedFile("test_file.txt", b"file_content")
        self.upload = Upload.objects.create(file=self.file, mime="text/plain", size=11)

    def test_upload_str(self):
        self.assertEqual(str(self.upload), str(self.upload.id))

    def test_upload_fields(self):
        self.assertEqual(self.upload.mime, "text/plain")
        self.assertEqual(self.upload.size, 11)
        self.assertEqual(self.upload.file.name, "uploads/test_file.txt")