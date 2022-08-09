import os
from datetime import datetime
import smtplib
import pandas as pd
import requests
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase
import traceback
DT = str(datetime.now()).split(' ')[0]

DocsDaily_hour_count_log = "/DriveD/Log/"
if not os.path.exists(DocsDaily_hour_count_log):
	os.makedirs(DocsDaily_hour_count_log)

def sendmail(msg_body):
	fromaddr = "yashwant@saverisk.com"
	toaddr = "yashwant@saverisk.com"
	   
	# instance of MIMEMultipart 
	msg = MIMEMultipart() 
	  
	# storing the senders email address   
	msg['From'] = fromaddr 
	  
	# storing the receivers email address  
	msg['To'] = toaddr 
	  
	# storing the subject  
	msg['Subject'] = "GST Level 1 hourly count."
	  
	# string to store the body of the mail 
	body = str(msg_body)
	  
	# attach the body with the msg instance 
	msg.attach(MIMEText(body, 'plain')) 

	# creates SMTP session 
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	  
	# start TLS for security 
	s.starttls() 
	  
	# Authentication 
	s.login(fromaddr, "yashwant@1991") 
	  
	# Converts the Multipart msg into a string 
	text = msg.as_string() 
	  
	# sending the mail 
	s.sendmail(fromaddr, toaddr, text) 
	  
	# terminating the session
	s.quit() 
	print ("mail sent")

df = pd.DataFrame()

try:
	with open(DocsDaily_hour_count_log+DT+'_start_end_log.txt','a') as apd:
		apd.write("Start time "+str(datetime.now())+'\n')
	with open("/DriveD/count_file.txt",'r') as rd:
		last_count_detail = rd.read()

	input_folder = "/DriveD/GST/main_page/"

	folder_name = sorted(os.listdir(input_folder))
	folder_name = [input_folder+x for x in folder_name]

	total_count = len(folder_name)

	last_count = last_count_detail

	hour_count =int(total_count) - int(last_count.strip())
	
	
	invalid_error_count = ""
	error_count = ""
	invalid_error_count = ""
	overall_count = ""

	df = df.append({"Process Name":"GST Server L1","Folder Name":"","Send Count":str(hour_count),'Error Count':"",'Invalid Error Count':"",'Total Count':str(total_count),"Start Time":"","End Time":"","TimeDelta":""},ignore_index=True)

	df = df[["Process Name","Folder Name","Send Count","Error Count","Invalid Error Count","Total Count","Start Time","End Time","TimeDelta"]]

	df = df.to_json(orient="records")

	req = requests.post('http://3.101.1.85',data={'countdata':df}).content
	
	msg_body = str(df)
	
	with open("/DriveD/count_file.txt",'w') as wr:
		wr.write(str(total_count))

	# sendmail(msg_body)

	with open(DocsDaily_hour_count_log+DT+'_start_end_log.txt','a') as apd:
		apd.write("End time "+str(datetime.now())+'\n')

except Exception as err:
	# print err
	trace = traceback.format_exc()
	print (trace)
	msg_body = "Error occured while running houly count"
	# sendmail(msg_body)
	with open(DocsDaily_hour_count_log+DT+'_start_end_log.txt','a') as apd:
		apd.write("Error "+str(err)+'|'+str(datetime.now())+'\n')
