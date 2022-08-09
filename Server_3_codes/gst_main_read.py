import os
import pandas as pd
import json
from datetime import datetime
import shutil
import requests

c_date = str(datetime.now()).split(" ")[0]

upload_log = "/DriveF/gst/log/"+str(datetime.now()).split(' ')[0]
if not os.path.exists(upload_log):
	os.makedirs(upload_log)
log = "/DriveF/gst/log"
if not os.path.exists(log):
	os.makedirs(log)

# read_done = "/DriveF/GST/Read_Done"
read_done = "/DriveF/read_done"
if not os.path.exists(read_done):
	os.makedirs(read_done)


input_folder = "/DriveF/GST/main_page/"

state_code_dict = {"35":"Andaman and Nicobar Islands","37":"Andhra Pradesh","12":"Arunachal Pradesh","18":"Assam","10":"Bihar","04":"Chandigarh","22":"Chhattisgarh","26":"Dadra and Nagar Haveli and Daman and Diu","25":"Daman and Diu","07":"Delhi","30":"Goa","24":"Gujarat","06":"Haryana","02":"Himachal Pradesh","01":"Jammu and Kashmir","20":"Jharkhand","29":"Karnataka","32":"Kerala","38":"Ladakh","31":"Lakshadweep","23":"Madhya Pradesh","27":"Maharashtra","14":"Manipur","17":"Meghalaya","15":"Mizoram","13":"Nagaland","21":"Odisha","97":"Other Territory","34":"Puducherry","03":"Punjab","08":"Rajasthan","11":"Sikkim","33":"Tamil Nadu","36":"Telangana","16":"Tripura","09":"Uttar Pradesh","05":"Uttarakhand","19":"West Bengal"}

listfiles = os.listdir(input_folder)
listfiles = [input_folder+x for x in listfiles][:2000]
print (len(listfiles))

if len(listfiles) == 2000:
	df1 = pd.DataFrame()
	# csv_name = "/DriveF/GST/csv/gst_main.csv"

	CsvFileSave = "/DriveF/GST/outputs"
	if not os.path.exists(CsvFileSave):
		os.makedirs(CsvFileSave)
	csv_name = CsvFileSave+"/"+str(datetime.now()).replace(":","_").replace(" ","_").replace(".","_").replace("-","_")+"_New.csv"

	count = 0
	for file in listfiles:
		count+=1
		print (count)
		print (file)

		try:

			file_download_time = datetime.fromtimestamp(os.path.getmtime(file))

			pan = file.replace("_main_no_records_Done.json","").replace("_main_no_records.json","").replace("_main_Done.json","").replace("_main.json","").split('/')[-1].split("_")[0]

			cin = file.replace("_main_no_records_Done.json","").replace("_main_no_records.json","").replace("_main_Done.json","").replace("_main.json","").split('/')[-1].split("_")[-1]

			if "_main_no_records" not in file:

				with open(file,'r') as rd:
					file_data = rd.read()

				json_data = json.loads(file_data)

				gstins_data = json_data["gstinResList"]

				for gstins_row in gstins_data:

					gstin = gstins_row["gstin"]
					
					gstin_status = gstins_row["authStatus"]

					gstin_state_code = gstins_row["stateCd"]

					State = state_code_dict[gstin_state_code]
					

					main_dict = {"Csv_Type":"GST Main","PAN":pan,"CIN":cin,"GSTIN":gstin,"GSTIN_Status":gstin_status,"GSTIN_State_Code":gstin_state_code,"State":State,"File_Download_Time":str(file_download_time)}
					df1 = df1.append(main_dict,ignore_index=True)
			
			else:
				main_dict = {"Csv_Type":"GST Main","PAN":pan,"CIN":cin,"GSTIN":"","GSTIN_Status":"","GSTIN_State_Code":"","State":"","File_Download_Time":str(file_download_time)}
				df1 = df1.append(main_dict,ignore_index=True)
		except:
			pass

		try:
			shutil.move(file,"/DriveF/GST/done_files")
		except:
			pass


	# df1 = df1.append(main_dict,ignore_index=True)
	# df1.replace('~','-', inplace=True, limit=None, regex=True)
	df1 = df1[["Csv_Type","CIN","PAN","GSTIN","GSTIN_Status","GSTIN_State_Code","State","File_Download_Time"]]
	# df1.to_csv(csv_name,sep='~',line_terminator='|',encoding='utf-8',mode = 'a')
	df1.to_csv(csv_name,index=False)

	uploaded_path = "/DriveF/gst/output_uploaded/"
	if not os.path.exists(uploaded_path):
		os.makedirs(uploaded_path)

	files = {}

	uploaded_path = "/DriveF/gst/output_uploaded/"
	if not os.path.exists(uploaded_path):
		os.makedirs(uploaded_path)
		
	url = 'http://ec2-54-255-94-235.ap-southeast-1.compute.amazonaws.com/file_upload_gst_din'

	destination_file = csv_name.split('/')[-1]

	# destination_csv = "/DriveF/gst/outputs/"+destination_file

	with open(csv_name,'rb') as rd:
		file_data = rd.read()

	try:
		# if os.path.exists(destination_csv):
		# 	os.remove(destination_csv)

		r = requests.post(url, data={'file_data':file_data,'name':destination_file})
		print (r.text)

		if "Success" in r.text and r.status_code == 200:
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