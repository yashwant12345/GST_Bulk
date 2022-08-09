import os


input_folder = "/gstshare/main_page/"

listfiles = os.listdir(input_folder)
listfiles = [input_folder+x for x in listfiles if "_main_read_done.json" in x]
print (len(listfiles))
# exit()
count = 0
for file in listfiles:
	count+=1
	print (count)

	os.rename(file,file.replace('_main_read_done.json',"_main_done.json"))

