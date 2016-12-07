"""
RLauncher by pydlv
12/6/16

This is just an attempt at a launcher for Roblox player in Python.
"""

import os;
os.chdir(os.path.dirname(os.path.realpath(__file__)));

import requests;
from settings import settings;
import json;
import sys;
import random;
import subprocess;

print("RLauncher by pydlv");

def get_immediate_subdirectories(a_dir):
	return [name for name in os.listdir(a_dir)
		if os.path.isdir(os.path.join(a_dir, name))]

versionsPath = os.getenv("LOCALAPPDATA") + "/Roblox/Versions";
try:
	dirNames = get_immediate_subdirectories(versionsPath);
except FileNotFoundError:
	print("Could not locate any versions of Roblox. Please make sure it's installed.");
	sys.exit(1);

dirNames.sort(key=lambda n: int(n.split("-")[1], 16));

if(len(dirNames) < 1):
	print("Could not locate any versions of Roblox. Please make sure it's installed.");
	sys.exit(1);

robloxPath = versionsPath + "/" + dirNames[0];

print("Logging in as %s..." % settings["Authentication"]["username"]);

session = requests.Session();

#Comment out to require authentication with .ROBLOSECURITY
request = session.post("https://www.roblox.com/newlogin", data = {"username": settings["Authentication"]["username"], "password": settings["Authentication"]["password"], "submitLogin": "Log In"});

#Check if login was successful
try:
	if "errors" in json.loads(session.get("https://api.roblox.com/currency/balance").text):
		raise ValueError;
	print("Login successful.");
except ValueError:
	print("Could not login with credentials. Attempting to authenticate with .ROBLOSECURITY cookie.");
	requests.utils.add_dict_to_cookiejar(session.cookies, {".ROBLOSECURITY": settings["Authentication"]["roblosecurity"].strip()});
	try:
		if "errors" in json.loads(session.get("https://api.roblox.com/currency/balance").text):
			raise ValueError;
		print("Login successful with .ROBLOSECURITY.");
	except ValueError:
		print("Failed to login with .ROBLOSECURITY.\n\nMake sure 2-factor authentication is off, or provide a valid .ROBLOSECURITY cookie.");
		sys.exit(1);

prejoin = None;

if(len(sys.argv) == 2):
	try:
		prejoin = int(sys.argv[1]);
	except ValueError:
		pass;

while(True):
	if(not prejoin):
		try:
			placeId = int(input("Enter place ID to join: "));
		except ValueError:
			continue;
	else:
		placeId = prejoin;
		prejoin = None;

	ticket = session.get("https://www.roblox.com/game-auth/getauthticket", headers={"Referer": "https://www.roblox.com/games/%i/pydlv" % placeId}).text;
	
	subprocess.call("\"%(path)s/RobloxPlayerBeta.exe\" --play -a https://www.roblox.com/Login/Negotiate.ashx -t %(ticket)s -j https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGame&browserTrackerId=%(browserTracker)i&placeId=%(placeId)i&isPartyLeader=false -b %(browserTracker)i" % {"path": robloxPath, "ticket": ticket, "placeId": placeId, "browserTracker": random.randint(1111111, 9999999)});

	if(len(sys.argv) == 2):
		sys.exit(0);