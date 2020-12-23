from django.db import models
# Create your models here.

class MemberData(models.Model):

    userid = models.CharField(
        max_length=40,
        default=""
    )
    displayname = models.CharField(
        max_length=40,
        default=""
    )
    nickname=models.CharField(
        max_length=40,
        default=""
    )


    # groupid = models.CharField(
    #     max_length=40,
    #     default=""
    # )