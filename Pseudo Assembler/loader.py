import re

def load(files, offset):
	f=open(files,'r')
	data=f.read()
	f.close()
	data=data.splitlines()
	for i in range(0,len(data)):
		line=data[i]
		#if(re.match('\r*', line)):
		#	print 'found'
		#	data.remove(line)
	for i in range(0,len(data)):
		line=data[i]
		if line.startswith('J') or line.startswith('LDA') or line.startswith('STA'):
			addr = line.split(' ')[1]
			val=int(line.split(' ')[1])+offset
			data[i]=line.replace(addr,str(val))
	f=open(files.split('.')[0]+'.load','w')
	f.write('\n'.join(data))
	f.close()
	print files.split('.')[0]+'.load file is generated'
