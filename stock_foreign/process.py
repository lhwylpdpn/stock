#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time
import os
import math
import scipy.stats
def loadcsv_add():
	high=[]
	low=[]
	open_=[]
	close=[]
	name_=[]
	date_=[]
	time_=[]
	sql=""
	reader = csv.reader(open("C:/Users/dell/AppData/Roaming/MetaQuotes/Terminal/50CA3DFB510CC5A8F28B48D1BF2A5702/MQL4/Files/API_callback.csv"))
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
	cur_stock.execute(sql)
def calc1():#计算个股与指标之间的相关度
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
	cur_stock.execute(sql)
	res=cur_stock.fetchall()
	dict1={}
	for r in res:
		stockid.append(r[0])
	for i in range(len(stockid)):
		for j in range(len(stockid)):
			if i<j:
				sql="select a.date,a.time,a.close,b.close,a.per,b.per from stock a ,stock b where a.stockid='"+stockid[i]+"' and b.stockid='"+stockid[j]+"' and a.date=b.date and a.time=b.time ORDER BY DATE_FORMAT(CONCAT(a.date,' ',a.time),'%Y.%c.%d %H:%i')"
				cur_stock.execute(sql)
				res=cur_stock.fetchall()
				for r in res:
					close_1.append(float(r[2]))
					close_2.append(float(r[3]))
					per_1.append(float(r[4]))
					per_2.append(float(r[5]))
					date1.append(str(r[0]))
					time1.append(str(r[1]))
				
				sql="insert into releation values('"+stockid[i]+"','"+stockid[j]+"','"+str(pearson(close_1[0:30],close_2[0:30]))+"','"+str(pearson(close_1[0:500],close_2[0:500]))+"','"+str(pearson(close_1,close_2))+"','"+str(pearson(per_1[0:30],per_2[0:30]))+"','"+str(pearson(per_1[0:500],per_2[0:500]))+"','"+str(pearson(per_1,per_2))+"','"+str(len(res))+"')"
				cur_stock.execute(sql)
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
	sql="select a.date,a.close,b.close from stock a,stock b where a.stockid='"+ida+"' and b.stockid='"+idb+"' and a.date=b.date and a.time=b.time ORDER BY DATE_FORMAT(CONCAT(a.date,' ',a.time),'%Y.%c.%d %H:%i') desc"
	#desc 确保按照时间倒序排序，最新数据在logrequest0

	cur_result.execute(sql)
	res=cur_result.fetchall()
	dict1={}
	for r in res:
		date.append(r[0])	
		stockidA.append(r[1])
		stockidB.append(r[2])
		logresult.append(math.log(r[1])-math.log(r[2]))
	#print(logresult[0])
	#print(sum(logresult)/len(logresult))
	#print(stdev(logresult))
	sqlresult=" insert into norm_data values ('"+ida+"','"+idb+"','"+str(stockidA[0])+"','"+str(stockidB[0])+"','"+str(norm(logresult[0],sum(logresult[0:30])/len(logresult[0:30]),stdev(logresult[0:30])))+"','"+str(norm(logresult[0],sum(logresult[0:90])/len(logresult[0:90]),stdev(logresult[0:90])))+"','"+str(norm(logresult[0],sum(logresult[0:500])/len(logresult[0:500]),stdev(logresult[0:500])))+"','"+str(norm(logresult[0],sum(logresult)/len(logresult),stdev(logresult)))+"','"+str(sum(logresult[0:30])/len(logresult[0:30]))+"','"+str(sum(logresult[0:90])/len(logresult[0:90]))+"','"+str(sum(logresult[0:500])/len(logresult[0:500]))+"','"+str(sum(logresult)/len(logresult))+"','"+str(stdev(logresult[0:30]))+"','"+str(stdev(logresult[0:90]))+"','"+str(stdev(logresult[0:500]))+"','"+str(stdev(logresult))+"'); "
	#sqlresult=" insert into norm_data values ('"+ida+"','"+idb+"',null,null,null,'"+str(norm(logresult[0],sum(logresult)/len(logresult),stdev(logresult)))+"',null,null,null,'"+str(sum(logresult)/len(logresult))+"',null,null,null,'"+str(stdev(logresult))+"'); "
	cur_result.execute(sqlresult)
	conn.commit()





def banlace(buyprice,sellprice,except_norm,point):
	#假设AB都是正数
	#(a-buyprice+sellprice-b)/(sellprice+buyprice)=point/100
	b=((sellprice+buyprice)*point/100+(buyprice-sellprice))/(math.exp(except_norm)-1)
	a=math.exp(except_norm)*b
	return (a,b)
def sign (p_gailv_high,p_gailv_low,point):#核心函数，查URL写数据库,计算指标库
	stocka=[]
	stockb=[]
	stocka_price=[]
	stockb_price=[]
	norm=[]
	norm_avg=[]
	norm_stdev=[]
	except_norm=[]
	except_buy_price=[]
	except_sell_price=[]
	except_buy_price_temp=""
	except_sell_price_temp=""
	sql="SELECT stockidA,stockidB,stockida_price,stockidb_price,normvalue_per_500,norm_avg_500,norm_stdev_500 FROM norm_data WHERE (normvalue_per_500> '"+str(p_gailv_high)+"' or normvalue_per_500<'"+str(p_gailv_low)+"')"
	cur_action.execute(sql)
	res=cur_action.fetchall()
	if len(res)>0:
		for r in res:
			norm.append(r[4])
			norm_avg.append(r[5])
			norm_stdev.append(r[6])
			if r[4]>p_gailv_high:
				stocka.append(r[1])
				stockb.append(r[0])
				stocka_price.append(r[3])
				stockb_price.append(r[2])
				except_buy_price_temp,except_sell_price_temp=banlace(r[3],r[2],-scipy.stats.norm.ppf(p_gailv_high,r[5],r[6]),point)
				except_buy_price.append(except_buy_price_temp)
				except_sell_price.append(except_sell_price_temp)
			if r[4]<p_gailv_low:
				stocka.append(r[0])
				stockb.append(r[1])
				stocka_price.append(r[2])
				stockb_price.append(r[3])
				except_buy_price_temp,except_sell_price_temp=banlace(r[2],r[3],scipy.stats.norm.ppf(p_gailv_low,r[5],r[6]),point)
				except_buy_price.append(except_buy_price_temp)
				except_sell_price.append(except_sell_price_temp)
		write_API(stocka,stockb,stocka_price,stockb_price,except_buy_price,except_sell_price)
		result_DB(stocka,stockb,stocka_price,stockb_price,except_buy_price,except_sell_price)

def write_API(stocka,stockb,stocka_price,stockb_price,except_buy_price,except_sell_price):
	json=""
	file_object = open('API.txt','w')
	for r in range(len(stocka)):
		json=json+"{'buyID':'"+str(stocka[r])+"',buyprice':'"+str(stocka_price[r])+"','sellID':'"+str(stockb[r])+"','sellprice':'"+str(stockb_price[r])+"','except_buy_price':'"+str(except_buy_price[r])+"','except_sell_price':'"+str(except_sell_price[r])+"'}"+"\n"
		#print(math.log(stocka_price[r])-math.log(stockb_price[r])) #buy-sell>except 就平仓
		#print(except_norm[r])
		#print(math.log(stocka_price[r]/stockb_price[r]))
		#print(math.exp(except_norm[r]))
	file_object.write(json)
	file_object.close()

#def clac_except():
def result_DB(stocka,stockb,stocka_price,stockb_price,except_buy_price,except_sell_price):
	sql=""
	for r in range(len(stocka)):
		sql=sql+"insert into `order` values (null,'"+str(stocka[r])+"','"+str(stockb[r])+"','"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"','"+str(stocka_price[r])+"','"+str(stockb_price[r])+"',null,0,0,0,0,'"+str(except_buy_price[r])+"','"+str(except_sell_price[r])+"',null,null);"
	cur_action.execute(sql)
	conn.commit()






if __name__ == "__main__":
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	
	cur_stock=conn.cursor()
	cur_action=conn.cursor()

	cur_result=conn.cursor()

	
	

	while(1):

		cur_stock.execute("delete from releation")
		loadcsv_add()
		calc1()
		cur_result.execute("delete from norm_data")
		stockid=[]
		sql233="SELECT stockidA,stockidB FROM `releation` WHERE   relation_per_500>0.8 LIMIT 10"
		cur_result.execute(sql233)
		res=cur_result.fetchall()
		for j in res:
			calc(j[0],j[1])
		sign(0.9,0.1,0.05)
		
		time.sleep(3600)

	conn.close()



	# result.conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	# result.curall=result.conn.cursor()
	# result.cur=result.conn.cursor()
	# result.cur.execute("delete from norm_data")
	# result.conn.commit()
	# result.stockid=[]
	# result.sql="SELECT stockidA,stockidB FROM `releation` WHERE   relation_per_500>0.9 LIMIT 10 "# 选取相关性强股票的策略
	# result.cur.execute(result.sql)
	# result.res=result.cur.fetchall()
	# for r in result.res:
		
	# 	result.calc(r[0],r[1])


	# action.conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	# action.cur=action.conn.cursor()
	# action.sign(0.6,0.4,0.1)
	# action.cur.close()
	# action.conn.close()


	# test.conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	# test.cur=test.conn.cursor()
	# test.action()
	# test.cur.close()
	# test.conn.close()