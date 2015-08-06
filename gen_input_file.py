#!/usr/bin/python
import MySQLdb
import re
import sys
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
document_list = list();
escape_list = [",","'","`","_","\\","/","+","-","*","(",")"]

with MySQLdb.connect("localhost","root","6a5a4a","gmarket",charset = 'utf8') as cursor:
	try:
		cursor.execute("select categ_name , id from categ ");
		categ_rs = cursor.fetchall()
		cursor.execute("select record_time from date_list ");
		date_rs = cursor.fetchall()
		for categ_row in categ_rs:
			categ_name = categ_row[0]
			categ_id = categ_row[1]
			for i in range(len(date_rs)):
				start_date = date_rs[i][0];
				for j in range(i,len(date_rs)):
					end_date = date_rs[j][0];
					print start_date , end_date , categ_name
					for map_size in (100,200,300):
						with open("in/categ%s_%s_%s_%d.in"%(categ_id,start_date,end_date,map_size),"w") as inputFile:
							inputFile.write("%s\n%s\n%s\n%d\n"%(categ_id,start_date,end_date,map_size));

	except Exception , e:
		print e
