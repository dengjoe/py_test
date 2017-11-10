#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test of tesseract-ocr '

__author__ = 'kevin deng'


from wand.image import Image
from PIL import Image as PIL
import pyocr
import pyocr.builders
import io


tool = pyocr.get_available_tools()[0]
lang = tool.get_available_languages()[1]

req_image = []
final_text = []

image_pdf = Image(filename="./传世书.pdf")
image_png = image_pdf.convert('png')

for img in image_png.sequence:
	img_page = Image(image=img)
	req_image.append(img_page.make_blob('png'))

for img in req_image:
	txt = tool.image_to_string(PI.open(io.BytesIO(img)), lang='chi_sim', builder=pyocr.builders.TextBuilder())
	final_text.append(txt)
