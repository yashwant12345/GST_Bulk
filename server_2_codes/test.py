import random
import time
import os
import pandas as pd

file = "/gstshare/main_page/AACCF8580F_U40106HR2016FTC064931_main_read_pending.json"
df = pd.read_json(file)
print (df)

# # folder = "/gstshare/main_page/"

# # listfiles = os.listdir(folder)
# # listfiles = [folder+x for x in listfiles]

# # with open("/DriveD/lists.txt",'w') as wr:
# # 	wr.write(str(listfiles))

# folder = "/DriveD/GST/detail_page/"

# listfiles = os.listdir(folder)
# listfiles = [folder+x for x in listfiles]
# print (len(listfiles))
# # with open("/DriveD/lists.txt",'w') as wr:
# # 	wr.write(str(listfiles))

# # for file in listfiles:
# # 	print (file)
# # 	cin_pan = file.split("/")[-1]
# # 	with open("/DriveD/GST/done_pan/"+cin_pan+".txt",'w') as wr:
# # 		wr.write("")
# # 	# exit()

# file1 = "/DriveD/GST/folder_list.txt"

# with open(file1,'r') as rd:
# 	list1 = rd.readlines()
# 	list1 = [x.strip() for x in list1]
# 	print (len(list1))

# file2 = "/DriveD/GST/downloaded_files.txt"

# with open(file2,'r') as rd:
# 	list2 = rd.readlines()
# 	list2 = [x.strip() for x in list2]
# 	print (len(list2))

# result = list(set(list1).intersection(list2))
# print (len(result))

# for res in result:

# 	with open("/DriveD/GST/common_pan.txt",'a') as ap:
# 		ap.write(res+"\n")


# file = "/DriveD/pan_unique.txt"
# with open(file,'r') as rd:
# 	list1 = rd.readlines()
# 	list1 = [x.strip() for x in list1]
# 	print (len(list1))
# # print (list1[:2])

# folder = "/DriveD/GST/detail_page/"

# listfiles = os.listdir(folder)
# listfiles = [folder+x for x in listfiles]
# # print (listfiles[:2])

# for txt in listfiles:
# 	# print (txt)
# 	name = txt.replace("/DriveD/GST/detail_page/","")+".txt"
# 	# print (name)
# 	# exit() 
# 	pan = txt.split("/")[-1].split("_")[0]
# 	cin = txt.split("/")[-1].split("_")[-1]
# 	cin_pan = cin+"|"+pan

# 	if not cin_pan in str(list1):
# 		with open("/DriveD/GST/done_text_main/"+name,'w') as wr:
# 			wr.write("")