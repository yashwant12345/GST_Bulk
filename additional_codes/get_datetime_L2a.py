import os
import pandas as pd
from datetime import datetime,timedelta
import os.path, time
import traceback
import requests
import pdb


p_date = str(datetime.now()-timedelta(days=1)).split(" ")[0]

c_date = str(datetime.now()).split(" ")[0]

folder = "/DriveD/GST/detail_page/"
# folder = "/DriveD/GST/main_page/"
folder_list_data = os.listdir(folder)
folder_list_data = [folder+x for x in folder_list_data]

masterdf = pd.DataFrame()

# if os.path.exists("/DriveD/additional_codes/file_with_datetime_L2a.txt"):
# 	os.remove("/DriveD/additional_codes/file_with_datetime_L2a.txt")

# if os.path.exists("/DriveD/additional_codes/file_with_date_only_L2a.txt"):
# 	os.remove("/DriveD/additional_codes/file_with_date_only_L2a.txt")

with open("/DriveD/additional_codes/file_with_date_only_L2a.txt",'r') as rd:
	skip_list = rd.readlines()

skip_list = ["/".join(x.split("/")[:5]).strip() for x in skip_list]

folder_list = list(set(folder_list_data)-set(skip_list))

count=0
for folder in folder_list:
	count+=1
	print (count,len(folder_list))

	listfiles = os.listdir(folder)
	listfiles = [folder+"/"+x for x in listfiles]
	if len(listfiles) !=0:
		listfiles = [x for x in listfiles if "_main_detail.json" in x][:1]
		try:
		
			for file in listfiles:
				folderdate = datetime.fromtimestamp(os.path.getmtime(file))
				folderdate_only = str(folderdate).split(" ")[0]

				with open("/DriveD/additional_codes/file_with_datetime_L2a.txt",'a') as ap:
					ap.write(file+"****"+str(folderdate)+"\n")

				with open("/DriveD/additional_codes/file_with_date_only_L2a.txt",'a') as ap:
					ap.write(file+"****"+str(folderdate_only)+"\n")
		except:
			pass

with open("/DriveD/additional_codes/file_with_date_only_L2a.txt",'r') as rd:
	date_data = rd.readlines()

date_data = [x.split("****")[-1].strip() for x in date_data]
# print (len(date_data))
distinct_date_data = sorted(list(set(date_data)))[:-1]

df = pd.DataFrame(date_data,columns=["date"])
# print (distinct_date_data)
# print (len(distinct_date_data))
# print (date_data[:10])
count_list = []
# distinct_date_data = ["2022-01-29"]
for distinct_date in distinct_date_data:

	df_date = df[df["date"]==distinct_date]
	# print (distinct_date)
	# print (len(df_date))

	count_list.append(len(df_date))

	dict_ = {"ServerName":"GST L2a","date":distinct_date,"GST L2a Count":str(len(df_date))}

	masterdf = masterdf.append(dict_,ignore_index=True)

total_count = sum(count_list)

masterdf["GST L2a Total Count"] = str(total_count)
masterdf = masterdf[masterdf["date"]==p_date]
masterdf = masterdf[["ServerName","date","GST L2a Count","GST L2a Total Count"]]

csv_name = "/DriveD/additional_codes/output/gst_l2a_"+str(c_date)+"_New.csv"

masterdf.to_csv(csv_name,index=False)

files = {}

uploaded_path = "/DriveD/gst/output_uploaded/"
if not os.path.exists(uploaded_path):
	os.makedirs(uploaded_path)
	
url = 'http://ec2-54-255-94-235.ap-southeast-1.compute.amazonaws.com/file_upload_gst_summary'

destination_file = csv_name.split('/')[-1]

# destination_csv = "/DriveD/gst/outputs/"+destination_file

with open(csv_name,'rb') as rd:
	file_data = rd.read()

try:
	# if os.path.exists(destination_csv):
	# 	os.remove(destination_csv)

	r = requests.post(url, data={'file_data':file_data,'name':destination_file})
	print (r.text)

	if "Success" in r.text and r.status_code == 200:
		print ("file uploaded")

		# with open(upload_log+'/success.txt','a') as ap:
		# 	ap.write('Running code '+csv_name+' uploaded at '+str(datetime.now())+'\n')

		# try:
		# shutil.move(csv_name,uploaded_path)
		# except:
		# 	os.remove(csv_name.replace("outputs","output_uploaded"))
		# 	shutil.move(csv_name,uploaded_path)

except:
	error = traceback.format_exc()
	print (error)