import os


# input_folder = "/gstshare/main_page/"

# listfiles = os.listdir(input_folder)
# listfiles = [input_folder+x for x in listfiles]
# print (len(listfiles))
# count = 0
# for file in listfiles:
# 	count+=1
# 	print (count)
# 	with open("/home/ubuntu/Desktop/list.txt",'a') as ap:
# 		ap.write(file+"\n")


input_folder = "/DriveD/GST/done_text/"

listfolders = os.listdir(input_folder)
listfolders = [input_folder+x for x in listfolders]
listfolders = list(set(["_".join(x.split("_")[:3]) for x in listfolders]))
# print (listfolders)
# exit()

count = 0
for file in listfolders:
	print (file)
	count+=1
	print (count)

	pan_cin = file.split("/")[-1].replace(".txt","")
	# print (pan_cin)
	# exit()

	with open("/DriveD/GST/done_pan/"+pan_cin+".txt",'w') as wr:
		wr.write("")


	# exit()