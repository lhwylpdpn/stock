#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time
import math
def st_norm(u):
	x=abs(u)/math.sqrt(2)
	T=(0.0705230784,0.0422820123,0.0092705272,0.0001520143,0.0002765672,0.0000430638)
	E=1-pow((1+sum([a*pow(x,(i+1)) for i,a in enumerate(T)])),-16)
	p=0.5-0.5*E if u<0 else 0.5+0.5*E
	return(p)
  
def norm(x,a,sigma):

	u=(x-a)/sigma
	return(st_norm(u))

def stdev(self):
	if len(self) < 1:
		return None
	else:
		avg = sum(self)/len(self)
		sdsq = sum([(i - avg) ** 2 for i in self])
		stdev = (sdsq / (len(self) - 1)) ** .5
		return stdev

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

	#print(sum(logresult)/len(logresult))
	#print(stdev(logresult))
	sqlresult=" insert into norm_data values ('"+ida+"','"+idb+"','"+str(norm(logresult[0],sum(logresult[0:30])/len(logresult[0:30]),stdev(logresult[0:30])))+"','"+str(norm(logresult[0],sum(logresult[0:90])/len(logresult[0:90]),stdev(logresult[0:90])))+"','"+str(norm(logresult[0],sum(logresult[0:365])/len(logresult[0:365]),stdev(logresult[0:365])))+"','"+str(norm(logresult[0],sum(logresult)/len(logresult),stdev(logresult)))+"','"+str(sum(logresult[0:30])/len(logresult[0:30]))+"','"+str(sum(logresult[0:90])/len(logresult[0:90]))+"','"+str(sum(logresult[0:365])/len(logresult[0:365]))+"','"+str(sum(logresult)/len(logresult))+"','"+str(stdev(logresult[0:30]))+"','"+str(stdev(logresult[0:90]))+"','"+str(stdev(logresult[0:365]))+"','"+str(stdev(logresult))+"'); "
	#sqlresult=" insert into norm_data values ('"+ida+"','"+idb+"',null,null,null,'"+str(norm(logresult[0],sum(logresult)/len(logresult),stdev(logresult)))+"',null,null,null,'"+str(sum(logresult)/len(logresult))+"',null,null,null,'"+str(stdev(logresult))+"'); "
	cur.execute(sqlresult)
	conn.commit()



if __name__ == "__main__":
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock',port=3306)
	curall=conn.cursor()
	cur=conn.cursor()
	cur.execute("delete from norm_data")
	conn.commit()
	stockid=[]
	sql="SELECT stockidA,stockidB FROM `releation` WHERE relation_per_month>0.9 AND relation_per_year>0.8 LIMIT 10 "# 选取相关性强股票的策略
	cur.execute(sql)
	res=cur.fetchall()
	for r in res:
		print(r[0],r[1]+"  is ok")
		calc(r[0],r[1])
