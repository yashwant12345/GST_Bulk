import os
import shutil

inputs = "/DriveD/GST/done_pan/"

listfiles = os.listdir(inputs)

listfiles = [inputs+x for x in listfiles]
# print (listfiles[:2])

check_list_path = "/home/ubuntu/Downloads/pan_done.txt"
with open(check_list_path,'r') as rd:
	check_list = rd.readlines()
	check_list = [x.strip() for x in check_list]

count=0
for pan in check_list:
	count+=1
	print (count)

	for file in listfiles:
		# print (file)
		dest = file.replace("/DriveD/GST/done_pan","/DriveD/GST/Read_Done")
		if pan in file:
			try:
				shutil.move(file,"/DriveD/GST/Read_Done")
			except:
				try:
					print (dest)
					os.remove(dest)
					shutil.move(file,"/DriveD/GST/Read_Done")
				except:
					with open("/DriveD/existing.txt",'a') as wr:
						wr.write(file+"\n")
					pass

				# shutil.move(file,"/DriveD/GST/Exists")
