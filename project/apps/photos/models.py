from django.db import models
from django.conf import settings

from PIL import Image
from PIL.ExifTags import TAGS
import os
from datetime import datetime
import uuid
from enum import IntEnum


class Category(models.Model):
    """
    Model representing a category for photos.
    
    Attributes
    ----------
    name : CharField
        Unique name of the category.

    Notes
    -----
    Category name also resembles name of a directory that stores photos of certain category.
    """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Photo(models.Model):
    """
    Model representing a photo uploaded to the system.
    
    Attributes
    ----------
    title : CharField
        Custom name for a photo.
    filename : CharField
        Original filename of the uploaded file.
    image : ImageField
        Image file associated with the photo.
    status : IntegerField
        Status of the photo (Tracked, Lost, Duplicated).
    category : ForeignKey
        Category to which the photo belongs.
    created_at : DateTimeField
        Timestamp indicating when the photo was uploaded.
    """

    class Status(IntEnum):
        TRACKED = 0
        LOST = 1
        DUPLICATED = 2

    PHOTO_STATUS = [
        (Status.TRACKED, 'TRACKED'),
        (Status.LOST, 'LOST'),
        (Status.DUPLICATED, 'DUPLICATED')
    ]

    def upload_to(instance, filename: str) -> str:
        """
        Determines the upload path for an image.
        
        Parameters
        ----------
        instance : Photo
            The instance of the Photo model.
        filename : str
            The original filename of the uploaded file.
        
        Returns
        -------
        str
            The file path where the image will be stored.
        """

        return os.path.join(settings.MEDIA_ROOT, instance.category.name, filename)
    

    title = models.CharField(max_length=255, help_text='Custom name for a photo')
    filename = models.CharField(max_length=255, help_text='Original filename of the uploaded file')
    image = models.ImageField(upload_to=upload_to, help_text='Image path')
    status = models.IntegerField(choices=PHOTO_STATUS, default=Status.TRACKED, help_text='State of a file detected by a system')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True, blank=True, help_text='Category that photo belongs to')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Time when photo was uploaded to a system')


    def save(self, *args, **kwargs):
        """
        Saves the photo object to the database. If a duplicate filename exists, marks the photo as DUPLICATED 
        and assigns it to the 'duplicates' category. Otherwise, assigns it as 'no category'.
        """
        if Photo.objects.filter(filename=self.filename).exists():
            self.status = Photo.Status.DUPLICATED
            self.title = f'{self.title}-{uuid.uuid4().hex}'

            duplicates, created = Category.objects.get_or_create(name=settings.DUPLICATES_DIR)
            self.category = duplicates
        else:
            no_category, created = Category.objects.get_or_create(name=settings.NO_CATEGORY_DIR)
            self.category = no_category
                    
        return super().save(*args, **kwargs)
    
    def get_filepath(self) -> str:
        """
        Returns the file path of the uploaded image.
        
        Returns
        -------
        str
            The absolute file path of the image.

        Notes
        -----
        `Photo.image.url` returns file path adjusted for web browser needs (eg. replaces spaces with '%20').
        """
        return f'{settings.MEDIA_ROOT}/{self.image.name}'
    
    def get_creation_date(self) -> str | None:
        """
        Extracts the creation date of the photo from its EXIF metadata.
        
        Returns
        -------
        str or None
            The formatted creation date in format specified at `settings.PHOTOS_DATETIME_FORMAT`
        """

        with Image.open(self.get_filepath()) as img:
            # Extract EXIF data and find the 'DateTime' tag
            exif_data = img._getexif()
            
            if exif_data is None:
                return None

            for tag, value in exif_data.items():
                if TAGS.get(tag) == 'DateTime':
                    # Change to proper time format
                    date = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                    return date.strftime(settings.PHOTOS_DATETIME_FORMAT)

            return None

    def __str__(self):
        return f'{self.category.name} - {self.title}'