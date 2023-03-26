from django.db import models
import uuid

# Create your models here.
class Upload(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4, verbose_name="Upload ID")
    file = models.FileField(upload_to="uploads/", verbose_name="File Path")
    mime = models.CharField(max_length=100, default="", verbose_name="Mime Type")
    size = models.PositiveIntegerField(default=0, verbose_name="File Size(bytes)")
    date_created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Date Created")
    date_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name="Date Modified")

    def __str__(self):
        return str(self.id)

class Team(models.Model):
    teamid = models.CharField(max_length=20, unique=True, editable=False, verbose_name="Team ID")
    name = models.CharField(max_length=100, verbose_name="Team Name")
    point = models.PositiveIntegerField(default=0, verbose_name="Team Point")
    upload = models.ForeignKey(Upload, null=True, to_field="id", on_delete=models.CASCADE, verbose_name="Upload ID")
    date_created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Date Created")
    date_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name="Date Modified")

    def save(self, *args, **kwargs):
        if not self.id:
            team_count = Team.objects.count()
            teamid = "TID" + str(team_count+1).zfill(6)
            self.teamid = teamid
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.teamid
    
class Match(models.Model):
    matchid = models.CharField(max_length=20, unique=True, editable=False, verbose_name="Match ID")
    team_1 = models.ForeignKey(Team, to_field="teamid", on_delete=models.CASCADE, related_name="matches_team_1", verbose_name="Team 1")
    team_1_score = models.PositiveIntegerField(default=0, verbose_name="Team 1 Score")
    team_2 = models.ForeignKey(Team, to_field="teamid", on_delete=models.CASCADE, related_name="matches_team_2", verbose_name="Team 2")
    team_2_score = models.PositiveIntegerField(default=0, verbose_name="Team 2 Score")
    date_created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Date Created")
    date_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name="Date Modified")

    def save(self, *args, **kwargs):
        if not self.id:
            match_count = Match.objects.count()
            matchid = "MID" + str(match_count+1).zfill(6)
            self.matchid = matchid
        super().save(*args, **kwargs)

    def __str__(self):
        return self.matchid
    
    class Meta:
        verbose_name_plural = "Matches"

class User(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4, verbose_name="User ID")
    name = models.CharField(max_length=100, null=True, verbose_name="User Name")
    email = models.EmailField(unique=True, verbose_name="User Email")
    password = models.CharField(max_length=255, verbose_name="User Password")
    date_created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Date Created")
    date_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name="Date Modified")

    def __str__(self):
        return str(self.id)