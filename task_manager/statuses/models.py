from django.db import models

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name