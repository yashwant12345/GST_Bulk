import os
import pymssql
import pandas as pd
from datetime import datetime
import os.path, time

folder = "/DriveE/main_page_2/"
# folder = "/DriveD/GST/main_page/"
listfiles = os.listdir(folder)
listfiles = [folder+x for x in listfiles]

masterdf = pd.DataFrame()

count=0
# for file in listfiles:
# 	count+=1
# 	print (count,len(listfiles))
# 	folderdate = datetime.fromtimestamp(os.path.getmtime(file))
# 	folderdate_only = str(folderdate).split(" ")[0]

# 	with open("/DriveD/additional_codes/file_with_datetime_2.txt",'a') as ap:
# 		ap.write(file+"****"+str(folderdate)+"\n")

# 	with open("/DriveD/additional_codes/file_with_date_only_2.txt",'a') as ap:
# 		ap.write(file+"****"+str(folderdate_only)+"\n")

with open("/DriveD/additional_codes/file_with_date_only_2.txt",'r') as rd:
	date_data = rd.readlines()

date_data = [x.split("****")[-1].strip() for x in date_data]
# print (len(date_data))
distinct_date_data = sorted(list(set(date_data)))[:-1]

df = pd.DataFrame(date_data,columns=["date"])
# print (distinct_date_data)
# print (len(distinct_date_data))
# print (date_data[:10])
count_list = []
for distinct_date in distinct_date_data:

	df_date = df[df["date"]==distinct_date]
	# print (distinct_date)
	# print (len(df_date))

	count_list.append(len(df_date))

	dict_ = {"ServerName":"GST L1b","date":distinct_date,"GST L1b Count":str(len(df_date))}

	masterdf = masterdf.append(dict_,ignore_index=True)

total_count = sum(count_list)

masterdf["GST L1b Total Count"] = str(total_count)
masterdf = masterdf[["ServerName","date","GST L1b Count","GST L1b Total Count"]]

masterdf.to_csv("/DriveD/additional_codes/output/gst_l1b.csv",index=False)