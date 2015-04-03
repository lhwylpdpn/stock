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

def req (stockid,chengben,count):#买多计算
	testhtml=urllib.request.urlopen("http://hq.sinajs.cn/list="+stockid).read()
	data_line=testhtml.decode('GBK').split(',')
	stockid_now=data_line[6]
	print(stockid_now,chengben,(float(stockid_now)-float(chengben))*float(count))
	return stockid_now
def req2 (stockid,chengben,count):#卖空计算
	testhtml=urllib.request.urlopen("http://hq.sinajs.cn/list="+stockid).read()
	data_line=testhtml.decode('GBK').split(',')
	stockid_now=data_line[6]
	print(stockid_now,chengben,(float(chengben)-float(stockid_now))*float(count))
	return stockid_now
def clac (stockid,count):#卖空计算
	testhtml=urllib.request.urlopen("http://hq.sinajs.cn/list="+stockid).read()
	data_line=testhtml.decode('GBK').split(',')
	clac=(float(data_line[3])-float(data_line[1]))*float(count)

	return clac
def clac2 (stockid,count):#卖空计算
	testhtml=urllib.request.urlopen("http://hq.sinajs.cn/list="+stockid).read()
	data_line=testhtml.decode('GBK').split(',')
	clac=(float(data_line[1])-float(data_line[3]))*float(count)
	
	return clac
if __name__ == '__main__':
	chengben=4.106*4000+21.59*1000+34.41*1100+21.15*1000
	chengben2=-4.106*4000+21.59*1000+34.41*1100+21.15*1000
	dangqian=float(req("sh600369","21.59","1000"))*1000+31.96*1100+float(req("sz002736","21.15","1000"))*1000 - float(req2("sh510300","4.106","4000"))*4000

	f2=(float(dangqian)-float(chengben2))
	f3=f2/(chengben)
	f4=f2+chengben+2057+7415
	# kong_price=3.439
	f6=clac("sh600369","1000")+clac("sz002736","1000")+clac2("sh510300","4000")
	# duo_price=21.047
	# kong_count=3000
	# duo_count=300
	# kong_now=req("sh510300")
	# duo_now=req("sz002736")
	# #当前营收价钱
	# f1_1=(kong_price-float(kong_now))*kong_count
	# f1_2=(float(duo_now)-duo_price)*duo_count
	# f1=(kong_price-float(kong_now))*kong_count+(float(duo_now)-duo_price)*duo_count
	# #当前营收比例
	# f2=f1/(kong_price*kong_count+duo_count*duo_price)
	# #当前偏差情况
	# f3=math.log(float(kong_now))-math.log(float(duo_now))
	# f4=norm(f3,0.17201,0.0394025)
	# #预期收益
	# print(f1_1)
	# print(f1_2)
	# print(f1)
	print(chengben)
	print(f2)
	print(f3)
	print(f4)
	print(f6)