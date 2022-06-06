# pip install requests json cmd

import requests, json, time, threading
from cmd import Cmd
from config import *
from zukebox_lib import *

url="http://"+str(serveraddress)+":"+str(port)+"/player"

class ZukeShell(Cmd):
	
	def do_status(self, args):
		"""get current player state"""
		print(str(Get.playerstatus()))
	
	def do_p(self, args):
		"""pause or unpause"""
		if Get.playerstatus()["playing"]==False: #player is paused -> press play
			Post.play()
		if Get.playerstatus()["playing"]==True: #stop player
			Post.pause()

	def do_quit(self, args):
		"""Quits the program."""
		print("Quitting.")
		raise SystemExit

	def do_skip(self, args):
		"""Skips the current song."""
		Post.skip()
		print("skipped song")

	def do_add(self, args):
		"""Add youtube url"""
		Post.song(link=args)
		
	def do_volume(self, args):
		"""set volume between 0 and 100"""
		#print(self.args)
		Post.volume(vol=args)
		
	def do_mute(self, args):
		"""mute volume set to 0"""
		Post.volume(vol=0)
	
	def do_ls(self, args):
		"""get playlist"""
		titlelist = Get.playlist()
		n=1
		for i in titlelist:
			print(str(n)+" : "+ i)
			n += 1

	def do_recent(self, args):
		"""get playlist"""
		recentsongs = Get.recenttracks()
		n=1
		for i in recentsongs:
			print(str(n)+" : "+ i)
			n += 1

	def do_rm(self, args):
		"""interactively remove songs from playlist"""
		titlelist = Get.playlist() #get number of songs in playlist
		x = len(titlelist)
		while x>0:
			n=1
			for i in titlelist:
				print(str(n)+" : "+ i)
				n += 1
				
			selection = input('Delete Number or e(xit): ')
			if selection=="e":
				break
			
			try: selection=int(selection)-1 #correction because index startet with 1
			except: print("Eingabefehler")
			else:
				if selection<x:
					confirm = input("Wirklich löschen (y/n):")
					if confirm=="y" or confirm=="j":
						Post.rm(selection, title=titlelist[selection])
				else: print("Kein Song gelöscht.")
			
			titlelist = Get.playlist() #get number of songs in playlist
			x = len(Get.playlist())
	
	def do_save(self, args):
		"""backup playlist and recent tracks to txt file """
		backup()
		
def backup():
	recenttracks=Get.recenttracks()
	with open("recenttracks.txt", "r") as f:
		content = f.read().splitlines()
	diff = list(set(recenttracks) - set(content))
	with open("recenttracks.txt", "a") as f:
		for line in diff:
			f.write(line+"\n")
	#print("recent tracks backed up succesfully")
	
	playlist=Get.playlist()
	if len(playlist)>0:
		t = time.localtime()
		current_time = time.strftime("%H_%M", t)
		playlistfile="playlistbackup/backup_"+current_time+".txt"
		with open(playlistfile, "w") as f:
			for line in playlist:
				f.write(line+"\n")
		#print("backed up playlist to: ", playlistfile)
	#else: print("Playlist empty")
	#print("\n")

def backuploop():
	while 1:
		backup()
		sleep(60)

autobackup = threading.Thread(target=backup)
autobackup.daemon = True
autobackup.start()

if __name__ == '__main__':
	prompt = ZukeShell()
	prompt.prompt = '> '
	prompt.cmdloop('Starting ZukeShell...')
	

