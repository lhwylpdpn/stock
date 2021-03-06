#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time

def timer (stockid):#核心函数，查URL写数据库,计算指标库
	testhtml=urllib.request.urlopen("http://table.finance.yahoo.com/table.csv?s="+stockid).read()
	data_line=testhtml.decode("utf8").split('\n')
	del data_line[0]
	del data_line[len(data_line)-1]
	#print(len(data_line))
	#for data in data_line:
	sql=""
	for i in range(len(data_line)):
		datas=data_line[i].split(',')
		if i<len(data_line)-1:
			datas_yes=data_line[i+1].split(',')
			sql=sql+"insert into stock.stock values('"+stockid+"','"+datas[0]+"','"+datas[2]+"','"+datas[3]+"','"+datas[1]+"','"+datas[4]+"','"+datas[6]+"','"+datas[5]+"','"+str((float(datas[4])-float(datas_yes[4]))/float(datas_yes[4]))+"',null);"
		else:
			sql=sql+"insert into stock.stock values('"+stockid+"','"+datas[0]+"','"+datas[2]+"','"+datas[3]+"','"+datas[1]+"','"+datas[4]+"','"+datas[6]+"','"+datas[5]+"',0,null);"
	#print (sql)
	cur.execute(sql)
	print(stockid+" is ok"+str(time.time()-time1)) 


def target():#写入各种参照值

	sql="INSERT INTO target SELECT a.date,a.close, (a.close - b.close)/a.close  FROM (SELECT  (@i:=@i+1)   AS   i,stockid,DATE,CLOSE FROM stock ,(SELECT   @i:=1) AS it WHERE stockid='000300.ss' ORDER BY DATE DESC) AS a ,(SELECT  (@j:=@j+1)   AS   i,stockid,DATE,CLOSE FROM stock ,(SELECT   @j:=0) AS it WHERE stockid='000300.ss' ORDER BY DATE DESC) AS b WHERE a.i=b.i"

	cur.execute(sql)
	print("000300.ss target is ok")
	conn.commit()
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
		print(r[0])
		stockid.append(r[0])
	for i in range(len(stockid)):
		for j in range(len(stockid)):
			if i<j:
				dict1[stockid[i]]=stockid[j]
	
	#cur.execute(sql)
	#r_clac=cur.fetchall()
	for (d,x) in dict1.items():
		sql="select a.date,a.close,b.close,a.per,b.per from stock a ,stock b where a.stockid='"+d+"' and b.stockid='"+x+"' and a.date=b.date order by date desc"
		cur.execute(sql)
		res=cur.fetchall()
		for r in res:
			close_1.append(float(r[1]))
			close_2.append(float(r[2]))
			per_1.append(float(r[3]))
			per_2.append(float(r[4]))
			date1.append(str(r[0]))
		sql="insert into releation values('"+d+"','"+x+"','"+str(pearson(close_1[0:30],close_2[0:30]))+"','"+str(pearson(close_1[0:365],close_2[0:365]))+"','"+str(pearson(close_1,close_2))+"','"+str(pearson(per_1[0:30],per_2[0:30]))+"','"+str(pearson(per_1[0:365],per_2[0:365]))+"','"+str(pearson(per_1,per_2))+"','"+str(len(res))+"')"
		cur.execute(sql)
		print(str(pearson(close_1,close_2)))
		print(str(pearson(per_1,per_2)))
		print(str(pearson(close_1[0:30],close_2[0:30])))
		print(str(pearson(per_1[0:30],per_2[0:30])))
		print(str(pearson(close_1[0:365],close_2[0:365])))
		print(str(pearson(per_1[0:365],per_2[0:365])))
		print(len(res))
	
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
	curall.execute("delete from stock")
	# #curall.execute("delete from target")
	# #curall.execute("delete from clac1")
	curall.execute("SELECT CONCAT(CODE,class) FROM stock_code WHERE STATUS=1")
	stone=curall.fetchall()
	for r in stone:
	 	#try:
	 	timer(str(r[0]))
	 	#except:
	 		#print("error   "+str(r[0]))
	 			
	#target()
	#for r in stone:
	#	try:
	#		calc(str(r[0]))
	#	except:
	#		continue
	conn.commit()
	
	
