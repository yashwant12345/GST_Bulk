import os
import pandas as pd
import json
from datetime import datetime



input_folder = "/DriveD/GST/main_page/"

state_code_dict = {"35":"Andaman and Nicobar Islands","37":"Andhra Pradesh","12":"Arunachal Pradesh","18":"Assam","10":"Bihar","04":"Chandigarh","22":"Chhattisgarh","26":"Dadra and Nagar Haveli and Daman and Diu","25":"Daman and Diu","07":"Delhi","30":"Goa","24":"Gujarat","06":"Haryana","02":"Himachal Pradesh","01":"Jammu and Kashmir","20":"Jharkhand","29":"Karnataka","32":"Kerala","38":"Ladakh","31":"Lakshadweep","23":"Madhya Pradesh","27":"Maharashtra","14":"Manipur","17":"Meghalaya","15":"Mizoram","13":"Nagaland","21":"Odisha","97":"Other Territory","34":"Puducherry","03":"Punjab","08":"Rajasthan","11":"Sikkim","33":"Tamil Nadu","36":"Telangana","16":"Tripura","09":"Uttar Pradesh","05":"Uttarakhand","19":"West Bengal"}

listfiles = os.listdir(input_folder)
listfiles = [input_folder+x for x in listfiles]
print (len(listfiles))

df1 = pd.DataFrame()
csv_name = "/DriveD/GST/csv/gst_main.csv"

count = 0
for file in listfiles:
	count+=1
	print (count)
	print (file)

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


# df1 = df1.append(main_dict,ignore_index=True)
# df1.replace('~','-', inplace=True, limit=None, regex=True)
df1 = df1[["Csv_Type","CIN","PAN","GSTIN","GSTIN_Status","GSTIN_State_Code","State","File_Download_Time"]]
# df1.to_csv(csv_name,sep='~',line_terminator='|',encoding='utf-8',mode = 'a')
df1.to_csv(csv_name,index=False)

	# exit()