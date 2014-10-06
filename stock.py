import threading
import urllib
import urllib.request
import csv
import pymysql
import time

def timer (stockid):#核心函数，查URL写数据库
	testhtml=urllib.request.urlopen("http://table.finance.yahoo.com/table.csv?s="+stockid).read()
	data_line=testhtml.decode("utf8").split('\n')
	del data_line[0]
	del data_line[len(data_line)-1]
	#print(len(data_line))
	for data in data_line:
		datas=data.split(',')
		sql="insert into stock.stock values('"+stockid+"','"+datas[0]+"','"+datas[2]+"','"+datas[3]+"','"+datas[1]+"','"+datas[4]+"','"+datas[6]+"','"+datas[5]+"',null,null)"
		#print (sql)
		cur.execute(sql)
	print(stockid+" is ok") 
	conn.commit()


def calc(stockid):#计算大盘赶超率和大盘相关度
	sql="INSERT INTO clac1(stockid,relativity,over) SELECT a.stockid,AVG(ABS(c-d)),AVG(c-d) FROM (SELECT a.stockid,a.date,(a.close - b.close)/b.close AS c FROM (SELECT  (@i:=@i+1)   AS   i,stockid,DATE,CLOSE FROM stock ,(SELECT @i:=1) AS it WHERE stockid='"+stockid+"' ORDER BY DATE DESC) AS a ,(SELECT  (@j:=@j+1)   AS   i,stockid,DATE,CLOSE FROM stock ,(SELECT   @j:=0) AS it WHERE stockid='"+stockid+"' ORDER BY DATE DESC) AS b WHERE a.i=b.i) a ,(SELECT a.stockid,a.date, (a.close - b.close)/a.close AS d FROM (SELECT  (@k:=@k+1)   AS   i,stockid,DATE,CLOSE FROM stock ,(SELECT   @k:=1) AS it WHERE stockid='000300.ss' ORDER BY DATE DESC) AS a ,(SELECT  (@l:=@l+1)   AS   i,stockid,DATE,CLOSE FROM stock ,(SELECT   @l:=0) AS it WHERE stockid='000300.ss'  ORDER BY DATE DESC) AS b WHERE a.i=b.i ) b WHERE a.date=b.date "

	cur.execute(sql)
	print(stockid+" 计算 is ok") 
	conn.commit()

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
	threads=[]
	pearson_1=[]
	pearson_2=[]
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock',port=3306)
	curall=conn.cursor()
	#curall.execute("delete from stock")
	#curall.execute("delete from clac1")
	cur=conn.cursor()
	curall.execute("SELECT * from tmp ")
	stone=curall.fetchall()
	for r in stone:
		pearson_1.append(float(r[0]))
		pearson_2.append(float(r[1]))

		#timer(str(r[0]))
	print(pearson(pearson_1,pearson_2))
	#for r in stone:
	#	calc(str(r[0]))
	#conn.commit()
