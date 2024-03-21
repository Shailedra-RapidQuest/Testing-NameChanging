import re, os

def url_safe_image_name(s):
    filename, extension = os.path.splitext(s)
    filename = re.sub(r'[^\w\-]', '', filename.lower())[:70]
    return filename + extension