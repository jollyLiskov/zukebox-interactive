#pip3 install youtube-search-python

# maybe needed by curses:
# export TERM=linux
# export TERMINFO=/usr/share/terminfo #for arch linux

from youtubesearchpython import *
import click
import time
import curses
import threading

from config import *
from zukebox_lib import *
 
def inputhandler(str_input):
		"""handle user input and if valid pass to youtube search"""
		helpcommand = ['h', '-h','help', '--help', 'hilfe', 'hilfe?', '?']

		if str_input in helpcommand:
			bottom_window.clear()
			bottom_window.addstr(0, 0, "Suche nach Songs! Alles nach einer # wird vor dem Song vorgelesen")
			bottom_window.addstr(1, 0, "Beispieleingabe: britney spears baby")
			bottom_window.addstr(2, 0, "Danach werden dir Suchergebnisse angezeigt. Wähle mit den Tasten 1 bis 5 einen Song aus")
			bottom_window.addstr(5, 0, "Tipp: Du kannst vor dem Song einen Kommentar vorlesen lassen, wenn du # benutzt!")
			bottom_window.addstr(7, 10, "Beispiel: britney spears baby # alles Gute Melle!")
			bottom_window.addstr(10, 0, "Drücke PRESSANYKEY oder ~ gum zur Suche zurückzukehren!")
			nerdtrap = bottom_window.getkey(0,0) #.decode(encoding="utf-8")
			#bottom_window.refresh()
			#nerdtrap = bottom_window.key(0,0).
			if str(nerdtrap)=='~':
				bottom_window.clear()
				bottom_window.addstr(0, 0, "Hey toll, du hast die Tilde ~ gefunden!")
				bottom_window.addstr(2, 0, "Zur Belohnung darfst du folgendes wissen:")
				bottom_window.addstr(4, 0, "Wenn du \"lang=XX\" eintippst kannst du die Vorlesesprache ändern, dann wird der nächste Kommentar mit lustigem Akzent vorgelesen.")
				bottom_window.addstr(6, 0, "Gültig sind zweistellige Länderkürzel.")
				bottom_window.addstr(8, 0, "Beispiel: \"lang=de\" für Deutsch oder \"lang=it\" für Italienisch.")
				#bottom_window.refresh()
				bottom_window.getkey(1,0)
		
		elif 'lang=' in str_input:
			inputsplit = str_input.split('=', 1)
			try:
				# perform some checks here
				lang=inputsplit[1]
				with open("gttslist.txt") as f:
					langlist = f.read().splitlines() 
				if lang in langlist:
					global ttslang
					ttslang=lang
					bottom_window.addstr(1, 0, "Sprache geändert!",curses.A_BLINK)
				else:
					bottom_window.addstr(1, 0, "Fehler!",curses.A_BLINK)
			except:
				pass
			finally:
				bottom_window.refresh()
				curses.napms(5000)
			
		elif len(str_input) > 3:
			inputsplit = str_input.split('#', 1)
			str_search=inputsplit[0]
			ttsmessage=""
			if len(inputsplit)==2:
				ttsmessage=inputsplit[1]
			yt_search(str_search, ttsmessage)

def yt_search(str_search, ttsmessage=""):
	global ttslang
	search = VideosSearch(str_search, limit=int_max_result)
	curses.flushinp() #clear input buffer
	index = 1
	for video in search.result()['result']:
		bottom_window.addnstr(index+2,10, str(index) + ' - ' + video['title'], num_cols-9)
		bottom_window.refresh()
		index += 1
		if index > int_max_result:
			break
	
	bottom_window.addstr(9, 9, "X - ABBRUCH", curses.A_DIM)
	bottom_window.addstr(11, 0, "Auswahl")
	bottom_window.addstr(11, 8, ">", curses.A_BLINK)
	bottom_window.refresh()
	selection = bottom_window.getstr(11,10,1).decode(encoding="utf-8")
	if (selection == 'x' or selection=='X'):
		bottom_window.clear()
		return
	try:
		if ((int(selection) >=1) and (int(selection) <= int_max_result)):
			#TODO
			# send video link to zuke
			#Post.song(search.result()['result'][int(selection)-1]['link'],ttsmessage,ttslang)
			#bottom_window.addstr(11, 0, "Song wird gesendet...",curses.A_BLINK)
			#bottom_window.refresh()
			#curses.napms(5000)
			#return
		
			index = 0
			for video in search.result()['result']:
				if index == int(selection)-1:
					# send video link to zuke
					Post.song(video['link'],ttsmessage,ttslang)
					bottom_window.addstr(11, 0, "Song wird gesendet...",curses.A_BLINK)
					bottom_window.refresh()
					time.sleep(3)
					#set lang back to "de" ...
					ttslang="de"
					return
				index += 1
		else: raise Exception()
	except:
		bottom_window.clear()
		bottom_window.addstr(11, 0, "Fehlerhafte Eingabe",curses.A_BLINK)
		bottom_window.refresh()
		curses.napms(5000)
		bottom_window.clear()
		yt_search(str_search) # rerun search with search term in case of invalid input
		
		
def top_win():
	### init some things ###
	i=1
	# get size of screen
	sizeX = int(num_lines//2)
	sizeY = int(num_cols)
	midY = sizeY//2
	
	#open top banner from file
	with open("topbanner.txt") as f:
		bannerline = f.read().splitlines() 
	bannerwidth=len(bannerline[1])
	bannerYpos = midY - (bannerwidth//2)
	bannerfillN = sizeY-bannerwidth
	# gerenate filler for banner
	bannerfiller = " "
	bannerchar=" "
	for x in range(bannerfillN//2-1):
		bannerfiller=bannerfiller+bannerchar
	for x in range(7):
		bannerline[x]=bannerfiller+bannerline[x]+bannerfiller
	
	# generate divider between top and bottom window 
	dividechar=" "
	dividestr=dividechar
	for x in range(sizeY-2):
		dividestr=dividestr+dividechar
	
	
	# main loop to update info top window
	while 1:
		#get status info
		playlistN=len(Get.playlist())
		if playlistN>0:
			try: # TODO: more elegant fix
				nextsongtitle=Get.playlist()[0]
			except: 
				pass
		else: nextsongtitle="-"
		
		### draw something
		#Top Banner
		strtime=f"humbly running since {i}s"
		top_window.addstr(0, 0,f"diy_aftershow v1.0 made with =3")
		top_window.addstr(0, sizeY-len(strtime),strtime)
		i+=1
		
		for x in range(7):
			top_window.addstr(x+1, 0, r"%s" % bannerline[x], curses.A_STANDOUT)

		# playerstatus
		top_window.addstr(sizeX-5, 0, "Spielt gerade > %s" % Get.playerstatus()['track']['title'], curses.A_DIM)
		top_window.addstr(sizeX-4, 0, "Nächster Song > %s" % nextsongtitle, curses.A_DIM)
		top_window.addstr(sizeX-3, 0, "Warteschlange > %s" % playlistN, curses.A_DIM)
		# last line
		top_window.addstr(sizeX-1, 0, "%s" % dividestr, curses.A_STANDOUT)
		
		top_window.refresh()
		time.sleep(1)
		top_window.clear()
		#or use erase instead of clear
		#top_window.clrtoeol() #erase to end of line

def fraishandler(): # catch escape key sequence strg+c and other problems
	bottom_window.clear()
	bottom_window.addstr(0, 0, "ERROR! Do you want to exit? y/n ")
	bottom_window.refresh()
	selection = bottom_window.getstr(1,0,1).decode(encoding="utf-8")
	if selection == 'f': # will not work ...
		curses.endwin()
		exit(1) # ... because this raises exception and results in forever loop
	elif selection == 'y':
		bottom_window.clear()
		bottom_window.addstr(0, 0, "lol nice try",curses.A_BLINK)
		bottom_window.refresh()
		time.sleep(5)
		#curses.napms(5000)
	else:
		bottom_window.clear()
		#curses.napms(5000)
	curses.flushinp()


def main():	
	#thread to refresh top window
	topwin_refresh = threading.Thread(target=top_win)
	topwin_refresh.daemon = True
	topwin_refresh.start()
	
	curses.echo() #show user input on screen
	curses.curs_set(0) #de/activate cursor
	#curses.nocbreak() #set input to cooked mode
	#screen.nodelay(True) #do not halt on getstr or getchar
	
	# main loop for searching vids in bottom window
	while 1:
		curses.flushinp()
		try:
			bottom_window.addstr(1, 0, "Suche")
			bottom_window.addstr(1, 6, ">", curses.A_BLINK)
			str_input = bottom_window.getstr(1,10,).decode(encoding="utf-8")
			bottom_window.refresh()
			inputhandler(str_input)
		except:
			pass
			#try: # in case a user presses strg+c again and again continue to loop forever
			#	fraishandler()
			#except:
			#	pass
		bottom_window.clear()
 
screen = curses.initscr()
num_lines, num_cols = screen.getmaxyx()
# lines, columns, start line, start column
top_window = curses.newwin(int(num_lines//2), int(num_cols), 0, 0)
bottom_window = curses.newwin(int((num_lines//2)+1), int(num_cols), int((num_lines//2)), 0)

screen.clear()
screen.refresh()

curses.wrapper(main())
curses.endwin()
