import sys
import os
import requests
import pytesseract
from PIL import Image
from io import StringIO

"""
Thanks: https://realpython.com/setting-up-a-simple-ocr-server/
"""

IMAGE_EXTENSIONS = [
    '.png', 
    '.jpg', 
    '.jpeg', 
    '.tiff', 
    '.bmp', 
    '.gif'
]


def save_file(filename, content):
    import codecs
    file = codecs.open(filename, "w", "utf-8")
    file.write(content)
    file.close()


def is_image(filename):
    return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))


def get_image_from_url(url):
    return Image.open(StringIO(requests.get(url).content))


def get_image_from_file(filename):
    return Image.open(filename)

def treat_text(text):
    text = text.replace('\n\n', '<p>')
    text = text.replace('\n', ' ')
    text = text.replace('<p>', '\n\n')
    while '  ' in text: text = text.replace('  ', ' ')
    return text.strip()


def ocr_image(image):
    return pytesseract.image_to_string(image)


if __name__ == '__main__':
    sys.stdout.write("A simple OCR utility\n")
    for p in ['input', 'output']:
        if not os.path.isdir(p):
            os.mkdir(p)
    files = os.listdir('input')
    print(os.getcwd())
    for file in files:
        input_file = 'input/%s' % file
        if is_image(input_file):
            for a in IMAGE_EXTENSIONS:
                if a in file.lower():
                    output_file = 'output/%s' % file.replace(a, '.txt')
            image = get_image_from_file(input_file)
            content = ocr_image(image)
            save_file(output_file, treat_text(content))
            sys.stdout.write("%s OK!\n" % file)
        elif os.path.isdir(input_file):
            print(f'{input_file} is dir')
            output_file = 'output/%s.txt' % file
            content = ''
            subfiles = os.listdir(input_file)
            subfiles.sort()
            for subfile in subfiles:
                input_file = 'input/%s/%s' % (file, subfile)
                if is_image(input_file):
                    print(input_file)
                    image = get_image_from_file(input_file)
                    content += ocr_image(image).strip()
            save_file(output_file, treat_text(content))
            sys.stdout.write("%s OK!\n" % output_file)
