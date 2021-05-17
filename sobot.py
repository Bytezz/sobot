#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,re,ast,random,time,datetime,pyttsx3

try:
	import thread
except:
	import _thread as thread

try:
	import terminal_virtualface as virtualface
	virtualface_enabled=True
except:
	virtualface_enabled=False

from pocketsphinx import LiveSpeech
#import speech_recognition as sr
from rmem import *
from difflib import SequenceMatcher

version="1.1"

def log(txt):
	txt=str(datetime.datetime.now())+" - "+str(txt)
	print(txt)
	with open("log.log","a") as log:
		log.write(txt+"\n")
		log.close()
def similar(a,b):
	try:
		a=encode(a)
	except:
		pass
	try:
		b=encode(b)
	except:
		pass
	return SequenceMatcher(None,a,b).ratio()
def encode(o):
	try:
		o=str(o)
	except:
		pass
	try:
		o=unicode(o,"utf-8")
	except:
		pass
	return o
def voice(txt):
	global voicetts;global voicebusy
	voicetts.say(txt)
	voicebusy=True
	voicetts.runAndWait()
	voicetts.stop()
	voicebusy=False
def face():
	global c
	oldc=c
	while True:
		if c!="":
			oldc=c
		if voicebusy:
			virtualface.face(speak=True)
		else:
			virtualface.face()
		print(oldc)
		time.sleep(.1)
def resultcode(cm,args=[]):
	global brain
	if "|&|" in cm:
		cm=cm.split("|&|")[(random.randrange(0,len(cm.split("|&|"))))]
	if cm.startswith(":goto:") and cm.endswith(":goto:"):
		if cm[6:-6] in brain:
			cm=resultcode(brain[cm[6:-6]],args)
	if cm.startswith("exec%=%") and cm.endswith("%=%exec"):
		exec("cm="+"".join(re.findall('exec%=%(.*?)%=%exec',cm)))
	return cm
def output(o):
	newinput=False
	o=encode(o)
	if o.startswith("<<newinput<") and o.endswith(">newinput>>"):
		newinput=True
		o,f=o[11:-11].split("<,>")
	if executiontype=="lite":
		print(o)
	else:
		voice(o) #thread.start_new_thread(voice,(o,)
	if newinput:
		exec("output("+f+"("+str(sinput().split(" "))+"))")
def sinput():
	if executiontype=="lite":
		o=raw_input("> ")
	else:
		for o in LiveSpeech():
			if o!="":
				break
	###
	# Google speech to text (online)
	#r=sr.Recognizer()
	#with sr.Microphone() as source:
	#	r.adjust_for_ambient_noise(source)
	#	audio=r.listen(source)
	#	try:
	#		o=r.recognize_google(audio)
	#	except Exception as e:
	#		log(e)
	#		o=""
	###
	return encode(o)

global executiontype
if len(sys.argv)>1:
	executiontype=sys.argv[1]
else:
	executiontype=""
global voicetts;voicetts=pyttsx3.init()
global voicebusy;voicebusy=True
try:
	anstollerance
except NameError:
	anstollerance=.65
try:
	exitcommand
except NameError:
	exitcommand="QUIT!"
# load brain
try:
	tbrain=open("brain","r")
	brain=ast.literal_eval(tbrain.read())
	tbrain.close()
except Exception as e:
	log("Brain error: "+str(e))
	brain={}
###
# load face
if virtualface_enabled and executiontype!="lite" and executiontype!="silent":
	thread.start_new_thread(face,())
###
global cm
global c
c=""
if executiontype=="lite":print("'"+exitcommand+"' to exit\n---------------")
if "SWM" in brain:
	cm=resultcode(brain["SWM"])
	output(cm)
while c!=exitcommand:
	args=[]
	c=sinput()
	if c!=exitcommand:
		rawc=c
		c=c.lower()
		if c in brain:
			cm=resultcode(brain[c])
			output(cm)
		else:
			atto=0
			attn=""
			num=0
			cwords=c.split(" ")
			rawcwords=rawc.split(" ")
			for a in brain:
				for n,word in enumerate(cwords):
					ccutted=" ".join(cwords[:len(cwords)-n])
					if similar(ccutted,a)>=anstollerance:
						if similar(ccutted,a)>atto:
							atto=float(similar(ccutted,a))
							attn=a
							args=rawcwords[len(rawcwords)-n:]
			if atto!=0:
				c=attn
				#print(">",c)
				#print("< Args:",args)
				cm=resultcode(brain[c],args)
				output(cm)
			elif "CNFE" in brain:
				cm=resultcode(brain["CNFE"])
				output(cm)
			else:
				output("Command not found.")
	else:
		if "CBM" in brain:
			cm=resultcode(brain["CBM"])
			output(cm)
		else:
			print("Exit...")