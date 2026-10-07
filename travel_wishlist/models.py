from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

class Place(models.Model):
    # Link each place to the user who created it.
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    # Store the destination name and whether the trip is complete.
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    # Keep optional details about a completed trip.
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)


def save(self, *args, **kwargs):
        # Find the saved record so a replaced photo can be removed.
        old_place = Place.objects.filter(pk=self.pk).first()
        if old_place and old_place.photo:
            if old_place.photo != self.photo:
                self.delete_photo(old_place.photo)

        super().save(*args, **kwargs)


def delete_photo(self, photo):
    # Remove photo files from storage when they are no longer used.
    if default_storage.exists(photo.name):
        default_storage.delete(photo.name)            

def delete(self, *args, **kwargs):
    # Delete the photo file before deleting the database record.
    if self.photo:
           self.delete_photo(self.photo)

    super().delete(*args, **kwargs)


def __str__(self):
    # Provide a readable description of the place in Django tools.
    photo_str = self.photo.url if self.photo else 'no photo'
    notes_str = self.notes[:100] if self.notes else 'no notes'
    return f'{self.pk}: {self.name} visited? {self.visited} on {self.date_visited}\nPhoto {photo_str}'
