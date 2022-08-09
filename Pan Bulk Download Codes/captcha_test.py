import requests
from scrapy.selector import Selector
import pandas as pd
import pdb,sys,uuid
# reload(sys)
# sys.setdefaultencoding("utf-8")
# import requesocks
import cv2
import os
import random
import bs4
import traceback
import glob2
import glob
import numpy as np
from datetime import datetime
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase
import time
import pdb
import multiprocessing as mp
import uuid
import pytesseract
from details_gst import gstinDownload




def read_captcha(captcha_path):
	# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
	confg = '--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'

	img = cv2.imread(captcha_path)
	# cv2.imshow('Original', img)
	# img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# cv2.imshow('Grey', img_grey)
	thresh, mask = cv2.threshold(img, 40, 255, cv2.THRESH_BINARY)
	# cv2.imshow('THRESH', mask)
	# kernel = np.ones((3,3),np.uint8)
	# closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations = 1)
	# cv2.imshow('Closing', closing)

	def thin_font(image,k):
		image = cv2.bitwise_not(image)
		kernel = np.ones((k,k),np.uint8)
		image = cv2.erode(image, kernel, iterations=1)
		image = cv2.bitwise_not(image)
		return (image)

	img_thin_font = thin_font(mask,3)
	# cv2.imshow('3Font', img_thin_font)

	img_final = img_thin_font
	text_ = pytesseract.image_to_string(img_final,config=confg)
	text_ = text_.strip()
	print (("sssssssssss",text_,len(text_)))

	img_thin_font = thin_font(mask,2)
	# cv2.imshow('2Font', img_thin_font)
	img_final = img_thin_font
	text_ = pytesseract.image_to_string(img_final,config=confg)
	text_ = text_.strip()
	print (("sssssssssss",text_,len(text_)))
		# print(pytesseract.image_to_string(img_final,config=confg))


	#############################################
	#### Detecting Characters  ######
	#############################################
	# hImg, wImg,_ = img.shape
	# boxes = pytesseract.image_to_boxes(img,config=confg)
	# for b in boxes.splitlines():
	# 	# print(b)
	# 	b = b.split(' ')
	# 	# print(b)
	# 	x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
	# 	cv2.rectangle(img, (x,hImg- y), (w,hImg- h), (50, 50, 255), 2)
	# 	cv2.putText(img,b[0],(x,hImg- y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)


	# cv2.imshow('Result', img_final)
	cv2.waitKey(0)


read_captcha("/home/ubuntu/Downloads/cap/f87c3eff-5f73-4d74-8039-0e7cbe66c208.png")