#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time

def calc():#计算个股与指标之间的相关度
	close_1=[]
	close_2=[]
	per_1=[]
	per_2=[]
	date1=[]
	stockid=[]
	a=[]
	b=[]
	
	sql="select stockid from stock group by stockid"
	cur.execute(sql)
	res=cur.fetchall()
	dict1={}
	for r in res:
		stockid.append(r[0])
	for i in range(len(stockid)):
		for j in range(len(stockid)):
			if i<j:
				sql="select a.date,a.close,b.close,a.per,b.per from stock a ,stock b where a.stockid='"+stockid[i]+"' and b.stockid='"+stockid[j]+"' and a.date=b.date order by date desc"
				cur.execute(sql)
				res=cur.fetchall()
				for r in res:
					close_1.append(float(r[1]))
					close_2.append(float(r[2]))
					per_1.append(float(r[3]))
					per_2.append(float(r[4]))
					date1.append(str(r[0]))
				sql="insert into releation values('"+stockid[i]+"','"+stockid[j]+"','"+str(pearson(close_1[0:30],close_2[0:30]))+"','"+str(pearson(close_1[0:365],close_2[0:365]))+"','"+str(pearson(close_1,close_2))+"','"+str(pearson(per_1[0:30],per_2[0:30]))+"','"+str(pearson(per_1[0:365],per_2[0:365]))+"','"+str(pearson(per_1,per_2))+"','"+str(len(res))+"')"
				cur.execute(sql)
				print(str(pearson(close_1,close_2)))
				print(str(pearson(per_1,per_2)))
				print(str(pearson(close_1[0:30],close_2[0:30])))
				print(str(pearson(per_1[0:30],per_2[0:30])))
				print(str(pearson(close_1[0:365],close_2[0:365])))
				print(str(pearson(per_1[0:365],per_2[0:365])))
				print(len(res))
				close_1=[]
				close_2=[]
				per_1=[]
				per_2=[]
	
	#sql="insert into clac1 (stockid, relativity) values ('"+stockid+"','"+str(pearson(pearson_1,pearson_2))+"')"
	#	cur.execute(sql)
	#print(stockid+" 计算 is ok 总计用时间"+str(time.time()-time1)) 
	#conn.commit()

def pearson(x,y):
	n=len(x)
	vals=range(n)
	# Simple sums
	sumx=sum([float(x[i]) for i in vals])
	sumy=sum([float(y[i]) for i in vals])
	# Sum up the squares
	sumxSq=sum([x[i]**2.0 for i in vals])
	sumySq=sum([y[i]**2.0 for i in vals])
	# Sum up the products
	pSum=sum([x[i]*y[i] for i in vals])
	# Calculate Pearson score
	num=pSum-(sumx*sumy/n)
	den=((sumxSq-pow(sumx,2)/n)*(sumySq-pow(sumy,2)/n))**.5
	if den==0: return 0
	r=num/den
	return r
if __name__ == "__main__":
	time1=time.time()
	threads=[]
	pearson_1=[]
	pearson_2=[]
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock',port=3306)
	curall=conn.cursor()
	cur=conn.cursor()
	calc()
	# #curall.execute("delete from target")
	# #curall.execute("delete from clac1")
	
	#target()
	#for r in stone:
	#	try:
	#		calc(str(r[0]))
	#	except:
	#		continue
	conn.commit()
	
	
