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
	for data in data_line:
		datas=data.split(',')
		sql="insert into stock.tmp3 values('"+stockid+"','"+datas[0]+"','"+datas[2]+"','"+datas[3]+"','"+datas[1]+"','"+datas[4]+"','"+datas[6]+"','"+datas[5]+"',null,null)"
		#print (sql)
		cur.execute(sql)
	print(stockid+" is ok"+str(time.time()-time1)) 

	conn.commit()


if __name__ == "__main__":
	time1=time.time()
	threads=[]
	pearson_1=[]
	pearson_2=[]
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock',port=3306)
	curall=conn.cursor()
	cur=conn.cursor()
	curall.execute("delete from tmp3")
	#curall.execute("delete from target")
	#curall.execute("delete from clac1")
	curall.execute("SELECT CONCAT(CODE,class) FROM stock_code2 WHERE STATUS=1")
	stone=curall.fetchall()
	for r in stone:
	
		timer(str(r[0]))
		
	conn.commit()	