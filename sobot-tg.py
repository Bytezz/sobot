#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,re,time,datetime,ast,random
try:
	import urllib.request as urllib
except:
	import urllib
try:
	import thread
except:
	import _thread as thread
from rmem import *
from difflib import SequenceMatcher

version="1.1"

def similar(a,b):
	return SequenceMatcher(None,a,b).ratio()
def epoch():
	return time.time()
def readurl(url):
	page=urllib.urlopen(url)
	content=page.read()
	page.close()
	return content
def snd(chat_id,text):
	global token
	global newinputs
	if text.startswith("<<newinput<") and text.endswith(">newinput>>"):
		text,f=text[11:-11].split("<,>")
		text=resultcode(text)
		newinputs[chat_id]=f
	try:
		result=readurl("https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+chat_id+"&text="+str(text))
		if '"error_code":403' in errorcont:
			print("User blocked the bot.")
			rmuser(chat_id)
	except Exception as e:
		log(e)
def log(t):
	t=str(datetime.datetime.now())+" - "+str(t)
	print(t)
	if not os.path.isfile("tg-log.log"):
		log=open("tg-log.log","w+")
		log.close()
	with open("tg-log.log","a") as log:
		log.write(str(t)+"\n")
		log.close()
def adduser(uid):
	if not os.path.isfile("subs.txt"):
		subf=open("subs.txt","w+")
		subf.close()
	with open("subs.txt","r") as subf:
		subs=subf.read()
		subf.close()
	subs=subs.split("\n")
	if not uid in subs:
		with open("subs.txt","a") as subf:
			subf.write(str(uid)+"\n")
			subf.close()
def rmuser(uid):
	with open("subs.txt","r") as subf:
		subs=subf.read()
		subf.close()
	subs=subs.split("\n")
	if uid in subs:
		for i,sub in enumerate(subs):
			if sub==uid:
				subs.pop(i)
		with open("subs.txt","w+") as subf:
			subf.write("\n".join(subs)+"\n")
			subf.close()
def resultcode(cm,args=[]):
	global brain
	if "|&|" in cm:
		cm=cm.split("|&|")[(random.randrange(0,len(cm.split("|&|"))))]
	if cm.startswith(":goto:") and cm.endswith(":goto:"):
		if brain.has_key(cm[6:-6]):
			cm=resultcode(brain[cm[6:-6]],args)
	if cm.startswith("exec%=%") and cm.endswith("%=%exec"):
		exec("cm="+"".join(re.findall('exec%=%(.*?)%=%exec',cm)))
	return cm
def elaborate(d):
	global brain
	global token
	global lastsendid
	global lui
	args=[]
	c=""
	text=""
	lui=d["update_id"]
	fileid=str(epoch())+str(random.randint(1000,9999))
	if "message" in d:
		chat_id=str(d["message"]["chat"]["id"])
		if "username" in d["message"]["from"]:
			user="@"+d["message"]["from"]["username"]
		elif "first_name" in d["message"]["from"]:
			user=d["message"]["from"]["first_name"]
		else:
			user=str(d["message"]["from"]["id"])
		try:
			adduser(chat_id)
			log(user+" used me.")
		except Exception as e:
			log(e)
		if "text" in d["message"]:
			if d["message"]["text"]!="":
				c=d["message"]["text"]
				if "\\u" in c:
					c=c.decode("unicode-escape")
					c=c.encode("utf-8")
				rawc=c
				c=c.lower()
				if chat_id in newinputs:
					exec("snd("+chat_id+","+newinputs.pop(chat_id)+"("+str(rawc.split(" "))+"))")
				else:
					if c=="/start":
						c="SWM"
					elif c=="/loggol": # and user=="@admin"
						with open("tg-log.log","r") as logf:
							snd(chat_id,"\n".join(logf.read().split("\n")[-50:]))
							logf.close()
					elif c=="/subus": # and user=="@admin"
						with open("subs.txt","r") as subs:
							snd(chat_id,len(subs.read().split("\n")))
							subs.close()
					if brain.has_key(c):
						cm=resultcode(brain[c])
						if cm!="":
							snd(chat_id,cm)
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
							tmpc=c
							c=attn
							#snd(chat_id,"> "+str(c))
							cm=resultcode(brain[c],args)
							if cm!="":
								snd(chat_id,cm)
						elif brain.has_key("CNFE"):
							cm=resultcode(brain["CNFE"])
							if cm!="":
								snd(chat_id,cm)
						else:
							snd(chat_id,"Command not found.")
		else:
			if brain.has_key("CNFE"):
				snd(chat_id,resultcode(brain["CNFE"]))
	#elif "inline_query" in d:
	#	if "username" in d["inline_query"]["from"]:
	#		user="@"+d["inline_query"]["from"]["username"]
	#	elif "first_name" in d["inline_query"]["from"]:
	#		user=d["inline_query"]["from"]["first_name"]
	#	else:
	#		user=str(d["inline_query"]["from"]["id"])
	#	iid=d["inline_query"]["id"]
	#	c=d["inline_query"]["query"]
	#	print("inline_query: "+c)
	#	laq="https://api.telegram.org/bot"+token+"/answerInlineQuery?id="+iid+"&results=type=article,title=Test,message_text=Test."
	#	print(laq)
	#	print(readurl(laq))
try:
	anstollerance
except NameError:
	anstollerance=0.65
global brain
tbrain=open("brain","r")
brain=ast.literal_eval(tbrain.read())
tbrain.close()
c=""
global token
global lastsendid
global lui
global newinputs
token=""
lastsendid={}
lui=0
newinputs=[]
stat='{"ok":true,"result":[]}'
running=True
while running:
	time.sleep(.5)
	try:
		ns=readurl("https://api.telegram.org/bot"+token+"/getUpdates?offset="+str(lui+1))
		if ns!=stat:
			da=ns.replace("\n","")
			da=da.replace('false','False').replace("true","True")
			#stat=ns
			da=ast.literal_eval(da)
			if "result" in da:
				for d in da["result"]:
					try:
						thread.start_new_thread(elaborate,(d,))
					except Exception as e:
						log(e)
	except Exception as e:
		log(e)