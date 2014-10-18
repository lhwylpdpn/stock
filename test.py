import threading
import urllib
import urllib.request
import csv
import pymysql
import time

# 自动计算买卖函数
#CCi函数
def 计算收益(a,b,a_1,b_1):
	tag=0
	d=[]
	write=[]
	for i in range(len(b)):
		c=float(b[i])-float(a[i]) #单笔差值
		d.append(c/float(a[i])) #  单笔盈利率
		if c>0:
			tag=tag+1
		write.append(a_1[i]+"	"+str(a[i])+"	"+b_1[i]+"	"+str(b[i])+"	"+str(c/float(a[i]))+"\n")
	write.append("总笔数"+str(len(b))+",盈利笔数"+str(tag)+",盈利笔数比例"+str(tag/len(b)*100)+"%,总收益比例"+str(sum(d)))
	file_object = open('test.txt', 'w')
	file_object.writelines(write)
	file_object.close( )
 
def  CCI(high,low,close,n):
	r=[]
	m=len(high)
	vals=range(m)
	for i in vals:
		try:
			TP=float((high[i]+low[i]+close[i])/3)
			#suma=sum(float(close[k]) for k in range(i,i+n))
			suma=sum((float(high[k])+float(low[k])+float(close[k]))/3 for k in range(i,i+n))
			MA=suma/n
			#MD=sum(abs(float(close[k])-MA) for k in range(i,i+n))/n
			MD=sum(abs((float(high[k])+float(low[k])+float(close[k]))/3-MA) for k in range(i,i+n))/n
			CCI=(TP-MA)/MD/0.015
		except:
			CCI=0

		r.append(CCI)
	return r
		
if __name__ == "__main__":
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock',port=3306)
	curall=conn.cursor()
	cur=conn.cursor()
	
	#curall.execute("delete from target")
	#curall.execute("delete from clac1")
	cur.execute("select stockid from tmp3 group by stockid")
	stone_0=cur.fetchall()
	r=[]
	stockid=[]
	date=[]
	high=[]
	low=[]
	close=[]
	for r in stone_0:
		stockid.append(str(r[0]))
	
	for i in range(len(stockid)):

		date=[]
		high=[]
		low=[]
		close=[]
		curall.execute("select stockid,date,high,low,close from tmp3 where stockid='"+stockid[i]+"' and volume<>0  order by date desc")
		stone=curall.fetchall()
		for r in stone:
			try:
				date.append(str(r[1]))
				high.append(float(r[2]))
				low.append(float(r[3]))
				close.append(float(r[4]))
			except:
				continue
		#target()
		##############################插入计时
		time1=time.time()
		##############################
		r=CCI(high,low,close,14)
		r.reverse()
		date.reverse()
		high.reverse()
		low.reverse()
		close.reverse()
		##############################插入计时
		print(stockid[i]+"计算结束"+str(time.time()-time1)) 
		time1=time.time()


		a=[]
		b=[]
		a_1=[]
		b_1=[]
		tag=0
		for i in range(len(r)):
			
			if ((float(r[i])>100 and float(r[i-1])<100) or (float(r[i])>-100 and float(r[i-1])<-100)) and i>=tag: 
				a.append(close[i])
				a_1.append(date[i])
				#print(r[i],r[i-1])
				for j in range(i,len(r)):
					if (float(r[j])<100 and float(r[j-1])>100) or (float(r[j])<-100 and float(r[j-1])>-100):
						b.append(close[j])
						b_1.append(date[j])
						#print("买入时间"+str(a)+","+str(float(r[i]))+","+"迈出时间"+str(b)+","+str(float(r[j])),j)
						tag=j
						break
		计算收益(a,b,a_1,b_1)