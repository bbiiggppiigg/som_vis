#!/usr/bin/python
import matplotlib.pyplot as plt
import sys
fig = plt.figure()
ax = fig.add_subplot(111)
history = dict()
if( len(sys.argv) !=3 ):
	print "Usage : inputilename outputfilename"
	print len(sys.argv)
	sys.exit(-1);

with open(sys.argv[1],'rb') as fin:
	with open(sys.argv[2],"w") as output:
		output.write('word,x,y\n')
		for line in fin:
			word, x, y = line.strip().split("\t")
			try:
				if(word in history):
					if(int(x)!= history[word][0] or int(y) != history[word][1]):
						print int(x) ,int(y)
				else:		
					ax.text(int(x), int(y), unicode(word.decode('utf-8')))
					history[word] = (int(x),int(y))
					output.write('%s,%d,%d\n'%(word.decode('utf-8').encode('utf-8'),int (x),int (y)));
			except Exception , e:
				print e
				pass
	
