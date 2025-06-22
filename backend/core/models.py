from django.db import models

# Create your models here.

class Core(models.Model):
    """
    Core model for the application.
    This can be extended with additional fields as needed.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This model is intended to be inherited, not used directly.

    def __str__(self):
        return f"Core Model (ID: {self.id})"
