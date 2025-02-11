from django.conf import settings
import os
import shutil

from ..models import Photo


class NoCategoryPhotos:    
    def create_dir(self):
        if not os.path.exists(settings.NO_CATEGORY_ROOT):
            os.mkdir(settings.NO_CATEGORY_ROOT)
    
    def move_files(self):
        for root, dirs, files in os.walk(settings.MEDIA_ROOT, topdown=False):

            # Move files
            for file in files:
                if file.lower().endswith(Photo.EXTENSIONS):  # Case-insensitive extension check
                    src_file_path = os.path.join(root, file)
                    dest_file_path = os.path.join(settings.NO_CATEGORY_ROOT, file)

                    try:
                        shutil.move(src_file_path, dest_file_path)
                        print(f"Moved: {src_file_path} -> {dest_file_path}")
                    except shutil.Error as e:
                        print(f"Error moving {src_file_path}: {e}")

                    file_name = file.split('/')[-1]
                    photo = Photo(name=file_name, category=None)
                    photo.save()
            
            # Delete empty dirs
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if os.path.exists(dir_path) and not os.listdir(dir_path):
                    try:
                        os.rmdir(dir_path)
                        print(f"Deleted empty directory: {dir_path}")
                    except OSError as e:
                        print(f"Error deleting directory {dir_path}: {e}")