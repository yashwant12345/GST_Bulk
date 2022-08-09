import requests
# from scrapy.selector import Selector
import pandas as pd
import pdb,sys,uuid
# reload(sys)
# sys.setdefaultencoding("utf-8")
import cv2
import os
import random
import bs4
import traceback
import glob2
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
from proxy_change import proxy_change




c_date = str(datetime.now()).split(" ")[0]

log = "/DriveE/GST/log"
if not os.path.exists(log):
	os.makedirs(log)


def MainFunctionCall(file):
	print (file)

	log = "/DriveE/GST/log"
	if not os.path.exists(log):
		os.makedirs(log)

	done_text = "/DriveE/GST/done_text/"
	if not os.path.exists(done_text):
		os.makedirs(done_text)

	done_text2 = "/DriveE/GST/done_text_main/"
	if not os.path.exists(done_text2):
		os.makedirs(done_text2)

	done_name = file.replace(".json","_done.json")

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

	if "_main_no_records.json" in file:
		os.rename(file,done_name)

		filesave_name = file.split("/")[-1]
		filesave_name = filesave_name.replace("_main_no_records.json","")

		with open(done_text+filesave_name+".txt",'w') as wr:
			wr.write("")

	else:
		filesave_name = file.split("/")[-1]
		filesave_name = filesave_name.replace("_main.json","")

		rand_sleep_time = random.randint(0, 5)
		print ("Sleep time is :",rand_sleep_time)
		time.sleep(rand_sleep_time)

		log = "/DriveE/GST/log"
		if not os.path.exists(log):
			os.makedirs(log)

		with open(log+'/'+c_date+'_gstin_start_end_txt','a') as ap:
			ap.write("Start gstin "+str(datetime.now())+'\n')

		try:

			def read_captcha(img_path):
				# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
				# confg = r'--oem 3 --psm 8 --tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata" outputbase digits'
				confg = '--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'

				# img_path = r"D:\Working\Python\virtualenv\gst_captcha\mycodes\GST\captcha\9e83451a-05fe-4d95-b657-a0ba42501aa1.png"
				# img_path = r"/DriveE/GST/sample_captcha/4df08adf-05dc-4424-8ac8-c3f893b1c013.png"
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


			captcha_save = "/DriveE/GST/captcha"
			if not os.path.exists(captcha_save):
				os.makedirs(captcha_save)

			input_dir = "/DriveE/GST/detail_page/"+filesave_name+"/"
			if not os.path.exists(input_dir):
				os.makedirs(input_dir)


			df = pd.read_json(file)
			# print (df)

			pending_file = file.replace("_main.json","_main_read_pending.json")

			try:
				os.rename(file,pending_file)
			except:
				os.remove(pending_file)
				os.rename(file,pending_file)
		

			gstinResList = df["gstinResList"].tolist()
			print (len(gstinResList))
			for gstin_res in gstinResList:
				gstin = gstin_res["gstin"]
				
				BS_file = input_dir+'/'+str(gstin)+'_Goods_services.json'

				main_detail = input_dir+'/'+str(gstin)+'_main_detail.json'

				fd_file = input_dir+'/'+str(gstin)+'_filing_details.json'

				if not os.path.exists(BS_file) and not os.path.exists(main_detail) and not os.path.exists(fd_file):
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
							session.proxies = {"http":"http://"+str(p_ip),"https":"https://"+str(p_ip)}

							user_agent_num = random.randint(0,len(useragent_list)-1)

							# req2 = session.get("https://services.gst.gov.in",timeout=120)
							# print ("req2",req2)

							# req = session.get("https://services.gst.gov.in/services/searchtp",timeout=60)
							# print ("req",req)

							rand_num = random.uniform(0,1)

							# captcha_url = "https://services.gst.gov.in/services/captcha?rnd=0.08350523045361613"

							captcha_url = "https://services.gst.gov.in/services/captcha?rnd="+str(rand_num)
							print (captcha_url)

							captcha_hdr = {
								"Host": "services.gst.gov.in",
								"Origin": "https://services.gst.gov.in",
								"Referer": "https://services.gst.gov.in/services/searchtp",
								"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
							}

							# user_agent_num = random.randint(0,len(useragent_list)-1)
							captcha_hdr['User-Agent']=str(useragent_list[user_agent_num])

							uid = uuid.uuid4()

							captcha_req = session.get(captcha_url, headers = captcha_hdr, timeout = 30)
							print ("captcha_req",captcha_req)

							with open(captcha_save+"/"+str(uid)+'.png','wb') as wr:
								wr.write(captcha_req.content)

							captcha = read_captcha(captcha_save+"/"+str(uid)+'.png')
							# captcha = raw_input()
							captcha = captcha.strip() if captcha else ''
							if "Captcha Reload" in captcha:
								print ("reload captcha")
								flag = 1
							else:
								print (captcha)

								post_hdrs = {
									"Host": "services.gst.gov.in",
									"Origin": "https://services.gst.gov.in",
									"Referer": "https://services.gst.gov.in/services/searchtp",
									"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
								}
								post_hdrs['User-Agent']=str(useragent_list[user_agent_num])

								payload = {"gstin": gstin, "captcha": str(captcha)}
								# payload = {"panNO": pan_no, "captcha": "123456"}
								print (payload)

								url = "https://services.gst.gov.in/services/api/search/taxpayerDetails"
								print (url)
								post_req = session.post(url, json = payload, headers = post_hdrs, timeout = 60)
								print ("post_req",post_req)
								# pdb.set_trace()

								if post_req.status_code==200:
									if "SWEB_9000" in post_req.text:
										print (("invalid captcha"))
									elif "SWEB_10001" in post_req.text:
										with open(input_dir+'/'+str(gstin)+'_no_records.json','w') as wr:
											wr.write(post_req.text)
										flag = 0
									else:
										with open(input_dir+'/'+str(gstin)+'_main_detail.json','w') as wr:
											wr.write(post_req.text)
										
										url3 = "https://services.gst.gov.in/services/api/search/goodservice?gstin="+gstin
										print (url3)

										get_hdrs = {
											"Host": "services.gst.gov.in",
											"Referer": "https://services.gst.gov.in/services/searchtp",
											"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
										}

										post_hdrs['User-Agent']=str(useragent_list[user_agent_num])

										get_req = session.get(url3, headers = get_hdrs, timeout = 60)
										print ("get_req",get_req)
										# pdb.set_trace()

										if get_req.status_code==200:
											with open(input_dir+'/'+str(gstin)+'_Goods_services.json','w') as wr:
												wr.write(get_req.text)

										url4 = "https://services.gst.gov.in/services/api/search/taxpayerReturnDetails"
										print (url4)
										last_post_hdrs = {
											"Host": "services.gst.gov.in",
											"Origin": "https://services.gst.gov.in",
											"Referer": "https://services.gst.gov.in/services/searchtp",
											"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
										}

										post_hdrs['User-Agent']=str(useragent_list[user_agent_num])


										lastpost_req = session.post(url4, json = payload, headers = post_hdrs, timeout = 60)
										print ("lastpost_req",lastpost_req)
										# pdb.set_trace()

										if lastpost_req.status_code==200:
											if "errorCode" in lastpost_req.text:
												print ("invalid captcha")
												print (lastpost_req.text)
											else:
												with open(input_dir+'/'+str(gstin)+'_filing_details.json','w') as wr:
													wr.write(lastpost_req.text)
												flag = 0

						except:
							proxy_flag = 1
							while proxy_flag==1:
								proxy_ip = proxy_change()
								p_ip=proxy_ip
								print ("proxy assigned",p_ip)
								
								proxy_flag = 0
							trc = traceback.format_exc()
							with open(log+'/'+c_date+'_gstin_start_end_txt','a') as ap:
								ap.write("Error "+str(trc)+"|"+str(datetime.now())+'\n')
							flag = 1

				# with open(done_text+filesave_name+"_"+str(gstin)+".txt",'w') as wr:
				with open(done_text+filesave_name+"_"+str(gstin)+".txt",'w') as wr1:
					wr1.write("")
				with open(done_text2+filesave_name+".txt",'w') as wr:
					wr.write("")

			try:
				os.rename(pending_file,done_name)
			except:
				error = traceback.format_exc()
				print (error)
				with open(log+'/'+c_date+'_gstin_start_end_txt','a') as ap:
					ap.write("Error in renaming file "+str(error)+" "+str(datetime.now())+'\n')
				pass

		except:
			err = traceback.format_exc()
			print (err)
			with open(log+'/'+c_date+'_gstin_start_end_txt','a') as ap:
				ap.write("Error in details "+str(err)+" "+str(datetime.now())+'\n')


	with open(log+'/'+c_date+'_gstin_start_end_txt','a') as ap:
		ap.write("End gstin "+str(datetime.now())+'\n')


with open(log+'/'+c_date+'_start_end_txt','a') as ap:
	ap.write("Start "+str(datetime.now())+'\n')

input_folder = "/DriveD/GST/main_page/"
# input_folder = "/gstshare/sss/"
input_files = os.listdir(input_folder)
file_data = [input_folder+x for x in input_files if "_main.json" in x]
print (len(file_data))
# exit()
# file_data = [x.strip() for x in file_data if "_done.json" not in x]
# file_data = [x.strip() for x in file_data if "_main_no_records" not in x]
# file_data = [x.strip() for x in file_data if "_main_read_pending.json" not in x]
# print (len(file_data))

# for value in file_data:
# 	MainFunctionCall(value)

pool = mp.Pool(processes=3)
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
