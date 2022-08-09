import os
import psutil
import time
from datetime import date, datetime


current_time = datetime.now()
c_time = str(datetime.now()).split(' ')[0]

log_path = "/DriveD/Log/Kill_Log"
if not os.path.exists(log_path):
	os.makedirs(log_path)

with open(log_path+"//"+c_time+"_start_end_log.txt","a") as wr:
	wr.write("Start at "+str(datetime.now())+"\n")

year = datetime.now().year

try:
	# kill_flag = 0
	for pid in psutil.pids():
		p = psutil.Process(pid)
		if p.name() == "python":
			a = p.cmdline()[-1]
			# print a

			if str(a).startswith("/DriveU/GST Code/code_new/"):

				start_time = str(p).split("started='")[-1].split("'")[0]

				if str(year) not in start_time:
					start_time = c_time+' '+str(p).split("started='")[-1].split("'")[0]
				
				format = '%Y-%m-%d %H:%M:%S'

				start_time = datetime.strptime(start_time,format)
				
				current_datetime = str(datetime.now()).split('.')[0]
				current_datetime = datetime.strptime(current_datetime,'%Y-%m-%d %H:%M:%S')
				
				running_time = (current_datetime - start_time).total_seconds()
				print running_time

				max_run_time = "1800"

				# max_run_time = "5000"

				if running_time > int(max_run_time):
					print "str(a)",str(a)
					with open(log_path+"/"+c_time+"_start_end_log.txt","a") as wr:
						wr.write("Process is killed. "+str(a)+"\n")
					# p.kill()
					print pid
					os.system("sudo kill -9 "+str(pid))
					# kill_flag = 1

					# listfiles = os.listdir("/DriveD/Doclist_new/MainServerSyncDocList/Input/DocList_bulk/")
					# listfiles = ["/DriveD/Doclist_new/MainServerSyncDocList/Input/DocList_bulk/"+x for x in listfiles if "_Pending.txt" in x]

					# for file in listfiles:
					# 	try:
					# 		os.rename(file,file.replace('_Pending','_New'))
					# 	except:
					# 		pass

except Exception, err:
	with open(log_path+"/"+c_time+"_start_end_log.txt","a") as wr:
		wr.write("Error "+str(err)+"\n")

with open(log_path+"/"+c_time+"_start_end_log.txt","a") as wr:
	wr.write("End at "+str(datetime.now())+"\n")