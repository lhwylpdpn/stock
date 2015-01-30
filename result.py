#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time
import math

def calc(ida,idb):#计算个股与指标之间的相关度
	adj_close_1=[]
	adj_close_2=[]
	date=[]
	stockidA=[]
	stockidB=[]
	logresult=[]
	sqlresult=""
	sql="select a.date,a.adj,b.adj from stock a,stock b where a.stockid='"+ida+"' and b.stockid='"+idb+"' and a.date=b.date order by a.date desc"
	cur.execute(sql)
	res=cur.fetchall()
	dict1={}
	for r in res:
		date.append(r[0])
		stockidA.append(r[1])
		stockidB.append(r[2])
		logresult.append(math.log(r[1])-math.log(r[2]))
		sqlresult=sqlresult+" insert into temp values ('"+r[0]+"','"+str(math.log(r[1])-math.log(r[2]))+"'); "
	cur.execute("delete from temp")
	cur.execute(sqlresult)
	conn.commit()





if __name__ == "__main__":
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock',port=3306)
	curall=conn.cursor()
	cur=conn.cursor()
	calc('600999.ss','000776.sz')