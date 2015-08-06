#!/usr/bin/python
import gensim, logging
import MySQLdb
import re
from gensim.models import Word2Vec
import numpy as np
import nltk
import string
from cStringIO import StringIO
import sys


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
document_list = list();
escape_list = [",","'","`","_","\\","/","+","-","*","(",")"]
if(len(sys.argv)!=5):
	print "Usage : model_output_file_name categ_id start_date end_date"
	sys.exit(-1);

categ_id = sys.argv[2];
start_date =sys.argv[3];
end_date = sys.argv[4];
with MySQLdb.connect("localhost","root","6a5a4a","gmarket",charset = 'utf8') as cursor:
	try:
		cursor.execute("select categ_name from categ where id = %s"%categ_id  );
		product_name = cursor.fetchone()[0]
		cursor.execute("select product_name from `%s` where record_time <= '%s' and record_time <= '%s'"  % (product_name,start_date,end_date)  );
		results = cursor.fetchall();
		#print len(results)
		for result in results:
			temp = result[0]
			for char in escape_list:
				temp = temp.replace(char," ")
			temp = re.sub("\d+"," ",temp)
			document_list.append(temp.lower().encode('utf-8').split())	
		model = Word2Vec(document_list, size=100, window=5, min_count=5, workers=4)
		with open(sys.argv[1],"wb") as fvec:
			for word in model.vocab.keys():
				vec = model[word]
				for i in range(vec.shape[0]):
				 	s = StringIO()
					np.savetxt(s,vec,fmt="%.5f",newline=",")
					fvec.write("%s%s\n" %(s.getvalue(),word))

	except Exception , e:
		print e
