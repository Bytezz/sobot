#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,random,thread
version="0.1.2"
def face(expr="normal",speak=False):
	def clear():
		os.system('cls' if os.name=='nt' else 'clear')
	def height():
		if os.name!="nt":
			return int(os.popen('stty size','r').read().split()[0])
		else:
			return 25
	def width():
		if os.name!="nt":
			return int(os.popen('stty size','r').read().split()[1])
		else:
			return 60
	def lenwidth(perc=50):
		if perc>100:
			perc=100
		elif perc<0:
			perc=0
		return int(width*perc/100)
	def lenheight(perc=50):
		if perc>100:
			perc=100
		elif perc<0:
			perc=0
		return int(height*perc/100)
	def percentage(perc,m):
		return m*perc/100
	def centerwidth(txt):
		return width/2-len(txt)/2
	def printxy(x,y,text):
		sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8"%(y,x,text))
		sys.stdout.flush()
	global width;width=width()
	global height;height=height()
	####
	runners=[]
	#
	eyebrowspos=None
	eyespos=None
	mouthpos=None
	####
	def eyebrows():
		runners.append(1)
		#
		brow="#"*lenwidth(25)
		# brow length, first[x,y], second[x,y]
		pos=[len(brow),[lenwidth(12),lenheight(13)],[width-lenwidth(12)-len(brow),lenheight(13)]]
		printxy(pos[1][0],pos[1][1],brow)
		printxy(pos[2][0],pos[2][1],brow)
		#
		runners.pop(0)
		return pos
	def eyes():
		runners.append(1)
		#
		# left[top left corner[x,y], bottom right corner[x,y]], right[top left corner[x,y], bottom right corner[x,y]],
		pos=[
			[ # left
				[ # top left
					eyebrowspos[1][0]+eyebrowspos[0]-percentage(75,eyebrowspos[0]), # top left x
					eyebrowspos[1][1]+1 # top left y
				],
				[ # bottom right
					eyebrowspos[1][0]+eyebrowspos[0]-percentage(75,eyebrowspos[0])+len("#"+("#"*(percentage(75,eyebrowspos[0])-2))+"#"), # bottom right x
					eyebrowspos[1][1]+lenheight(20) # bottom right y
				]
			],
			[ # right
				[ # tl
					eyebrowspos[2][0], # tlx
					eyebrowspos[2][1]+1 # tly
				],
				[ # br
					eyebrowspos[2][0]+len("#"+("#"*(percentage(75,eyebrowspos[0])-2))+"#"), # brx
					eyebrowspos[2][1]+lenheight(20) # bry
				]
			]
		]
		for i in range(1,lenheight(20)):
			printxy(eyebrowspos[1][0]+eyebrowspos[0]-percentage(75,eyebrowspos[0]),eyebrowspos[1][1]+i,"#"+(" "*(percentage(75,eyebrowspos[0])-2))+"#")
			printxy(eyebrowspos[2][0],eyebrowspos[2][1]+i,"#"+(" "*(percentage(75,eyebrowspos[0])-2))+"#")
		printxy(eyebrowspos[1][0]+eyebrowspos[0]-percentage(75,eyebrowspos[0]),eyebrowspos[1][1]+i+1,"#"+("#"*(percentage(75,eyebrowspos[0])-2))+"#")
		printxy(eyebrowspos[2][0],eyebrowspos[2][1]+i+1,"#"+("#"*(percentage(75,eyebrowspos[0])-2))+"#")
		#
		runners.pop(0)
		return pos
	def eyesdot():
		runners.append(1)
		#
		eyewidth=eyespos[0][1][0]-eyespos[0][0][0]
		eyeheight=eyespos[0][1][1]-eyespos[0][0][1]
		printxy(eyespos[0][0][0]+percentage(50,eyewidth),eyespos[0][0][1]+percentage(50,eyeheight),"#")
		printxy(eyespos[1][0][0]+percentage(50,eyewidth),eyespos[1][0][1]+percentage(50,eyeheight),"#")
		#
		runners.pop(0)
	def nose():
		runners.append(1)
		#
		n="#"*lenwidth(3)+" "*lenwidth(4)+"#"*lenwidth(3)
		printxy(centerwidth(n),lenheight(45),n)
		#
		runners.pop(0)
	def mouth():
		runners.append(1)
		#
		m="#"*lenwidth(50)
		# x, y
		pos=[centerwidth(m),lenheight(70)]
		printxy(centerwidth(m),lenheight(70),m)
		if speak:
			m="#"*lenwidth(25)
			printxy(centerwidth(m),lenheight(random.randint(75,85)),m)
		else:
			m="#"*lenwidth(25)
			printxy(centerwidth(m),lenheight(70)+1,m)
		#
		runners.pop(0)
		return pos
	####
	clear()
	#
	thread.start_new_thread(nose,())
	thread.start_new_thread(mouth,())
	#
	eyebrowspos=eyebrows()
	eyespos=eyes()
	eyesdot()
	#nose()
	#mouthpos=mouth()
	while runners!=[]:
		pass

if __name__=="__main__":
	face()