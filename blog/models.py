from django.db import models
import os

class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    MEDIA_TYPES = [
        ('image', 'Imagen'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Documento'),
    ]
    
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    
    media_file = models.FileField(upload_to='posts/media/', blank=True, null=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, blank=True, null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.media_file:
            file_extension = self.media_file.name.lower().split('.')[-1]
            
            if file_extension in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                self.media_type = 'image'
            elif file_extension in ['mp4', 'avi', 'mov', 'wmv', 'flv']:
                self.media_type = 'video'
            elif file_extension in ['mp3', 'wav', 'ogg', 'flac']:
                self.media_type = 'audio'
            elif file_extension in ['pdf', 'doc', 'docx', 'txt']:
                self.media_type = 'document'
        
        super().save(*args, **kwargs)
    
    @property
    def has_media(self):
        return bool(self.media_file)
    
    @property
    def is_image(self):
        return self.media_type == 'image'
    
    @property
    def is_video(self):
        return self.media_type == 'video'
    
    @property
    def is_audio(self):
        return self.media_type == 'audio'
    
    @property
    def is_document(self):
        return self.media_type == 'document'

class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.post}'"