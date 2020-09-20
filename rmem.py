#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast,datetime
def update_memory(mem):
	with open("mem","w+") as f:
		f.write(str(mem))
		f.close()
try:
	with open("mem","r") as f:
		mem=f.read()
		if mem!="":
			mem=ast.literal_eval(mem)
		else:
			mem={}
			update_memory(mem)
		f.close()
except Exception as e:
	print(e)
	mem={}
	update_memory(mem)
def make_a_newinput(o,f):
	return "<<newinput<"+str(o)+"<,>"+str(f)+">newinput>>"
#anstollerance=0
#exitcommand="exit()"
name="Sobot"
birth="06/10/2017"
def yearsold():
	return "I'm "+str(int(datetime.date.today().year)-int(birth.split("/")[-1]))+"."
def sayhello(args):
	if args==[]:
		return make_a_newinput("Who should I say hello?","sayhello")
	else:
		return "Hello "+", ".join(args)
def setusername(args):
	if args==[]:
		return make_a_newinput("How I have to call you?","setusername")
	else:
		mem["username"]=str(args[0])
		update_memory(mem)
		return "Ok, "+mem["username"]+"."
def showusername():
	if "username" in mem:
		return "Your name is "+mem["username"]
	else:
		return "I don't know."