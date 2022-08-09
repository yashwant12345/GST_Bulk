import requests
import os
import pandas as pd
from time import sleep
import pdb
# os.system("sudo service apache2 restart")
# sleep(10)

df = pd.DataFrame()

file = "/DriveG/DriveF/AutoCSV/BSE/Detailed_2021-12-21 18:53:23.951659_New_Done.csv"

with open(file,'rb') as rd:
	file_data = rd.read()



# pdf_path = "/DriveK/Final End To End/30.pdf"

req = requests.post('http://ec2-54-255-94-235.ap-southeast-1.compute.amazonaws.com/file_upload',data={'file_data':file_data,'name':"yash_test.csv"})
# req = requests.get('http://ec2-54-255-94-235.ap-southeast-1.compute.amazonaws.com/ibbipdf?pdf_path=/DriveD/hosting/Allahabad.pdf')
print req.text
exit()
# pdb.set_trace()
# print req.content
# filename = str(eq.headers['Content-Disposition']).split("filename=")[-1].replace('.zip','')
# print filename
with open('/home/ubuntu/Desktop/sample.pdf','wb') as wr:
	wr.write(req.content)

# for upload files================


# afile = open('/home/ubuntu/Desktop/aa040d18b4ab.zip','r')
# fullfile = afile.read()
# afile.close()

# files = {
#     'file': (
#     	"/DriveH/zip_file_upload/aa040d18b4ab.zip",
#         open('/home/ubuntu/Desktop/aa040d18b4ab.zip', 'rb'), 
#         'application/octet-stream'
#     )
# }

# eq = requests.post('http://ec2-13-229-129-224.ap-southeast-1.compute.amazonaws.com/upload',files=files).content
# print eq