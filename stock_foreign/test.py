#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time
import math


def action():
	stocka=[]
	stockb=[]
	stocka_price=[]
	stockb_price=[]
	orderid=[]
	next_high=[]
	next_low=[]
	next_stockid=[]
	except_buy_price=[]
	except_sell_price=[]
	sql2=""
	sql_action=""
	sql="select order_stockA,order_stockB,order_priceA,order_priceB,orderid,except_buy_price,except_sell_price from `order` where action=0 and status=0"
	cur.execute(sql)
	res=cur.fetchall()
	print(res)
	if res:
		for r in res:
			action_buy_price_temp=""
			action_sell_price_temp=""
			stocka.append(r[0])
			stockb.append(r[1])
			stocka_price.append(r[2])
			stockb_price.append(r[3])
			orderid.append(r[4])
			except_buy_price.append(r[5])
			except_sell_price.append(r[6])
			#sql2=sql2+"update `order` set status=1 where orderid='"+str(r[4])+"'"

			#cur.execute(sql2) 调试中，暂时取消更新状态
			#平仓操作
			sql="SELECT a.`stockid`,a.`high`,a.`low`,b.`stockid`,b.`high`,b.`low`,DATE_FORMAT(CONCAT(a.DATE,' ',a.TIME),'%Y.%c.%d %H:%i') FROM `stock_test`a ,stock_test b WHERE a.`stockid`='"+str(r[0])+"' AND b.`stockid`='"+str(r[1])+"' AND a.`date`=b.`date` AND a.`time`=b.`time` AND DATE_FORMAT(CONCAT(a.DATE,' ',a.TIME),'%Y.%c.%d %H:%i') IN (SELECT DATE_FORMAT(DATE_ADD(Max(DATE_FORMAT(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i')),INTERVAL 1 HOUR),'%Y.%c.%d %H:%i') FROM stock)"
			cur2.execute(sql)
			ress=cur2.fetchall()
			if len(ress)>0:
				print(ress)
				for j in ress:
					print(j[1],j[2],j[4],j[5],r[5],r[6])
						#r[5]except_buy_pirce r[6]except_sell_price
						#j[1]buy_high j[2]buy_low j[4]sell_high j[5]sell_low
					if j[1]>=r[5] and j[5]<=r[6] and j[2]<=r[5] and r[6]<=j[4]:
						action_buy_price_temp=r[5]
						action_sell_price_temp=r[6]
					if r[5]<j[2] and j[5]<=r[6]  and r[6]<=j[4]:
						action_buy_price_temp=j[2]
						action_sell_price_temp=r[6]
					if r[5]<j[2] and r[6]>j[4]:
						action_buy_price_temp=j[2]
						action_sell_price_temp=j[4]
					if j[1]>=r[5] and j[2]<=r[5] and r[6]>j[4]:
						action_buy_price_temp=r[5]
						action_sell_price_temp=j[4]
					if action_sell_price_temp !='' and action_buy_price_temp !='':
						sql_action=sql_action+"update `order` set status=1 , order_time_trade='"+str(j[6])+"',action_buy_price='"+str(action_buy_price_temp)+"',action_sell_price='"+str(action_sell_price_temp)+"' where orderid='"+str(r[4])+"' ;"
			action_buy_price_temp=""
			action_sell_price_temp=""			
		if sql_action!='':
			cur.execute(sql_action)
			print('have trade!!')
		else:
			print("no trade")
		#print(sql_action)
		conn.commit()
	else:		
		print("haven't trade")

if __name__ == "__main__":
	time1=time.time()
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	cur=conn.cursor()
	cur2=conn.cursor()
	action()
	cur.close()
	conn.close()
	


  # 接到建仓信号，返回建仓成功
  # 判断下一小时内的ln（差额）的最大和最小，如果存在区间内，认为已经操作，如果没有不操作
 #  操作完毕后写入订单,写入卖操作
   #下一小时数据写回到stock库，重新执行stock、result、action

