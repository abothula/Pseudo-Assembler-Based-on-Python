import re,compiler,linker,assembler,loader
files=[]
print 'Enter file names(in descending order of execution):'
while True:
	print 'File Name:',
	fname=raw_input()
	if fname is '':
		break;
	files.append(fname)
main='concatenated'+'.link'  
symbols=compiler.convtoassembly(files)
assembler.pass1(files)
assembler.pass2(files)
linker.link(main, symbols)
print '\nEnter Loading location' 
offset=int(raw_input())
loader.load(main,offset)
