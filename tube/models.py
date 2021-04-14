from django.db import models
from django.utils import timezone

class Video(models.Model):

    class Meta:

        db_table = "video"

    title   = models.CharField(verbose_name="タイトル", max_length=30)
    comment = models.CharField(verbose_name="動画説明文", max_length=2000)
    dt      = models.DateTimeField(verbose_name="投稿日", default=timezone.now)

    def __str__(self):
        return self.title