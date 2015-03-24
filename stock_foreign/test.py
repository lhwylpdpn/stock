#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time
import math


def action():
	stocka=[]
	stockb=[]
	stocka_price=[]
	stockb_price=[]
	orderid=[]
	next_high=[]
	next_low=[]
	next_stockid=[]
	sql2=""
	sql="select order_stockA,order_stockB,order_priceA,order_priceB,orderid from `order` where action=0 and status=0"
	cur.execute(sql)
	res=cur.fetchall()
	for r in res:
		stocka.append(r[0])
		stockb.append(r[1])
		stocka_price.append(r[2])
		stockb_price.append(r[3])
		orderid.append(r[4])
		sql2=sql2+"update `order` set status=1 where orderid='"+str(r[4])+"'"

	cur.execute(sql2)
	sql="SELECT high,low,stockid FROM `stock_test` WHERE DATE_FORMAT(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') IN (SELECT DATE_FORMAT(DATE_ADD(MIN(DATE_FORMAT(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i')),INTERVAL 1 HOUR),'%Y.%c.%d %H:%i') FROM stock)"
	cur.execute(sql)
	res=cur.fetchall()
	for r in res:
		next_high.append(r[0])
		next_low.append(r[1])
		next_stockid.append(r[2])
	print(next_high)
	print(stocka)
if __name__ == "__main__":
	time1=time.time()
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	cur=conn.cursor()
	action()
	cur.close()
	conn.close()
	


  # 接到建仓信号，返回建仓成功
  # 判断下一小时内的ln（差额）的最大和最小，如果存在区间内，认为已经操作，如果没有不操作
 #  操作完毕后写入订单,写入卖操作
   #下一小时数据写回到stock库，重新执行stock、result、action

