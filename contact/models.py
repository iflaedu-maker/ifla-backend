from django.db import models


class ContactMessage(models.Model):
    """Contact form message model"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    language = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} ({self.email})"

