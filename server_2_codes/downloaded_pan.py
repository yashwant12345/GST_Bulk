import os


folder = "/DriveD/GST/detail_page/"

listfiles = os.listdir(folder)
# print (len(listfiles))

count=0
for file in listfiles:
	count+=1
	print (count)
	with open("/DriveD/GST/pan_cin_list.txt",'a') as wr:
		wr.write(file+"\n")