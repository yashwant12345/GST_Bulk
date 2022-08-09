import os





input_folder = "/DriveD/GST/detail_page/"
listfiles = os.listdir(input_folder)
listfiles = [input_folder+x for x in listfiles]

count = 0
for file in listfiles:
	count+=1
	print (count)

	main_file_json = file.replace("/DriveD/GST/detail_page","/gstshare/main_page")+"_main.json"
	

	if os.path.exists(main_file_json):
		print (main_file_json)
		os.rename(main_file_json,main_file_json.replace("_main.json","_main_done.json"))
		# exit()`

	