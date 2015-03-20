#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time
import math
def sign (p_gailv):#核心函数，查URL写数据库,计算指标库
	sql=" SELECT stockidA,stockidB FROM norm_data WHERE normvalue_per_500>= '"+p_gailv+"'"
	cur.execute(sql)
	res=cur.fetchall()
	for r in res:
		stocka.append(r[0])
		stockb.append(r[1])
	for r in range(len(stocka))




if __name__ == "__main__":
	time1=time.time()
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	cur=conn.cursor()
	loadcsv()
	calc()
	cur.close()
	conn.close()