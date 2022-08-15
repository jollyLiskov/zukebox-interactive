import requests, json
#from cmd import Cmd
from config import * 

url="http://"+str(serveraddress)+":"+str(port)+"/player"

class Get():
	def request(address):
		try:
			r = requests.get(address)
			zukejson = json.loads(r.text)
		except:
			zukejson = {}
			zukejson["tracks"] = [{"title":"CONNECTION ERROR"}] #tracks as list of dic is uses by playlist and recent
			zukejson["track"] = {"title":"CONNECTION ERROR"} #track as dic is used by playerstatus
		finally:
			return zukejson

	def playerstatus():
		playerstate=Get.request(url+"/control")
		return playerstate
	
	def playlist():
		playlist=Get.request(url+"/tracks")
		titlelist = []
		for i in playlist["tracks"]:
			titlelist.append(i["title"])
		return titlelist #return list of titles
	
	def recenttracks():
		playlist=Get.request(url+"/recent-tracks")
		recentlist = []
		for i in playlist["tracks"]:
			recentlist.append(i["title"])
		return recentlist #return list of titles
		
class Post():
	def pause():
		requests.patch(url+"/control", json={'playing': False}, headers={'Content-Type': 'application/json'})
	
	def play():
		requests.patch(url+"/control", json={'playing': True}, headers={'Content-Type': 'application/json'})
	
	def volume(vol):
		data={'volume': int(vol)}
		requests.patch(url+"/control", json=data, headers={'Content-Type': 'application/json'})
	
	def time(sec):
		data={'time': int(sec)}
		requests.patch(url+"/control", json=data, headers={'Content-Type': 'application/json'})
		
	def skip():
		duration=Get.playerstatus()['track']['duration']
		if duration > 0:
			Post.time(sec=duration-1)
	
	def song(link, ttsmessage="", ttslang=ttslang):
		data={
			"user": "server",
			"url": link,
			"message": ttsmessage,
			"lang": ttslang
			}
		requests.post(url+"/tracks", json=data, headers={'Content-Type': 'application/json'})

	def rm(n, title):
		# check if track index did not change since user input
		r = requests.get(url+"/tracks/"+ str(n))
		rmtitle=json.loads(r.text)
		if title==rmtitle["title"]:
			requests.delete(url+"/tracks/"+str(n))
			return 1
		else: return 0
	
