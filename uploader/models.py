from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=20
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=255
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    tags = models.ManyToManyField(Tag, blank=True)
    upload = models.FileField(
        upload_to='files/%Y/%m/%d',
        blank=True,
        null=True)

    def __str__(self):
        return self.title
