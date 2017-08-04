import re

pp=0

symbols = {}
symbols_extern = {}
loopend = []
startif = []


def convtoassembly(files):
	code = []
	variable_code = []
	cc=1											#for generating individual 
	pp=1
	loopcount=0
	ifcount=0
	assign=re.compile('var(.*?)=(.*)')				#assigning regular expressions
	ext=re.compile('extern (.*)')					#.*? means the first occurence of ( .(anything) *(any number of times) )
	arith=re.compile('(.*?)=(.*?)[\+\-\&\|](.*?)')
	arith_add=re.compile('(.*?)=(.*?)\+(.*)')
	arith_sub=re.compile('(.*?)=(.*?)\-(.*)')
	arith_or=re.compile('(.*?)=(.*?)\|(.*)')
	arith_and=re.compile('(.*?)=(.*?)\&(.*)')

	for filen in files:								
		f=open(filen,'r')
		data=f.read()								#reading file
		f.close()
		filename=filen.split('.')[0]				#get filename
		symbols[filename]= {}						#dictionary with symbol of each file		
		symbols_extern[filename]= {}				#dictionary with external symbol of each file			
		lines=data.splitlines()						#splitting in lines
		for line in lines:
			line=line.strip()						#remove extra white space
			if assign.match(line):					#if line matches var assign
				asign=line[3:]						#remove var part
				a=re.search(r'(.*?)=(.*)',asign)
				vari = a.group(1).strip()           #takes out variable
				val = a.group(2).strip()			#takes out value
				variable_code.append([vari,val])
				symbols[filename][vari] = 0
				pp += 0

			elif ext.match(line):
				var=line[6:].strip()
				symbols_extern[filename][var]='extern'+var

			elif arith.match(line):
				a=re.search(r'(.*?)=(.*?)[\+\-\&\|](.*)',line)
				if arith_add.match(line):
					op='ADD '
					opi='ADI '
				elif arith_sub.match(line):
					op='SUB '
					opi='SUI '
				elif arith_and.match(line):
					op='ANA '
					opi='ANI '
				elif arith_or.match(line):
					op='ORA '
					opi='ORI '
				vari = a.group(1).strip()
				var1 = a.group(2).strip()
				var2 = a.group(3).strip()
				if var1.isdigit() and var2.isdigit():
					code.append('MVI Areg, '+var1+'\n')
					code.append(opi+var2+'\n')
					code.append('STA '+vari+'\n')
					pp += 3
				elif var1.isdigit():
					code.append('LDA '+var2+'\n')
					code.append('MOV Breg, Areg\n')
					code.append('MVI Areg, '+var1+'\n')
					code.append(op+'Breg\n')
					code.append('STA '+vari+'\n')
					pp += 5
				elif var2.isdigit():
					code.append('LDA '+var1+'\n')
					code.append(opi+var2+'\n')
					code.append('STA '+vari+'\n')
					pp += 3
				else:
					code.append('LDA '+var2+'\n')
					code.append('MOV Breg, Areg\n')
					code.append('LDA '+var1+'\n')
					code.append(op+'Breg\n')
					code.append('STA '+vari+'\n')
					pp += 5

			elif line.startswith('loop'):
				loopcount+=1
				a=re.search(r'loop(.*)',line)
				count=a.group(1).strip()
				code.append('L'+str(loopcount)+' '+'PUSH Dreg\n')				#for nested loops
				code.append('MVI Ereg, '+count+'\n')
				symbols[filename]['L'+str(loopcount)] = pp
				pp += 2
				loopend.append(loopcount)

			elif line.startswith('endloop'):
				code.append('MOV Areg, Ereg\n')
				code.append('SUI 1\n')
				code.append('MOV Ereg, Areg\n')
				code.append('JNZ '+'L'+str(loopend.pop())+'\n')
				code.append('POP Dreg'+'\n')
				pp += 5

			elif line.startswith('if'):
				a=re.search(r'if(.*?)\((.*?)\)',line)					#if (condn)
				cond = a.group(2)
				if '>' in cond:
					ifcount+=1
					a=re.search(r'(.*?)>(.*)',cond)
					var1 = a.group(1).strip()
					var2 = a.group(2).strip()
					code.append('I'+str(ifcount)+' '+'LDA '+var1+'\n')
					code.append('MOV Breg, Areg\n')
					code.append('LDA '+var2+'\n')
					code.append('SUB Breg\n')
					startif.append(ifcount)
					code.append('JP P'+str(ifcount)+'\n')
					code.append('JZ P'+str(ifcount)+'\n')
					symbols[filename]['I'+str(ifcount)] = pp
					pp += 6
				elif '=' in cond:
					ifcount+=1
					a=re.search(r'(.*?)=(.*)',cond)
					var1 = a.group(1).strip()
					var2 = a.group(2).strip()
					code.append('LDA '+var1+'\n')
					code.append('MOV Breg, Areg\n')
					code.append('LDA '+var2+'\n')
					code.append('SUB Breg\n')
					startif.append(ifcount)
					code.append('JNZ P'+str(ifcount)+'\n')
					symbols[filename]['I'+str(ifcount)] = pp
					pp += 5

			elif line.startswith('endif'):
				currif=str(startif.pop())
				code.append('P'+currif+' PASS \n')
				symbols[filename]['P'+currif] = pp
				pp+=1

			else:
				a=re.search(r'(.*?)=(.*)',line)
				var=a.group(1).strip()
				val=a.group(2).strip()
				if val.isdigit():
					code.append('MVI Areg, '+val+'\n')
					code.append('STA '+var+'\n')
					pp += 2
				else:
					code.append('LDA '+val+'\n')
					code.append('STA '+var+'\n')
					pp += 2
		#finding values for each variable for symbol table
		for val in variable_code:
			code.append(val[0]+' '+'DC '+val[1]+'\n')
			symbols[filename][val[0]] =pp
			pp+=1 
		####	
		variable_code=[]
		code.append('\n \n \n')
	code.append('HLT\n')
	filename='concatenated'
	f=open(filename+'.link','w')
	f.write(''.join(code))
	f.close()
	f=open(filename+'.assemble','w')
	f.write(''.join(code))# join concatenates list items to a string
	f.close()
	print filename+'.assemble file generated.'
	print(symbols)
	#print(symbols_extern)
	return symbols
