from django.db import models

class Tenant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subdomain = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)  # 👈 add thi
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['subdomain'])]

    def __str__(self):
        return self.name