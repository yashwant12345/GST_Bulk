import pandas as pd
from datetime import datetime


def proxy_change():
	file = "/DriveD/Pan Bulk Download Codes/proxy_webshare.csv"

	df = pd.read_csv(file,sep="|")
	df = df.sort_values(by=["datetime"])
	ips = df['proxy'].tolist()
	p_ip_new = ips[0]
	df.loc[df['proxy']==p_ip_new,"datetime"]=str(datetime.now())
	df.to_csv(file,sep="|",index=False)
	return p_ip_new
	
	