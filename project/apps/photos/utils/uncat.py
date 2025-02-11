from django.conf import settings
import os
import shutil


FILES_PATH = os.path.join(settings.MEDIA_ROOT, 'Bez Kategorii')
PHOTOS_EXTENSIONS = ('.png', '.jpg', '.jpeg')


def create_dir():
    if not os.path.exists(FILES_PATH):
        os.mkdir(FILES_PATH)


def move_files():
    for root, dirs, files in os.walk(settings.MEDIA_ROOT, topdown=False):

        # Move files
        for file in files:
            if file.lower().endswith(PHOTOS_EXTENSIONS):  # Case-insensitive extension check
                src_file_path = os.path.join(root, file)
                dest_file_path = os.path.join(FILES_PATH, file)

                try:
                    shutil.move(src_file_path, dest_file_path)
                    print(f"Moved: {src_file_path} -> {dest_file_path}")
                except shutil.Error as e:
                    print(f"Error moving {src_file_path}: {e}")
        

        # Delete empty dirs
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if os.path.exists(dir_path) and not os.listdir(dir_path):
                try:
                    os.rmdir(dir_path)
                    print(f"Deleted empty directory: {dir_path}")
                except OSError as e:
                    print(f"Error deleting directory {dir_path}: {e}")