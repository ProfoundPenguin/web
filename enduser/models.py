import uuid
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone

# Create your models here.
class Announcement(models.Model):
    image = models.ImageField(upload_to='announcements/')
    title = models.CharField(max_length=200)
    caption = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()

    class Meta:
        verbose_name = "Announcements"
        verbose_name_plural = "Announcements"

    def save(self, *args, **kwargs):
        # Open the image using Pillow
        img = Image.open(self.image)

        # Resize the image
        if img.width > 500:
            # Calculate the new height to maintain aspect ratio
            ratio = 500 / float(img.width)
            height = int((float(img.height) * float(ratio)))
            img = img.resize((500, height))

        # Convert the image to WebP format
        buffer = BytesIO()
        img.save(fp=buffer, format='WEBP')

        # Generate a new file name with a unique identifier
        new_filename = f"{uuid.uuid4()}.webp"

        # Save the converted image with the new file name
        self.image.save(new_filename, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Landing(models.Model):
    image = models.ImageField(upload_to='landing/')

    class Meta:
        verbose_name = "Landing Page Image"
        verbose_name_plural = "Landing Page Image"

    def save(self, *args, **kwargs):
        # Open the image using Pillow
        img = Image.open(self.image)

        # Resize the image
        if img.width > 700:
            # Calculate the new height to maintain aspect ratio
            ratio = 700 / float(img.width)
            height = int((float(img.height) * float(ratio)))
            img = img.resize((700, height), Image.ANTIALIAS)

        # Convert the image to WebP format
        buffer = BytesIO()
        img.save(fp=buffer, format='WEBP')

        # Generate a new file name with a unique identifier
        new_filename = f"{uuid.uuid4()}.webp"

        # Save the converted image with the new file name
        self.image.save(new_filename, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image: {self.image.name}"

class Team(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    image = models.ImageField(upload_to='team/')

    class Meta:
        verbose_name = "Modify Team Section"
        verbose_name_plural = "Modify Team Section"

    def save(self, *args, **kwargs):
        # Open the image using Pillow
        img = Image.open(self.image)

        # Resize the image
        if img.width > 300:
            # Calculate the new height to maintain aspect ratio
            ratio = 300 / float(img.width)
            height = int((float(img.height) * float(ratio)))
            img = img.resize((300, height))

        # Convert the image to WebP format
        buffer = BytesIO()
        img.save(fp=buffer, format='WEBP')

        # Generate a new file name with a unique identifier
        new_filename = f"{uuid.uuid4()}.webp"

        # Save the converted image with the new file name
        self.image.save(new_filename, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image: {self.image.name}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    class Meta:
        verbose_name = "Modify Courses Section"
        verbose_name_plural = "Modify Courses Section"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.convert_and_resize_image()

    def convert_and_resize_image(self):
        image_path = self.image.path
        with Image.open(image_path) as img:
            img = img.convert("RGBA")  # Ensure transparency is preserved
            img.thumbnail((30, img.height))
            img.save(image_path, "WEBP", lossless=True)

class Subject(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subjects')

    class Meta:
        verbose_name = "Add or Remove Subjects"
        verbose_name_plural = "Add or Remove Subjects"

    def __str__(self):
        return self.name

class Why(models.Model):
    image = models.ImageField(upload_to='why/', blank=True)
    title = models.CharField(max_length=200)
    caption = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Modify (Why enroll) Section"
        verbose_name_plural = "Modify (Why enroll) Section"

    def save(self, *args, **kwargs):
        # Open the image using Pillow
        img = Image.open(self.image)

        # Resize the image
        if img.width > 100:
            # Calculate the new height to maintain aspect ratio
            ratio = 100 / float(img.width)
            height = int((float(img.height) * float(ratio)))
            img = img.resize((100, height), Image.ANTIALIAS)

        # Convert the image to WebP format
        buffer = BytesIO()
        img.save(fp=buffer, format='WEBP')

        # Generate a new file name with a unique identifier
        new_filename = f"{uuid.uuid4()}.webp"

        # Save the converted image with the new file name
        self.image.save(new_filename, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

def get_default_expired_date():
    return timezone.make_aware(datetime(2000, 1, 1))

class AnnouncementBar(models.Model):
    text = models.TextField(null=False, blank=False, default="Type a new announcement here.")
    # image = models.ImageField(upload_to='announcementBar/', blank=False, default="default.jpg")
    expiration_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk and AnnouncementBar.objects.exists():
            raise ValidationError('There is already an instance of AnnouncementBar.')
        return super(AnnouncementBar, self).save(*args, **kwargs)

    def __str__(self):
        return "Announcement Bar"

    class Meta:
        verbose_name = "Announcement Bar"
        verbose_name_plural = "Announcement Bars"