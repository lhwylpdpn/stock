import threading
import urllib
import urllib.request
import csv
import pymysql
import time

conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock',port=3306)
curall=conn.cursor()
curall2=conn.cursor()
curall.execute("SELECT stockid FROM `stock` GROUP BY stockid")
stockids=curall.fetchall()
for stock in stockids:

	curall2.execute("SELECT * FROM stock WHERE stockid='"+stock[0]+"' ORDER BY DATE")
	stone=curall2.fetchall()
	i=0
	c_h_list=[]
	del c_h_list[:]
	for s in stone:
		if (round(float(s[5]-s[4])/s[5],2)>0):#获取涨跌幅度
			i=i+1
		else:
			i=0
		c_h_list.append(i)

	l_all=str(round(float(c_h_list.count(0)/len(c_h_list)),4))
	h1=str(round(float(c_h_list.count(1)/len(c_h_list)),4))
	h2=str(round(float(c_h_list.count(2)/len(c_h_list)),4))
	h3=str(round(float(c_h_list.count(3)/len(c_h_list)),4))
	h4=str(round(float(c_h_list.count(4)/len(c_h_list)),4))
	h5=str(round(float(c_h_list.count(5)/len(c_h_list)),4))
	h6=str(round(float(c_h_list.count(6)/len(c_h_list)),4))
	h7=str(round(float(c_h_list.count(7)/len(c_h_list)),4))
	h8=str(round(float(c_h_list.count(8)/len(c_h_list)),4))
	h9=str(round(float(c_h_list.count(9)/len(c_h_list)),4))
	h10=str(round(float(c_h_list.count(10)/len(c_h_list)),4))

	curall.execute("insert into stock_h_l values('"+stock[0]+"','"+l_all+"','"+h1+"','"+h2+"','"+h3+"','"+h4+"','"+h5+"','"+h6+"','"+h7+"','"+h8+"','"+h9+"','"+h10+"')")
	print(stock[0]+"is ok")
	conn.commit()
conn.close()