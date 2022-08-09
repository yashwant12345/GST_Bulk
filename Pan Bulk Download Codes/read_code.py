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

def readfunction(folder,cin,reqid):
	upload_log = "/DriveD/gst/log/"+str(datetime.now()).split(' ')[0]
	if not os.path.exists(upload_log):
		os.makedirs(upload_log)
	log = "/DriveD/gst/log"
	if not os.path.exists(log):
		os.makedirs(log)

	with open(log+'/'+c_date+'_read_start_end_txt','a') as ap:
		ap.write("Start "+str(datetime.now())+'\n')

	try:
		df1 = pd.DataFrame()
		df2 = pd.DataFrame()
		df3 = pd.DataFrame()
		df4 = pd.DataFrame()
		df5 = pd.DataFrame()


		CsvFileSave = "/DriveD/gst/outputs"
		if not os.path.exists(CsvFileSave):
			os.makedirs(CsvFileSave)

		csv_name = CsvFileSave+"/"+reqid+"_New.csv"
		print (csv_name)

		# main page read ==============================================

		state_code_dict = {"35":"Andaman and Nicobar Islands","37":"Andhra Pradesh","12":"Arunachal Pradesh","18":"Assam","10":"Bihar","04":"Chandigarh","22":"Chhattisgarh","26":"Dadra and Nagar Haveli and Daman and Diu","25":"Daman and Diu","07":"Delhi","30":"Goa","24":"Gujarat","06":"Haryana","02":"Himachal Pradesh","01":"Jammu and Kashmir","20":"Jharkhand","29":"Karnataka","32":"Kerala","38":"Ladakh","31":"Lakshadweep","23":"Madhya Pradesh","27":"Maharashtra","14":"Manipur","17":"Meghalaya","15":"Mizoram","13":"Nagaland","21":"Odisha","97":"Other Territory","34":"Puducherry","03":"Punjab","08":"Rajasthan","11":"Sikkim","33":"Tamil Nadu","36":"Telangana","16":"Tripura","09":"Uttar Pradesh","05":"Uttarakhand","19":"West Bengal"}
		# folder = "/DriveF/GST Code/main_page/"

		listfiles = os.listdir(folder)
		listfiles = [folder+"/"+x for x in listfiles if "_main.json" in x]

		file = listfiles[0]
		print (file)

		with open(file,'r') as rd:
			file_data = rd.read()

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

		# df1 = df1.append(main_dict,ignore_index=True)
		# df1.replace('~','-', inplace=True, limit=None, regex=True)
		df1 = df1[["Csv_Type","CIN","PAN","GSTIN","GSTIN_Status","GSTIN_State_Code","State"]]
		df1.to_csv(csv_name,sep='~',line_terminator='|',encoding='utf-8',mode = 'a')

		# # =======================================================================

		# # Details page read =====================================================

		df2 = pd.DataFrame()
		listfiles = os.listdir(folder)
		listfiles = [folder+"/"+x for x in listfiles if "_main_detail.json" in x]
		for file in listfiles:
			print ("file",file)
			
			with open(file,'r') as rd:
				file_data = rd.read()

			json_data = json.loads(file_data)
			# print json_data

			gstin_no = file.split("/")[-1].split("_")[0].replace(".json","")
			print (gstin_no)

			try:
				legal_bussiness_name = json_data["lgnm"]
			except:
				legal_bussiness_name = ''
			
			try:
				trade_name = json_data["tradeNam"]
			except:
				trade_name = ''

			try:
				regist_date = json_data["rgdt"]
			except:
				regist_date = ''

			try:
				consti_busns = json_data["ctb"]
			except:
				consti_busns

			try:
				gstin_status = json_data["sts"]
			except:
				gstin_status = ''

			try:
				taxpayer_type = json_data["dty"]
			except:
				taxpayer_type = ''

			try:
				admin_office = json_data["ctj"]
			except:
				admin_office = ''

			try:
				other_office = json_data["stj"]
			except:
				other_office = ''

			try:
				principal_place_business = json_data["pradr"]["adr"]
			except:
				principal_place_business = ''

			try:
				business_nature = json_data["nba"]
				business_nature = ",".join(business_nature)
			except:
				business_nature = ''

			detail_main_dict = {"Csv_Type":"GST Detail Main","GSTIN":gstin_no,"Legal Name of Business":legal_bussiness_name,"Trade Name":trade_name,"Effective Date of registration":regist_date,"Constitution of Business":consti_busns,"GSTIN_UIN Status":gstin_status,"Taxpayer Type":taxpayer_type,"Administrative Office":admin_office,"Other Office":other_office,"Principal Place of Business":principal_place_business,"Nature of Business Activities":business_nature}
			df2 = df2.append(detail_main_dict,ignore_index=True)

		# df1 = df1.append(detail_main_dict,ignore_index=True)
		# df1.replace('~','-', inplace=True, limit=None, regex=True)
		df2 = df2[["Csv_Type","GSTIN","Legal Name of Business","Trade Name","Effective Date of registration","Constitution of Business","GSTIN_UIN Status","Taxpayer Type","Administrative Office","Other Office","Principal Place of Business","Nature of Business Activities"]]
		df2.to_csv(csv_name,sep='~',line_terminator='|',encoding='utf-8',mode = 'a')

		# Details goods and services =======================================================

		listfiles = os.listdir(folder)
		listfiles = [folder+"/"+x for x in listfiles if "_Goods_services.json" in x]
		for file in listfiles:
			with open(file,'r') as rd:
				file_data = rd.read()

			json_data = json.loads(file_data)
			# print json_data

			gstin_no = file.split("/")[-1].split("_")[0].replace(".json","")
			# print gstin_no

			if "No records found" not in str(json_data):
				print (file)
				# print json_data

				gstin_no = file.split("/")[-1].split("_")[0]

				try:
				
					BA_data = json_data["bzsdtls"]
					
					for ba_dat in BA_data:
					
						try:
							HSN = ba_dat["saccd"]
						except:
							HSN = ''

						try:
							description = ba_dat["sdes"]
						except:
							description = ''

						Type = "Services"

						services_main_dict = {"Csv_Type":"Details_goods_services","GSTIN":gstin_no,"Type":"Services","HSN":HSN,"Description":description}
						df3 = df3.append(services_main_dict,ignore_index=True)
				except:
					BA_data = json_data["bzgddtls"]

					for ba_dat in BA_data:
						# print ba_dat

						try:
							HSN = ba_dat["hsncd"]
						except:
							HSN = ''

						try:
							description = ba_dat["gdes"]
						except:
							description = ''

						Type = "Goods"

						goods_main_dict = {"Csv_Type":"Details_goods_services","GSTIN":gstin_no,"Type":"Goods","HSN":HSN,"Description":description}
						df4 = df4.append(goods_main_dict,ignore_index=True)

		if not df3.empty:

			df3 = df3[["Csv_Type","GSTIN","Type","HSN","Description"]]
			df3.to_csv(csv_name,sep='~',line_terminator='|',encoding='utf-8',mode = 'a')

		if not df4.empty:

			df4 = df4[["Csv_Type","GSTIN","Type","HSN","Description"]]
			df4.to_csv(csv_name,sep='~',line_terminator='|',encoding='utf-8',mode = 'a')

		listfiles = os.listdir(folder)
		listfiles = [folder+"/"+x for x in listfiles if "_filing_details.json" in x]
		for file in listfiles:
			print (file)
			with open(file,'r') as rd:
				file_data = rd.read()

			json_data = json.loads(file_data)

			gstin_no = file.split("/")[-1].split("_")[0].replace(".json","")

			try:

				FD_data = json_data["filingStatus"]
				for fd_dat in FD_data:
					for fd in fd_dat:
						# print fd
						try:
							filing_type = fd["rtntype"]
						except:
							filing_type = ''

						try:
							financial_year = fd["fy"]
						except:
							financial_year = ''
						# print financial_year

						try:
							tax_period = fd["taxp"]
						except:
							tax_period = ''
						# print tax_period

						try:
							date_of_filing = fd["dof"]
						except:
							date_of_filing = ''
						# print date_of_filing

						try:
							status = fd["status"]
						except:
							status = ''
						# print filing_type

						filing_details_dict = {"Csv_Type":"Filing details","GSTIN":gstin_no,"Filing Type":"filing_type","Financial Year":financial_year,"Tax Period":tax_period,"Date of Filing":date_of_filing,"Status":status}
						df5 = df5.append(filing_details_dict,ignore_index=True)
			
			except:
				pass

		df5 = df5[["Csv_Type","GSTIN","Filing Type","Financial Year","Tax Period","Date of Filing","Status"]]
		df5.to_csv(csv_name,sep='~',line_terminator='|',encoding='utf-8',mode = 'a')

		time.sleep(5)

		files = {}

		uploaded_path = "/DriveD/gst/output_uploaded/"
		if not os.path.exists(uploaded_path):
			os.makedirs(uploaded_path)
			
		url = r"http://ec2-52-220-0-175.ap-southeast-1.compute.amazonaws.com/uploader.aspx?dir=L:\MCA\MCA Csv Output\GST Update"

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