import os
import shutil

folder = "/DriveD/GST/detail_page/"

folder_list = os.listdir(folder)
folder_list = [folder+x for x in folder_list]

for folder_name in folder_list:
	print (folder_name)
	# exit()

	file_list = os.listdir(folder_name)
	file_list = [folder_name+"/"+x for x in file_list]
	print (len(file_list))
	# exit()

	if len(file_list) == 0:
		shutil.rmtree(folder_name)
	# else:
	# 	print ("Ignore")

	# for file in file_list:
	# 	print (file)
	# 	# print (len(file))
	# 	exit()