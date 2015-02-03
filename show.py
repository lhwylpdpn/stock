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

def req (stockid):#核心函数，查URL写数据库,计算指标库
	testhtml=urllib.request.urlopen("http://hq.sinajs.cn/list="+stockid).read()
	data_line=testhtml.decode('GBK').split(',')
	stockid_now=data_line[6]
	print(stockid_now)
	return stockid_now
if __name__ == '__main__':

	kong_price=26.91
	duo_price=24.69
	kong_count=200
	duo_count=200
	kong_now=req("sh600030")
	duo_now=req("sh600999")
	#当前营收价钱
	f1=-((kong_price-float(kong_now))*kong_count+(float(duo_now)-duo_price)*duo_count)
	#当前营收比例
	f2=f1/(kong_price*kong_count+duo_count*duo_price)
	#当前偏差情况
	f3=math.log(float(kong_now))-math.log(float(duo_now))
	f4=norm(f3,0.17201,0.0394025)
	#预期收益
	print(f1)
	print(f2)
	print(f4)