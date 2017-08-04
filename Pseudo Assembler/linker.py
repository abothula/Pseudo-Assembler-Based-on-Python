def link(files, symbols):
	var_loc=makeuniversal(symbols)
	#print var_loc
	f=open(files,'r')
	data=f.read()
	f.close()
	data=data.splitlines()
	for i in range(0,len(data)):
		line=data[i]
		if line.startswith('J') or line.startswith('LDA') or line.startswith('STA'):
			variable_name = line.split(' ')[1]
			val=var_loc[variable_name]
			data[i]=line.replace(variable_name,str(val))
	f=open(files,'w')
	f.truncate()
	f.write('\n'.join(data))
	f.close()

	
def makeuniversal(symbols):
	variable_loc={}						#global valriable locations
	for filename in symbols:
		for key,val in symbols[filename].items():
			variable_loc[key]=val
	return variable_loc
