import os
import pymssql
import pandas as pd
from datetime import datetime
import os.path, time

# folder = "/DriveE/main_page_2/"
folder = "/DriveD/GST/main_page/"
listfiles = os.listdir(folder)
listfiles = [folder+x for x in listfiles]

with open("/DriveD/GST/level_1_only_done.txt",'r') as rd:
	done_list = rd.readlines()

done_list = [x.strip() for x in done_list]

final_result = list(set(listfiles)-set(done_list))
print (len(final_result))

serverip = "ec2-54-255-94-235.ap-southeast-1.compute.amazonaws.com"

print ("Connection Start")
conn = pymssql.connect(server=serverip,user='sa', password="Spot@2017",database='gst_data')
cursor = conn.cursor(as_dict=True)
print ("Connection done")
# exit()
# query = "exec fetch_database_tables"
# cursor.execute(query)

count=0
for file in final_result:
	count+=1
	print (count,len(final_result))
	print (file)
	pan_a = file.split("/")[-1].split("_")[0]
	cin_b = file.split("/")[-1].split("_")[1]

	pan_cin = str(pan_a)+"_"+str(cin_b)

	if pan_cin not in str(done_list):
		
		if len(pan_a) == 10:
			pan = pan_a
			cin = cin_b
		else:
			pan = cin_b
			cin = pan_a
		try:

			# folderdate = datetime.fromtimestamp(os.path.getmtime(file))

			if "_main_no_records.json" in file:

				gstin="NA"

				query = "insert into GST_Level_1_Only ([PAN], [CIN], [GSTIN], [DateTime]) VALUES ("+"'"+str(pan)+"',"+"'"+str(cin)+"',"+"'"+str(gstin)+"',"+"'"+str(datetime.now())+"')"
				cursor.execute(query)
				conn.commit()
				with open("/DriveD/GST/level_1_only_done.txt",'a') as ap:
					ap.write(file+"\n")
			else:
				try:
					df = pd.read_json(file)
					for gstinlist in df["gstinResList"]:
						gstin = gstinlist["gstin"]
						query = "insert into GST_Level_1_Only ([PAN], [CIN], [GSTIN], [DateTime]) VALUES ("+"'"+str(pan)+"',"+"'"+str(cin)+"',"+"'"+str(gstin)+"',"+"'"+str(datetime.now())+"')"
						cursor.execute(query)
						conn.commit()
				except:
					rename_file = "_".join(file.split("_")[:3])+"_main_no_records.json"
					os.rename(file,rename_file)
					gstin = "NA"
					query = "insert into GST_Level_1_Only ([PAN], [CIN], [GSTIN], [DateTime]) VALUES ("+"'"+str(pan)+"',"+"'"+str(cin)+"',"+"'"+str(gstin)+"',"+"'"+str(datetime.now())+"')"
					cursor.execute(query)
					conn.commit()
				with open("/DriveD/GST/level_1_only_done.txt",'a') as ap:
					ap.write(file+"\n")
		except:
			pass