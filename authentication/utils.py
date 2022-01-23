from PIL import Image, ImageEnhance
import os
from datetime import datetime
from django.conf import settings
from io import BytesIO
from django.core.files import File


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.username, datetime.now().strftime('%Y-%m-%d_%H-%M'), ext)
    return os.path.join('authentication', filename)


def add_watermark(image):
    img = Image.open(image.path)
    watermark = Image.open(settings.WATERMARK_PATH)
    width, height = img.size
    max_size = (width//5, height//5)
    watermark.thumbnail(max_size, Image.ANTIALIAS)
    watermark_x, watermark_y = watermark.size
    x = width - watermark_x
    y = height - watermark_y
    img.paste(watermark, (x, y), watermark)
    img.save(image.path)
    return image
