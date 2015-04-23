#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time
import math
import scipy.stats


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
	cur.execute(sql)
	res=cur.fetchall()
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
		#write_API(stocka,stockb,stocka_price,stockb_price,except_buy_price,except_sell_price)
		result_DB(stocka,stockb,stocka_price,stockb_price,except_buy_price,except_sell_price)
		print(stocka,stockb,stocka_price,stockb_price,except_buy_price,except_sell_price)
def write_API(stocka,stockb,stocka_price,stockb_price,except_buy_price,except_sell_price):
	json=""
	file_object = open("C:/Users/dell/AppData/Roaming/MetaQuotes/Terminal/50CA3DFB510CC5A8F28B48D1BF2A5702/MQL4/Files/API.txt",'w')
	for r in range(len(stocka)):
		#json=json+"'buyID':'"+str(stocka[r])+"',buyprice':'"+str(stocka_price[r])+"','sellID':'"+str(stockb[r])+"','sellprice':'"+str(stockb_price[r])+"','except_buy_price':'"+str(except_buy_price[r])+"','except_sell_price':'"+str(except_sell_price[r])+"'"+"\n"
		json=json+str(stocka[r][0:6])+","+str(stocka_price[r])+","+str(stockb[r][0:6])+","+str(stockb_price[r])+","+str(except_buy_price[r])+","+str(except_sell_price[r])+"\n"
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
	cur.execute(sql)
	conn.commit()
if __name__ == "__main__":
	time1=time.time()
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	cur=conn.cursor()
	sign(0.6,0.4,0.5)
	cur.close()
	conn.close()
