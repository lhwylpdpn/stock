#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time
import math
import json

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
	clac=(float(data_line[3])-float(data_line[2]))*float(count)
	return clac
def clac2 (stockid,count):#卖空计算
	testhtml=urllib.request.urlopen("http://hq.sinajs.cn/list="+stockid).read()
	data_line=testhtml.decode('GBK').split(',')
	clac=(float(data_line[2])-float(data_line[3]))*float(count)
	
	return clac
if __name__ == '__main__':

	file = 'F:/data-show/json/private.json'
	f = open(file, 'r')
	dict = json.dumps(f.read())
	f.close()

	chengben=21.59*1000+34.41*1100+20.96*1100+27.06*500
	chengben2=21.59*1000+34.41*1100+20.96*1100+27.06*500
	dangqian=float(req("sh600369","21.59","1000"))*1000+31.96*1100+float(req("sz002736","20.96","1100"))*1100+float(req("sh600109","27.06","500"))*500

	f2=(float(dangqian)-float(chengben2))#收益
	f3=f2/(chengben)#收益百分比
	f4=f2+chengben+148.98+9803#总资金

	#f6=
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