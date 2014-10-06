import threading
import urllib
import urllib.request
import csv
import pymysql
import time


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

	pearson_1=[1,1,1.01,1,3]
	pearson_2=[1.01,1.01,2,1.01,1.01]
	print(pearson(pearson_1,pearson_2))