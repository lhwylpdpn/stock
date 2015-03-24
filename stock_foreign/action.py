#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time
import math




def sign (p_gailv_high,p_gailv_low):#核心函数，查URL写数据库,计算指标库
	stocka=[]
	stockb=[]
	stocka_price=[]
	stockb_price=[]
	norm=[]
	norm_avg=[]
	norm_stdev=[]
	sql="SELECT stockidA,stockidB,stockida_price,stockidb_price,normvalue_per_500,norm_avg_500,norm_stdev_500 FROM norm_data WHERE (normvalue_per_500>= '"+str(p_gailv_high)+"' or normvalue_per_500<='"+str(p_gailv_low)+"')"
	cur.execute(sql)
	res=cur.fetchall()
	for r in res:
		stocka.append(r[0])
		stockb.append(r[1])
		stocka_price.append(r[2])
		stockb_price.append(r[3])
		norm.append(r[4])
		norm_avg.append(r[5])
		norm_stdev.append(r[6])

	write_API(stocka,stockb,stocka_price,stockb_price)
	result_DB(stocka,stockb,stocka_price,stockb_price)

def write_API(stocka,stockb,stocka_price,stockb_price):
	json=""
	file_object = open('API.txt','w')
	for r in range(len(stocka)):
		json=json+"{'buyID':'"+str(stocka[r])+"',buyprice':'"+str(stocka_price[r])+"','sellID':'"+str(stockb[r])+"','sellprice':'"+str(stockb_price[r])+"'}"+"\n"
	file_object.write(json)
	file_object.close()
#def clac_except():
def result_DB(stocka,stockb,stocka_price,stockb_price):
	sql=""
	for r in range(len(stocka)):
		sql=sql+"insert into `order` values (null,'"+str(stocka[r])+"','"+str(stockb[r])+"','"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"','"+str(stocka_price[r])+"','"+str(stockb_price[r])+"',null,0,0,0,0);"
	cur.execute(sql)
	conn.commit()
if __name__ == "__main__":
	time1=time.time()
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	cur=conn.cursor()
	sign(0.9,0.1)
	cur.close()
	conn.close()
	