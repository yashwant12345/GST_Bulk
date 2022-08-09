import os


# # input_folder = "/DriveD/GST/detail_page/"
# # listfiles = os.listdir(input_folder)
# # # listfiles = [input_folder+x for x in listfiles]

# # count=0
# # for file in listfiles:
# # 	count+=1
# # 	print (count)
# # 	with open("/DriveD/GST/folder_list.txt",'a') as ap:
# # 		ap.write(file+"\n")

# file1 = "/DriveD/GST/folder_list.txt"

# with open(file1,'r') as rd:
# 	data1 = rd.readlines()
# 	data1 = [x.strip() for x in data1]


# file2 = "/gstshare/ssss/downloaded_files.txt"

# with open(file2,'r') as rd:
# 	data2 = rd.readlines()
# 	data2 = [x.strip() for x in data2]

# print (len(data1))
# print (len(data2))
# c = list(set(data2)-set(data1))
# # print (c)
# print (len(c))


folder = "/gstshare/main_page/"

listfiles = os.listdir(folder)
listfiles = [folder+x for x in listfiles if "_main_read_done.json" in x]
print (len(listfiles))

count = 0
for file in listfiles:
	# print (file)
	count+=1
	print(count)
	# exit()

	os.rename(file,file.replace("_main_read_done.json","_main.json"))