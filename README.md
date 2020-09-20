# Sobot
Simple modular algorithm to make bots in a easy way.  
With a simple file of text can be created an input output bot.

# Applications
Sobot can be used to make:
- InfoBox, to give information to people for example in a tourist place.
- Simple chat bot.
- Customer service bot.
- FAQ bot.
- Vocal/textual assistant.

# How it works
Sobot it's based on 2 file plus 2 optional:  

- The main file (sobot.py), which makes the bot works.
- The brain (brain), that contains all the commands with the response.
- The Read only MEMory (rmem.py), that contains vars and functions (optional).
- The memory (mem), that contains editable vars which are stored (optional).

# Get started

## Sobot
The main file (sobot.py) has to be edited only if you want contribute to improve Sobot.  
sobot-tg.py it's sobot.py for telegram's bot.  
Sobot can be executed in 3 ways:

- Normal way, just execute it.
- `lite`, only text.
- `silent`, nothing is shown.

To choose has to be passed an arg:  
`./sobot.py lite`

## Brain
To make a bot with Sobot, has to be written the brain.

### Basics
The brain it's only a python's dictionary in a text file which get loaded inside the main file:  
```python
{
"say hello":"Hello, World!",
'hi':':goto:say hello:goto:'
}
```
This is a simple example of how a brain it's written. All it's between "{" and "}", each command
it's inside " or ' and the respective answer after ":" and also inside " or '. After every answer
must be put a comma (",") (at the last line it's optional).
Outside the " and the ', the code can have spaces, tabs and new lines.

### Commands
Brain have its own commands to work:

- `|&|`
- `:goto:`
- `exec%=%`

"|&|" it's used to put more answer to one command, will be returned only one randomly selected.  
":goto:" call another command, must be put at the start and at the end of name of command to call.  
"exec%=%" will execute python code, must be put at the start (exec%=%) and at the end (%=%exec). Can be used to call rmem.py functions.

## Read only MEMory (rmem.py)
Here there are all the functions which the bot can execute and all the vars (that will be restored on restart).

### Special vars
In rmem.py there are some vars that declared can be used to customize the bot's settings:

- `anstollerance`, which sets the tollerance for commands detection (float, default: .65).
- `exitcommand`, that sets the command to exit from the bot (string, default: "QUIT!").

### Arguments
To commands can be passed args (as array). To get args in functions in rmem.py, put "args" as arg for function.
```python
def example(args):
	return ", ".join(args)
```

### Special returns
Special returns are codes in return value of rmem.py's functions which say what to do to Sobot:

- `"<<newinput<WHAT BOT HAVE TO SAY<,>FUNCTION TO RUN>newinput>>"`, this is useful to get args in a function that needs args and no one
is given. "WHAT BOT HAVE TO SAY" it's what the bot have to ask to user to get args and "FUNCTION TO RUN" it's the name of the function
to send args.
```python
def example(args):
	if args==[]:
		return "<<newinput<Insert args.<,>example>newinput>>"
	else:
		return ", ".join(args)
```

## Memory (mem)
Memory it's the same as brain: a python's dictionary inside a text file.  
mem it's a place where vars are stored with read and write access, usually by rmem.py.
To use mem, has to be laoded into rmem.py
```python
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
```

## Bonus
Inside sobot.py there are code commented about the using of Google speech to text, which is more accurate but needs an internet connection
and may result in privacy issue (regard Google).

## Example
In the repo it's available an example of how to use Sobot.  
Check "brain", "rmem.py" and "mem".

***

[License](LICENSE)  
[Developer](https://github.com/Bytezz)