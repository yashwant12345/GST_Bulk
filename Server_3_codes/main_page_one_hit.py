import requests
# from scrapy.selector import Selector
import pandas as pd
import pdb,sys,uuid
import cv2
import os
import random
# import bs4
import traceback
# import glob2
# import glob
import numpy as np
from datetime import datetime
# import smtplib 
# from email.mime.multipart import MIMEMultipart 
# from email.mime.text import MIMEText 
# from email.mime.base import MIMEBase
import time
import pdb
import multiprocessing as mp
import uuid
import pytesseract
import shutil
# from details_gst import gstinDownload
# from read_code import readfunction
# from proxy_change import proxy_change
from proxy_change import proxy_change



c_date = str(datetime.now()).split(" ")[0]
print (c_date)
# exit()

log = "/DriveF/GST/log"
if not os.path.exists(log):
	os.makedirs(log)

with open(log+'/'+c_date+'_start_end_txt','a') as ap:
	ap.write("Start "+str(datetime.now())+'\n')

def MainFunctionCall(inputrow):
	print ("main function",inputrow)
	# p_ip = "5.79.66.2:13081"

	rand_sleep_time = random.randint(0, 3)
	print ("Sleep time is :",rand_sleep_time)
	time.sleep(rand_sleep_time)

	def read_captcha(img_path):
		# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
		# confg = r'--oem 3 --psm 8 --tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata" outputbase digits'
		confg = '--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'

		# img_path = r"D:\Working\Python\virtualenv\gst_captcha\mycodes\GST\captcha\9e83451a-05fe-4d95-b657-a0ba42501aa1.png"
		# img_path = r"/DriveF/GST/sample_captcha/4df08adf-05dc-4424-8ac8-c3f893b1c013.png"
		bmp_path = img_path.replace(".png",".bmp")

		img = cv2.imread(img_path)
		# cv2.imshow('Original', img)
		# img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# cv2.imshow('Grey', img_grey)
		thresh, mask = cv2.threshold(img, 40, 255, cv2.THRESH_BINARY)
		# cv2.imshow('THRESH', mask)

		# get the sizes
		h, w = mask.shape[:2]
		# print ("h:",h,"w:",w)

		mask[:, 0] = 255
		mask[:, 1] = 255
		mask[:, w-1] = 255
		mask[:, w-2] = 255
		mask[0, :] = 255
		mask[1, :] = 255
		mask[h-1, :] = 255
		mask[h-2, :] = 255
		# cv2.imshow('mask', mask)

		img_grey = mask

		ls = [	{"h1":0,"h2":26,"w1":44,"w2":60,"tx":0,"ty":1},
				{"h1":0,"h2":26,"w1":60,"w2":66,"tx":0,"ty":2},
				{"h1":0,"h2":26,"w1":66,"w2":72,"tx":0,"ty":3},
				{"h1":0,"h2":26,"w1":72,"w2":78,"tx":0,"ty":4},
				{"h1":0,"h2":26,"w1":78,"w2":86,"tx":0,"ty":5},
				{"h1":0,"h2":26,"w1":86,"w2":99,"tx":0,"ty":6},
				{"h1":0,"h2":26,"w1":99,"w2":106,"tx":0,"ty":5},
				{"h1":0,"h2":26,"w1":106,"w2":111,"tx":0,"ty":4},
				{"h1":0,"h2":26,"w1":111,"w2":117,"tx":0,"ty":3},
				{"h1":0,"h2":26,"w1":117,"w2":124,"tx":0,"ty":2},
				{"h1":0,"h2":26,"w1":124,"w2":141,"tx":0,"ty":1},
				{"h1":26,"h2":50,"w1":44,"w2":60,"tx":0,"ty":-1},
				{"h1":26,"h2":50,"w1":60,"w2":66,"tx":0,"ty":-2},
				{"h1":26,"h2":50,"w1":66,"w2":72,"tx":0,"ty":-3},
				{"h1":26,"h2":50,"w1":72,"w2":78,"tx":0,"ty":-4},
				{"h1":26,"h2":50,"w1":78,"w2":86,"tx":0,"ty":-5},
				{"h1":26,"h2":50,"w1":86,"w2":99,"tx":0,"ty":-6},
				{"h1":26,"h2":50,"w1":99,"w2":106,"tx":0,"ty":-5},
				{"h1":26,"h2":50,"w1":106,"w2":111,"tx":0,"ty":-4},
				{"h1":26,"h2":50,"w1":111,"w2":117,"tx":0,"ty":-3},
				{"h1":26,"h2":50,"w1":117,"w2":124,"tx":0,"ty":-2},
				{"h1":26,"h2":50,"w1":124,"w2":141,"tx":0,"ty":-1}
				]
		# print (len(ls))
		# print (ls[0]["h2"])

		for i in range(len(ls)):
			# print (i)
			h1 = ls[i]["h1"]
			h2 = ls[i]["h2"]
			w1 = ls[i]["w1"]
			w2 = ls[i]["w2"]
			tx = ls[i]["tx"]
			ty = ls[i]["ty"]

			matrix =[[1, 0, tx], #x 
				 	 [0, 1, ty]] #y
			t = np.float32(matrix)

			img_crop = img_grey[h1:h2, w1:w2]
			# print (img_crop)
			# cv2.imshow('img_crop', img_crop)
			h, w = img_crop.shape[:2]

			# transform
			img_trans = cv2.warpAffine(img_crop, t, (w, h), borderValue=(255,255,255))
			# cv2.imshow('img_trans', img_trans)

			# replace
			img_grey[h1:h2, w1:w2] = img_trans
			# cv2.imshow(str(i), img_grey)

		# cv2.imshow("Result", img_grey)
		# cv2.imwrite(bmp_path,img_grey)

		# confg = '--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'

		def thin_font(image,k):
			image = cv2.bitwise_not(image)
			kernel = np.ones((k,k),np.uint8)
			image = cv2.erode(image, kernel, iterations=1)
			image = cv2.bitwise_not(image)
			return (image)

		img_thin_font = thin_font(img_grey,3)
		# cv2.imshow("3", img_thin_font)

		img_final = img_thin_font
		text_ = pytesseract.image_to_string(img_final,config=confg)
		text_ = text_.strip()
		# print (("OCR3 ",text_,len(text_)))

		if len(text_) == 6:
			return text_

		else:

			img_thin_font = thin_font(img_grey,2)
			# cv2.imshow("2", img_thin_font)

			img_final = img_thin_font
			text_ = pytesseract.image_to_string(img_final,config=confg)
			text_ = text_.strip()
			# print (("OCR2 ",text_,len(text_)))

			if len(text_) == 6:
				return text_
			else:
				# read_captcha2
				kernel = np.ones((3,3),np.uint8)
				closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations = 1)
				closing = cv2.cvtColor(closing, cv2.COLOR_BGR2GRAY)

				text_ = pytesseract.image_to_string(closing,config=confg)
				text_ = text_.strip()
				# print (("closing OCR ",text_,len(text_)))

				if len(text_) == 6:
					return text_
				else:
					return "Captcha Reload"

			cv2.waitKey(0)

	captcha_save = "/DriveF/GST/captcha"
	if not os.path.exists(captcha_save):
		os.makedirs(captcha_save)

	maindir_save = "/DriveF/GST/main_page"
	if not os.path.exists(maindir_save):
		os.makedirs(maindir_save)

	tempdir_save = "/DriveF/GST/temp"
	if not os.path.exists(tempdir_save):
		os.makedirs(tempdir_save)

	maindir_save2 = "/DriveF/GST/main_page_2"
	if not os.path.exists(maindir_save2):
		os.makedirs(maindir_save2)

	pan_no = inputrow.split("|")[0]
	cin = inputrow.split("|")[1]
	pan_no = pan_no.strip()
	print (pan_no)
	# exit()

	pan_folder = maindir_save
	if not os.path.exists(pan_folder):
		os.makedirs(pan_folder)

	filesave_1 = pan_folder+'/'+str(pan_no)+'_'+str(cin)+'_main.json'
	no_data = pan_folder+'/'+str(pan_no)+'_'+str(cin)+'_main_no_records.json'
	done_file = pan_folder+'/'+str(pan_no)+'_'+str(cin)+'_main_done.json'
	done_read = pan_folder+'/'+str(pan_no)+'_'+str(cin)+'_main_read_done.json'
	pending_done = pan_folder+'/'+str(pan_no)+'_'+str(cin)+'_main_read_pending.json'

	# filesave_2 = maindir_save2+'/'+str(pan_no)+'_'+str(cin)+'_main.json'
	# no_data2 = maindir_save2+'/'+str(pan_no)+'_'+str(cin)+'_main_no_records.json'
	# done_read2 = maindir_save2+'/'+str(pan_no)+'_'+str(cin)+'_main_read_done.json'
	# done_file2 = maindir_save2+'/'+str(pan_no)+'_'+str(cin)+'_main_done.json'
	# pending_done2 = maindir_save2+'/'+str(pan_no)+'_'+str(cin)+'_main_read_pending.json'

	# if not os.path.exists(filesave_1) and not os.path.exists(no_data) and not os.path.exists(done_file) and not os.path.exists(done_read) and not os.path.exists(filesave_2) and not os.path.exists(no_data2) and not os.path.exists(done_file2) and not os.path.exists(done_read2):
	if not os.path.exists(filesave_1) and not os.path.exists(no_data) and not os.path.exists(done_file) and not os.path.exists(done_read) and not os.path.exists(pending_done):
		
		flag = 1
		while flag == 1:
			try:
				proxy_flag = 1
				while proxy_flag==1:
					proxy_ip = proxy_change()
					p_ip=proxy_ip
					print ("proxy assigned",p_ip)
					proxy_flag = 0

				useragent_list = ["Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
									"Mozilla/5.0 (Linux; U; Android 4.0.3; de-ch; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
									"Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9",
									"Mozilla/5.0 (Linux; U; Android 2.3.5; zh-cn; HTC_IncredibleS_S710e Build/GRJ90) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
									"Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
									"Mozilla/5.0 (Linux; U; Android 2.3.4; fr-fr; HTC Desire Build/GRJ22) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
									"Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; T-Mobile myTouch 3G Slide Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
									"Mozilla/5.0 (Linux; U; Android 2.3.3; zh-tw; HTC_Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
									"Mozilla/5.0 (Linux; U; Android 2.3.3; zh-tw; HTC_Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari",
									"Mozilla/5.0 (Linux; U; Android 2.3.3; zh-tw; HTC Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
									"Mozilla/5.0 (Linux; U; Android 2.3.3; ko-kr; LG-LU3000 Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
									"Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
									"Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile",
									"Mozilla/5.0 (Linux; U; Android 2.3.3; de-de; HTC Desire Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
									"Mozilla/5.0 (Linux; U; Android 2.3.3; de-ch; HTC Desire Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
									"Mozilla/5.0 (Linux; U; Android 2.2; fr-lu; HTC Legend Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
									"Mozilla/5.0 (Linux; U; Android 2.2; en-sa; HTC_DesireHD_A9191 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
									"Mozilla/5.0 (Linux; U; Android 2.2.1; fr-fr; HTC_DesireZ_A7272 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
									"Mozilla/5.0 (Linux; U; Android 2.2.1; en-gb; HTC_DesireZ_A7272 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
									"Mozilla/5.0 (Linux; U; Android 2.2.1; en-ca; LG-P505R Build/FRG83) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"]

				session = requests.session()
				session.proxies = {"http":"http://"+str(p_ip),"https":"http://"+str(p_ip)}

				get_hdr={"Host": "services.gst.gov.in",
						"Origin": "https://services.gst.gov.in",
						"Connection":"keep-alive"}

				user_agent_num = random.randint(0,len(useragent_list)-1)
				# get_hdr['User-Agent']=str(useragent_list[user_agent_num])

				# req2 = session.get("https://services.gst.gov.in",headers=get_hdr,timeout=120)
				# print ("req2",req2)

				# req = session.get("https://services.gst.gov.in/services/searchtpbypan",headers=get_hdr,timeout=120)
				# print ("req",req)

				rand_num = random.uniform(0,1)

				captcha_url = "https://services.gst.gov.in/services/captcha?rnd="+str(rand_num)
				print (captcha_url)

				captcha_hdr = {
					"Host": "services.gst.gov.in",
					"Origin": "https://services.gst.gov.in",
					"Referer": "https://services.gst.gov.in/services/searchtpbypan",
					"Connection":"keep-alive",
					# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
					"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
				}

				# user_agent_num = random.randint(0,len(useragent_list)-1)
				captcha_hdr['User-Agent']=str(useragent_list[user_agent_num])

				uid = uuid.uuid4()

				captcha_req = session.get(captcha_url, headers = captcha_hdr, timeout = 30)
				print ("captcha_req",captcha_req)

				with open(captcha_save+"/"+str(uid)+'.png','wb') as wr:
					wr.write(captcha_req.content)

				captcha = read_captcha(captcha_save+"/"+str(uid)+'.png')
				captcha = captcha.strip() if captcha else ''
				if "Captcha Reload" in captcha:
					print ("Reload Captcha")
					time.sleep(2)
					flag = 1
				else:

					# captcha = raw_input()
					print (captcha)

					# post_hdrs = {
					# 	"Accept": "application/json, text/plain, */*",
					# 	"Accept-Encoding": "gzip, deflate, br",
					# 	"Accept-Language": "en-US,en;q=0.9",
					# 	"Connection": "keep-alive",
					# 	"Content-Length": "41",
					# 	"Content-Type": "application/json;charset=UTF-8",
					# 	"Host": "services.gst.gov.in",
					# 	"Origin": "https://services.gst.gov.in",
					# 	"Referer": "https://services.gst.gov.in/services/searchtpbypan",
					# 	"Sec-Fetch-Dest": "empty",
					# 	"Sec-Fetch-Mode": "cors",
					# 	"Sec-Fetch-Site": "same-origin",
					# 	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
					# }

					post_hdrs = {
						"Host": "services.gst.gov.in",
						"Origin": "https://services.gst.gov.in",
						"Referer": "https://services.gst.gov.in/services/searchtpbypan",
						"Connection":"keep-alive",
						"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
					}

					# user_agent_num = random.randint(0,len(useragent_list)-1)
					post_hdrs['User-Agent']=str(useragent_list[user_agent_num])

					payload = {"panNO": pan_no, "captcha": str(captcha)}
					# payload = {"panNO": pan_no, "captcha": "123456"}
					print (payload)

					url = "https://services.gst.gov.in/services/api/get/gstndtls"
					print (url)
					post_req = session.post(url, json = payload, headers = post_hdrs, timeout = 120)
					print ("post_req",post_req)
					# pdb.set_trace()

					if post_req.status_code==200:
						if "SWEB_9000" in post_req.text:
							print ("invalid captcha")
						elif "SWEB_10001" in post_req.text:
							temp_save = tempdir_save+'/'+str(pan_no)+'_'+str(cin)+'_main_no_records.json'
							if os.path.exists(temp_save):
								os.remove(temp_save)
							with open(temp_save,'w') as wr:
								wr.write(post_req.text)
							shutil.move(temp_save,maindir_save)

							flag = 0
						else:							
							temp_save = tempdir_save+'/'+str(pan_no)+'_'+str(cin)+'_main.json'
							if os.path.exists(temp_save):
								os.remove(temp_save)
							with open(temp_save,'w') as wr:
								wr.write(post_req.text)



							shutil.move(temp_save,maindir_save)
							# gstinDownload(pan_no)
							# readfunction(pan_folder,cin)

							flag = 0
					else:
						time.sleep(2)


			except Exception as er:
				print (er)
				proxy_flag = 1
				while proxy_flag==1:
					proxy_ip = proxy_change()
					p_ip=proxy_ip
					print ("proxy assigned",p_ip)
					
					proxy_flag = 0
				time.sleep(2)
				err = traceback.format_exc()
				print (err)
				with open(log+'/start_end_txt','a') as ap:
					ap.write("Error in main "+str(err)+" "+str(datetime.now())+'\n')
				flag = 1

	else:
		print ("skipped")


# file = "/DriveF/inputs/DirectorPAn.txt"

file = "/DriveF/inputs/PAN.txt"

with open(file,'r') as rd:
	file_data = rd.readlines()

file_data = [x.replace("_Empty","").strip() for x in file_data]
file_data = list(set(file_data))
# print ("================",len(file_data))
# print (file_data[:2])
# exit()
pool = mp.Pool(processes=4)
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

done_file = file.replace("_Pending.txt","_Done.txt")
os.rename(file,done_file)

with open(log+'/start_end_txt','a') as ap:
	ap.write("End "+str(datetime.now())+'\n')