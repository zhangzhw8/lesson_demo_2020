from django.conf import settings
from django.db import models

# Create your models here.


class WeChatUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)
    motto = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    pic = models.CharField(max_length=60, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Status(models.Model):
    user = models.ForeignKey(WeChatUser, models.CASCADE)
    text = models.CharField(max_length=280)
    pics = models.CharField(max_length=100, null=True, blank=True)
    pub_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-id"]


class Reply(models.Model):
    status = models.ForeignKey(Status, models.CASCADE)
    author = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=[("0", "like"), ("1", "comment")])
    text = models.CharField(max_length=280, null=True, blank=True)
    at_person = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return "{} on {}".format(self.author, self.status.text)
