import requests
from scrapy.selector import Selector
import pandas as pd
import pdb,sys,uuid
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
from read_code import readfunction
from proxy_change import proxy_change



c_date = str(datetime.now()).split(" ")[0]
print (c_date)
exit()

log = "/DriveD/GST/log"
if not os.path.exists(log):
	os.makedirs(log)

with open(log+'/'+c_date+'_start_end_txt','a') as ap:
	ap.write("Start "+str(datetime.now())+'\n')

def MainFunctionCall(inputrow):
	# print ("main function")

	rand_sleep_time = random.randint(0, 5)
	print ("Sleep time is :",rand_sleep_time)
	time.sleep(rand_sleep_time)

	proxy_flag = 1
	while proxy_flag==1:
		proxy_ip = proxy_change()
		p_ip=proxy_ip
		print ("proxy assigned",p_ip)
		
		proxy_flag = 0


	def read_captcha2(captcha_path):
		bmp_path = captcha_path.replace(".png",".bmp")
		txt_path = captcha_path.replace(".png","")

		img = cv2.imread(captcha_path)
		# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# cv2.imshow("img", img)
		ret, mask = cv2.threshold(img, 10, 225, cv2.THRESH_BINARY)
		# cv2.imshow("mask", mask)
		# cv2.waitKey(0)
		# print (img)
		# with open('abc.txt', 'w') as wr:
		# 	wr.write(img)
		# np.savetxt("abc.csv", img, delimiter=",")
		# cv2.imwrite(bmp_path,mask)
		# exit()

		kernel = np.ones((3,3),np.uint8)
		# kernel = np.ones((2,2),np.uint8)
		# opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)#, iterations = 1)
		closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations = 1)
		# kernel = np.ones((1,2),np.uint8)
		# closing = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel, iterations = 1)
		# opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel, iterations = 1)
		closing = cv2.cvtColor(closing, cv2.COLOR_BGR2GRAY)
		# cv2.imshow("closing", closing)
		# cv2.waitKey(0)
		# cv2.imwrite("1.bmp",closing)

		rows, columns = closing.shape
		# print ('rows',rows,'columns',columns)
		# exit()

		# for c in range(1,columns):
		# 	# print (closing[:, c])
		# 	for r in range(1,rows):
		# 		if closing[r, c] == 67 and closing[r-1, c] == 225:
		# 			closing[r, c] = 225
		# 	for r in range(rows-1,-1,-1):
		# 		if closing[r, c] == 67 and closing[r+1, c] == 225:
		# 			closing[r, c] = 225
		# closing = np.where(closing == 67, 0, closing)

		closing[:, 0] = 225
		closing[:, 1] = 225
		closing[:, columns-1] = 225
		closing[:, columns-2] = 225
		closing[0, :] = 225
		closing[1, :] = 225
		closing[rows-1, :] = 225
		closing[rows-2, :] = 225
		
		# print (closing[:, 0])
		# exit()
		# 	for j in closing[:, i]:
		# 		if j_c > 0:
		# 			if j == 67 and 

		# kernel = np.ones((2,2),np.uint8)
		# closing = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel, iterations = 1)

		print ((bmp_path))
		cv2.imwrite(bmp_path,closing)
		# cv2.imshow("mask", mask)
		# cv2.waitKey(0)
		# exit()
		# np.savetxt("abc1.csv", closing, delimiter=",")

		ocr_text = ''
		# ocr_bat = '"C:\Program Files (x86)\Tesseract-OCR\\tesseract.exe" "'+bmp_path+'" "'+txt_path+r'" --psm 7 --oem 0 "E:\Working\Python\Captcha\numbers"'
		# ocr_bat = r'"C:\Program Files\Tesseract-OCR\tesseract.exe"'+' "'+bmp_path+'"'+' "'+txt_path+'"'+' --psm 8 -c tessedit_char_blacklist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		# ocr_bat = 'tesseract '+' "'+bmp_path+'"'+' "'+txt_path+'"'+' --psm 8 -c tessedit_char_whitelist=1234567890'
		# ocr_text = 'tesseract '+'"'+bmp_path+'" '+'"'+txt_path+'.txt"'+' "--psm" '+'"/DriveD/GSTCode/letters_small"'
		# ocr_text = 'tesseract '+'"'+bmp_path+'" '+'"'+txt_path+'" '+"'--psm 8 -c '"+'"/DriveD/GST/Codes/letters_small"'
		# ocr_text = 'tesseract '+'"'+bmp_path+'" '+'"'+txt_path+'" '+"'--psm 8 -c '"+'"/DriveD/gst/Codes/letters_small"'
		ocr_text = 'tesseract '+'"'+bmp_path+'" '+'"'+txt_path+'" '+' --psm 8 -c tessedit_char_whitelist=1234567890'
		print (ocr_text)
		# ocr_text = 'tesseract '+'"'+bmp_path+'" '+'"'+txt_path+'" '+'--psm 8 -c tessedit_char_whitelist=1234567890'
		# print (ocr_text)
		os.system(ocr_text)
		txt_path = txt_path + '.txt'

		if os.path.isfile(txt_path):
			with open(txt_path) as f: 
				ocr_text = f.read()
				ocr_text = ocr_text.replace("\n", "").replace(" ", "")
			# os.remove(txt_path)
		else:
			print ('captcha txt file not found')
		# if os.path.isfile(bmp_path):
			# os.remove(bmp_path)
		print (("sss-" + ocr_text + "-ss"))
		return ocr_text

	def read_captcha(captcha_path):
		# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
		confg = '--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'
		# confg = '--psm 8 '+'"/DriveD/GST/Codes/letters_small"'

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

		if len(text_) == 6:
			return text_
		else:
			img_thin_font = thin_font(mask,2)
			# cv2.imshow('2Font', img_thin_font)
			img_final = img_thin_font
			text_ = pytesseract.image_to_string(img_final,config=confg)
			text_ = text_.strip()
			print (("sssssssssss",text_,len(text_)))
			# print(pytesseract.image_to_string(img_final,config=confg))

			if len(text_) == 6:
				return text_
			else:
				text_ = read_captcha2(captcha_path)
				text_ = text_.strip()
				if len(text_) == 6:
					return text_
				else:
					return "Captcha Reload"


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

	session = requests.session()
	# session.proxies = {"http":"http://posquryx-100:cak55d3jxw0t@p.webshare.io:80","https":"https://posquryx-100:cak55d3jxw0t@p.webshare.io:80"}
	# session.proxies = {"https":"https://posquryx-1:cak55d3jxw0t@p.webshare.io:80"}

	captcha_save = "/DriveD/GST/captcha"
	if not os.path.exists(captcha_save):
		os.makedirs(captcha_save)

	maindir_save = "/DriveD/GST/main_page"
	if not os.path.exists(maindir_save):
		os.makedirs(maindir_save)


	pan_no = inputrow.split("~")[0]
	cin = inputrow.split("~")[-1]
	pan_no = pan_no.strip()
	print (pan_no)
	pan_folder = maindir_save+'/'+pan_no
	if not os.path.exists(pan_folder):
		os.makedirs(pan_folder)
	flag = 1
	while flag == 1:
		try:
			

			session = requests.session()
			session.proxies = {"http":"http://"+str(p_ip),"https":"https://"+str(p_ip)}

			req2 = session.get("https://services.gst.gov.in",timeout=60)
			print ("req2",req2)

			req = session.get("https://services.gst.gov.in/services/searchtpbypan",timeout=60)
			print ("req",req)

			captcha_url = "https://services.gst.gov.in/services/captcha?rnd=0.08350523045361613"

			captcha_hdr = {
				"Host": "services.gst.gov.in",
				"Origin": "https://services.gst.gov.in",
				"Referer": "https://services.gst.gov.in/services/searchtpbypan",
				# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
				"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
			}

			uid = uuid.uuid4()

			captcha_req = session.get(captcha_url, headers = captcha_hdr, timeout = 60)
			print ("captcha_req",captcha_req)

			with open(captcha_save+"/"+str(uid)+'.png','wb') as wr:
				wr.write(captcha_req.content)

			captcha = read_captcha(captcha_save+"/"+str(uid)+'.png')
			captcha = captcha.strip() if captcha else ''
			if "Captcha Reload" in captcha:
				print ("Reload Captcha")
				flag = 1
			else:

				# captcha = raw_input()
				print (captcha)

				post_hdrs = {
					"Accept": "application/json, text/plain, */*",
					"Accept-Encoding": "gzip, deflate, br",
					"Accept-Language": "en-US,en;q=0.9",
					"Connection": "keep-alive",
					"Content-Length": "41",
					"Content-Type": "application/json;charset=UTF-8",
					"Host": "services.gst.gov.in",
					"Origin": "https://services.gst.gov.in",
					"Referer": "https://services.gst.gov.in/services/searchtpbypan",
					"Sec-Fetch-Dest": "empty",
					"Sec-Fetch-Mode": "cors",
					"Sec-Fetch-Site": "same-origin",
					"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
				}

				payload = {"panNO": pan_no, "captcha": str(captcha)}
				# payload = {"panNO": pan_no, "captcha": "123456"}
				print (payload)

				url = "https://services.gst.gov.in/services/api/get/gstndtls"
				print (url)
				post_req = session.post(url, json = payload, headers = post_hdrs, timeout = 60)
				print ("post_req",post_req)
				# pdb.set_trace()

				if post_req.status_code==200:
					if "SWEB_9000" in post_req.text:
						print ("invalid captcha")
					elif "SWEB_10001" in post_req.text:
						with open(pan_folder+'/'+str(pan_no)+'_'+str(cin)+'_main_no_records.json','w') as wr:
							wr.write(post_req.text)
						flag = 0
					else:
						with open(pan_folder+'/'+str(pan_no)+'_'+str(cin)+'_main.json','w') as wr:
							wr.write(post_req.text)
						gstinDownload(pan_no)
						# readfunction(pan_folder,cin)

						flag = 0

		except:
			proxy_flag = 1
			while proxy_flag==1:
				proxy_ip = proxy_change()
				p_ip=proxy_ip
				print ("proxy assigned",p_ip)
				
				proxy_flag = 0
			err = traceback.format_exc()
			print (err)
			with open(log+'/start_end_txt','a') as ap:
				ap.write("Error in main "+str(err)+" "+str(datetime.now())+'\n')
			flag = 1

# file = "/DriveD/GST/Inputs/AAACR5055K.txt"
file = "/DriveD/GST/Inputs/PAN.txt"
with open(file,'r') as rd:
	file_data = rd.readlines()

file_data = [x.strip() for x in file_data]
print (len(file_data))
pool = mp.Pool(processes=60)
results = [pool.apply_async(MainFunctionCall, args=(value,)) for value in file_data]
pool.close()
pool.join()
flag4 = 1
while flag4 == 1:
	try:
		output = [p.get() for p in results]
		flag4 = 0
	except:
		flag4 = 1
	flag4 = 0

with open(log+'/start_end_txt','a') as ap:
	ap.write("End "+str(datetime.now())+'\n')