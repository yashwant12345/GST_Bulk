import os
import json
import pdb
import traceback
# import pymssql
from datetime import datetime
import pandas as pd
import requests
import shutil
import time

c_date = str(datetime.now()).split(" ")[0]

upload_log = "/DriveD/gst/log/"+str(datetime.now()).split(' ')[0]
if not os.path.exists(upload_log):
	os.makedirs(upload_log)
log = "/DriveD/gst/log"
if not os.path.exists(log):
	os.makedirs(log)

read_done = "/DriveD/GST/Read_Done"
if not os.path.exists(read_done):
	os.makedirs(read_done)

with open(log+'/'+c_date+'_read_start_end_txt','a') as ap:
	ap.write("Start "+str(datetime.now())+'\n')

try:
	df1 = pd.DataFrame()
	df2 = pd.DataFrame()
	df3 = pd.DataFrame()
	df4 = pd.DataFrame()
	df5 = pd.DataFrame()

	CsvFileSave = "/DriveD/output"
	if not os.path.exists(CsvFileSave):
		os.makedirs(CsvFileSave)

	csv_name = CsvFileSave+"/main_page_"+str(datetime.now()).replace(":","_").replace(" ","_").replace(".","_").replace("-","_")+"_New.csv"
	print (csv_name)

	# # main page read ==============================================

	# state_code_dict = {"35":"Andaman and Nicobar Islands","37":"Andhra Pradesh","12":"Arunachal Pradesh","18":"Assam","10":"Bihar","04":"Chandigarh","22":"Chhattisgarh","26":"Dadra and Nagar Haveli and Daman and Diu","25":"Daman and Diu","07":"Delhi","30":"Goa","24":"Gujarat","06":"Haryana","02":"Himachal Pradesh","01":"Jammu and Kashmir","20":"Jharkhand","29":"Karnataka","32":"Kerala","38":"Ladakh","31":"Lakshadweep","23":"Madhya Pradesh","27":"Maharashtra","14":"Manipur","17":"Meghalaya","15":"Mizoram","13":"Nagaland","21":"Odisha","97":"Other Territory","34":"Puducherry","03":"Punjab","08":"Rajasthan","11":"Sikkim","33":"Tamil Nadu","36":"Telangana","16":"Tripura","09":"Uttar Pradesh","05":"Uttarakhand","19":"West Bengal"}
	folder = "/gstshare/main_page/"

	listfiles = os.listdir(folder)
	listfiles = [folder+x for x in listfiles if "_done.json" in x]
	print (len(listfiles))
	# exit()
	
	count = 0

	for file in listfiles:
		print (file)
		count = count+1
		print (count)
		if os.path.exists(file):
			pan = file.split('/')[-1].split("_")[0]

			cin = file.split('/')[-1].split("_")[1]

			state_code_dict = {"35":"Andaman and Nicobar Islands","37":"Andhra Pradesh","12":"Arunachal Pradesh","18":"Assam","10":"Bihar","04":"Chandigarh","22":"Chhattisgarh","26":"Dadra and Nagar Haveli and Daman and Diu","25":"Daman and Diu","07":"Delhi","30":"Goa","24":"Gujarat","06":"Haryana","02":"Himachal Pradesh","01":"Jammu and Kashmir","20":"Jharkhand","29":"Karnataka","32":"Kerala","38":"Ladakh","31":"Lakshadweep","23":"Madhya Pradesh","27":"Maharashtra","14":"Manipur","17":"Meghalaya","15":"Mizoram","13":"Nagaland","21":"Odisha","97":"Other Territory","34":"Puducherry","03":"Punjab","08":"Rajasthan","11":"Sikkim","33":"Tamil Nadu","36":"Telangana","16":"Tripura","09":"Uttar Pradesh","05":"Uttarakhand","19":"West Bengal"}

			with open(file,'r') as rd:
				file_data = rd.read()

			pending_file = file.replace("_done.json","_read_pending.json")

			try:
				os.rename(file,pending_file)
			except:
				os.remove(pending_file)
				os.rename(file,pending_file)

			json_data = json.loads(file_data)

			gstins_data = json_data["gstinResList"]

			for gstins_row in gstins_data:

				# main_dict["Csv_Type"] = "GST Main"

				pan = file.split('/')[-1].replace(".json","").split("_")[0]
				# main_dict["PAN"] = pan

				# cin = file.split('/')[-1].replace(".json","").split("_")[-1]
				# main_dict["CIN"] = cin

				gstin = gstins_row["gstin"]
				# main_dict["GSTIN"] = gstin

				gstin_status = gstins_row["authStatus"]
				# main_dict["GSTIN_Status"] = gstin_status

				gstin_state_code = gstins_row["stateCd"]
				# main_dict["GSTIN_State_Code"] = gstin_state_code

				State = state_code_dict[gstin_state_code]
				# main_dict["State"] = State

				main_dict = {"Csv_Type":"GST Main","PAN":pan,"CIN":cin,"GSTIN":gstin,"GSTIN_Status":gstin_status,"GSTIN_State_Code":gstin_state_code,"State":State}
				df1 = df1.append(main_dict,ignore_index=True)


			done_file = pending_file.replace("_read_pending.json","_read_done.json")

			try:
				os.rename(pending_file,done_file)
			except:
				os.remove(done_file)
				os.rename(pending_file,done_file)

	# df1 = df1.append(main_dict,ignore_index=True)
	# df1.replace('~','-', inplace=True, limit=None, regex=True)
	df1 = df1[["Csv_Type","CIN","PAN","GSTIN","GSTIN_Status","GSTIN_State_Code","State"]]
	df1.to_csv(csv_name,sep='~',line_terminator='|',encoding='utf-8',mode = 'a')


	time.sleep(2)

	if os.path.exists(csv_name):
		files = {}

		uploaded_path = "/DriveD/gst/output_uploaded/"
		if not os.path.exists(uploaded_path):
			os.makedirs(uploaded_path)
			
		url = r"http://ec2-13-228-179-100.ap-southeast-1.compute.amazonaws.com/uploader.aspx?dir=F:\\GST Bulk"

		destination_file = csv_name.split('/')[-1]

		destination_csv = "/DriveD/gst/outputs/"+destination_file

		with open(csv_name, 'rb') as rd:
			files[str(destination_file)] = rd.read()

		try:
			# if os.path.exists(destination_csv):
			# 	os.remove(destination_csv)

			r = requests.post(url, files=files)
			print (r.text)

			if "Successful" in r.text and r.status_code == 200:
				print ("file uploaded")

				with open(upload_log+'/success.txt','a') as ap:
					ap.write('Running code '+csv_name+' uploaded at '+str(datetime.now())+'\n')

				# try:
				shutil.move(csv_name,uploaded_path)
				# except:
				# 	os.remove(csv_name.replace("outputs","output_uploaded"))
				# 	shutil.move(csv_name,uploaded_path)

		except:
			error = traceback.format_exc()
			print (error)
			
			with open(upload_log+'/error2.txt','a') as ap:
				ap.write(str(error)+' '+csv_name+' '+str(datetime.now())+'\n')
			pass

except:
	err = traceback.format_exc()
	print (err)
	with open(log+'/'+c_date+'_read_start_end_txt','a') as ap:
		ap.write("Error in read "+str(err)+" "+str(datetime.now())+'\n')

with open(log+'/'+c_date+'_read_start_end_txt','a') as ap:
	ap.write("End "+str(datetime.now())+'\n')




# readfunction("/DriveD/gst/main_page/AAACR7637P","L60300MH1988PLC049019","2c8d3fa2-2b11-4629-81f8-d5aef49d7ed6")