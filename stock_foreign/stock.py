#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time
import os
def loadcsv_add():
	high=[]
	low=[]
	open_=[]
	close=[]
	name_=[]
	date_=[]
	time_=[]
	sql=""
	reader = csv.reader(open("C:/Users/Administrator/AppData/Roaming/MetaQuotes/Terminal/50CA3DFB510CC5A8F28B48D1BF2A5702/MQL4/Files/API_callback.csv"))
	for row in reader:
		name_.append(row[0]+"60.csv")
		date_.append(row[1][0:10])
		time_.append(row[1][11:16])
		open_.append(row[2])
		high.append(row[3])
		low.append(row[4])
		close.append(row[5])

	for i in range(len(date_)):
				
		sql=sql+"insert into stock_foreign.stock values ('"+name_[i]+"','"+date_[i]+"','"+time_[i]+"','"+open_[i]+"','"+high[i]+"','"+low[i]+"','"+close[i]+"',0,'"+str((float(close[i])-float(open_[i]))/float(open_[i]))+"',null);"
	cur.execute(sql)
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

def loadcsv ():#核心函数，查URL写数据库,计算指标库
	sql="delete from stock;"
	s=os.getcwd()
	for filename in getFileList(os.getcwd()+"\stock-data"):
		print(filename)
		high=[]
		low=[]
		open_=[]
		close=[]
		amount=[]
		date_=[]
		time_=[]
		reader = csv.reader(open("stock-data/"+filename))
		for row in reader:
			date_.append(row[0])
			time_.append(row[1])
			open_.append(row[2])
			high.append(row[3])
			low.append(row[4])
			close.append(row[5])
			amount.append(row[6])
		for i in range(len(date_)):
			if i==0:
				sql=sql+"insert into stock_foreign.stock values ('"+filename+"','"+date_[i]+"','"+time_[i]+"','"+open_[i]+"','"+high[i]+"','"+low[i]+"','"+close[i]+"','"+amount[i]+"',0,null);"
			else:
				sql=sql+"insert into stock_foreign.stock values ('"+filename+"','"+date_[i]+"','"+time_[i]+"','"+open_[i]+"','"+high[i]+"','"+low[i]+"','"+close[i]+"','"+amount[i]+"','"+str((float(close[i])-float(close[i-1]))/float(close[i-1]))+"',null);"
	cur.execute(sql)


# def target():#写入各种参照值

# 	sql="INSERT INTO target SELECT a.date,a.close, (a.close - b.close)/a.close  FROM (SELECT  (@i:=@i+1)   AS   i,stockid,DATE,CLOSE FROM stock ,(SELECT   @i:=1) AS it WHERE stockid='000300.ss' ORDER BY DATE DESC) AS a ,(SELECT  (@j:=@j+1)   AS   i,stockid,DATE,CLOSE FROM stock ,(SELECT   @j:=0) AS it WHERE stockid='000300.ss' ORDER BY DATE DESC) AS b WHERE a.i=b.i"

# 	cur.execute(sql)
# 	print("000300.ss target is ok")
# 	conn.commit()
def calc():#计算个股与指标之间的相关度
	close_1=[]
	close_2=[]
	per_1=[]
	per_2=[]
	date1=[]
	stockid=[]
	time1=[]
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
				sql="select a.date,a.time,a.close,b.close,a.per,b.per from stock a ,stock b where a.stockid='"+stockid[i]+"' and b.stockid='"+stockid[j]+"' and a.date=b.date and a.time=b.time ORDER BY DATE_FORMAT(CONCAT(a.date,' ',a.time),'%Y.%c.%d %H:%i')"
				cur.execute(sql)
				res=cur.fetchall()
				for r in res:
					close_1.append(float(r[2]))
					close_2.append(float(r[3]))
					per_1.append(float(r[4]))
					per_2.append(float(r[5]))
					date1.append(str(r[0]))
					time1.append(str(r[1]))
				
				sql="insert into releation values('"+stockid[i]+"','"+stockid[j]+"','"+str(pearson(close_1[0:100],close_2[0:100]))+"','"+str(pearson(close_1[0:1000],close_2[0:1000]))+"','"+str(pearson(close_1,close_2))+"','"+str(pearson(per_1[0:100],per_2[0:100]))+"','"+str(pearson(per_1[0:1000],per_2[0:1000]))+"','"+str(pearson(per_1,per_2))+"','"+str(len(res))+"')"
				cur.execute(sql)
				# print(str(pearson(close_1,close_2)))
				# print(str(pearson(per_1,per_2)))
				# print(str(pearson(close_1[0:30],close_2[0:30])))
				# print(str(pearson(per_1[0:30],per_2[0:30])))
				# print(str(pearson(close_1[0:500],close_2[0:500])))
				# print(str(pearson(per_1[0:500],per_2[0:500])))
				# print(len(res))

				close_1=[]
				close_2=[]
				per_1=[]
				per_2=[]

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
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	cur=conn.cursor()

	loadcsv()
	#loadcsv_add()
	calc()
	cur.close()
	conn.close()