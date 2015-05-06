#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time
import os
def getFileList( p ):
	p = str( p )
	if p=="":
		return [ ]
	p = p.replace( "/","\\")
	if p[-1] != "\\":
		p = p+"\\"
	a = os.listdir( p )
	b = [ x   for x in a if os.path.isfile( p + x ) ]
	return b
def report_load_all ():#核心函数，查URL写数据库,计算指标库
	sql=""
	s=os.getcwd()
	for filename in getFileList(os.getcwd()+"\static-data"):
		print(filename)
		orderid=[]
		high=[]
		low=[]
		open_price=[]
		open_time=[]
		close_price=[]
		close_time=[]
		profit=[]
		report_time=[]
		buyprice_except_open=[]
		sellprice_except_open=[]

		reader = csv.reader(open("static-data/"+filename))
		for row in reader:
			
			orderid.append(row[0])
			open_price.append(row[1])
			open_time.append(row[2])
			close_price.append(row[3])
			close_time.append(row[4])
			profit.append(row[5])
			report_time.append(row[8])
			buyprice_except_open.append(row[9])
			sellprice_except_open.append(row[10])
			sql=sql+"insert into report_order values (null,'"+str(row[0])+"','"+str(row[1])+"','"+str(row[2])+"','"+str(row[3])+"','"+str(row[4])+"','"+str(row[5])+"','"+str(row[8])+"','"+str(row[9])+"','"+str(row[10])+"');"
		cur.execute(sql)

if __name__ == "__main__":
	time1=time.time()
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	cur=conn.cursor()
	report_load_all()
	#loadcsv_add()
	#calc()
	conn.commit()
	cur.close()
	conn.close()