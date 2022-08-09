from datetime import datetime, timedelta,date
import glob2
import os
import os.path, time    
import shutil

dt1=datetime.now()-timedelta(days=2)

rootfolder = '/DriveU/GST Code/main_page/'
# folderlist = os.listdir(rootfolder)
# folderlist = [rootfolder+x for x in folderlist]
folderlist = glob2.glob(rootfolder+'/**/*')
for path in folderlist:
	# if "Done.csv" in path or "Done.txt" in path or "Error.csv" in path:
	if os.path.isfile(path):

		folderdate = datetime.fromtimestamp(os.path.getmtime(path))

		if folderdate<dt1:
			print"xxxx",path, folderdate
			
			os.system('sudo chmod -R ugo+rwx '+'"'+path+'"')

			os.remove(path)

rootfolder = '/DriveU/GST Code/details/'
# folderlist = os.listdir(rootfolder)
# folderlist = [rootfolder+x for x in folderlist]
folderlist = glob2.glob(rootfolder+'/**/*')
for path in folderlist:
	# if "Done.csv" in path or "Done.txt" in path or "Error.csv" in path:
	if os.path.isfile(path):

		folderdate = datetime.fromtimestamp(os.path.getmtime(path))

		if folderdate<dt1:
			print"xxxx",path, folderdate
			
			os.system('sudo chmod -R ugo+rwx '+'"'+path+'"')

			os.remove(path)
