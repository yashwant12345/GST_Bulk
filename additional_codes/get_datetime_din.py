import os
import pandas as pd
from datetime import datetime,timedelta
import os.path, time
import traceback
import requests
import pdb


p_date = str(datetime.now()-timedelta(days=1)).split(" ")[0]

c_date = str(datetime.now()).split(" ")[0]

# c_date = "2022-01-21"

# if os.path.exists("/DriveD/additional_codes/file_with_datetime_din.txt"):
# 	os.remove("/DriveD/additional_codes/file_with_datetime_din.txt")

# if os.path.exists("/DriveD/additional_codes/file_with_date_only_din.txt"):
# 	os.remove("/DriveD/additional_codes/file_with_date_only_din.txt")


with open("/DriveD/additional_codes/file_with_date_only_din.txt",'r') as rd:
	skip_list = rd.readlines()

skip_list = [x.split("****")[0].strip() for x in skip_list]

input_folder_2 = "/DriveD/GST/done_files/"

folder_name_2 = sorted(os.listdir(input_folder_2))
folder_name_2 = [input_folder_2+x for x in folder_name_2]

input_folder = "/DriveD/GST/main_page/"

folder_name = sorted(os.listdir(input_folder))
folder_name = [input_folder+x for x in folder_name]

listfiles_data = folder_name+folder_name_2

listfiles = list(set(listfiles_data)-set(skip_list))

masterdf = pd.DataFrame()

count=0
for file in listfiles:
	count+=1
	print (count,len(listfiles))
	try:
		folderdate = datetime.fromtimestamp(os.path.getmtime(file))
		folderdate_only = str(folderdate).split(" ")[0]

		with open("/DriveD/additional_codes/file_with_datetime_din.txt",'a') as ap:
			ap.write(file+"****"+str(folderdate)+"\n")

		with open("/DriveD/additional_codes/file_with_date_only_din.txt",'a') as ap:
			ap.write(file+"****"+str(folderdate_only)+"\n")
	except:
		pass

with open("/DriveD/additional_codes/file_with_date_only_din.txt",'r') as rd:
	date_data = rd.readlines()

date_data = [x.split("****")[-1].strip() for x in date_data]
print (len(date_data))
# pdb.set_trace()
distinct_date_data = sorted(list(set(date_data)))[:-1]

df = pd.DataFrame(date_data,columns=["date"])
# print (distinct_date_data)
# print (len(distinct_date_data))
# print (date_data[:10])
count_list = []
for distinct_date in distinct_date_data:

	# pdb.set_trace()

	df_date = df[df["date"]==distinct_date]
	# print (distinct_date)
	# print (len(df_date))

	count_list.append(len(df_date))

	dict_ = {"ServerName":"GST DIN","date":distinct_date,"GST DIN Count":str(len(df_date))}

	masterdf = masterdf.append(dict_,ignore_index=True)

total_count = sum(count_list)

masterdf["GST DIN Total Count"] = str(total_count)
# pdb.set_trace()
masterdf = masterdf[masterdf["date"]==p_date]
masterdf = masterdf[["ServerName","date","GST DIN Count","GST DIN Total Count"]]
csv_name = "/DriveD/additional_codes/output/gst_din_"+str(c_date)+".csv"

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