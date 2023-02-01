# zukebox_interactive
**Abandoned! There won't be any development, bug fixes or pulls!**

zukebox_interactive is a retro kiosk client for zukebox https://github.com/tomicooler/zukebox

It can be used as a collaborative music playlist, which is called "youtube party" in Germany.

![image](https://user-images.githubusercontent.com/52667770/216048266-dbd1775d-13a7-4ab4-91e7-1cd072d6d60d.png)

This was my very first project and I am not a professional developer and had a tight schedule because it needed to be working for a specific party. So expect some bugs and overall extremely poor code quality.

It was run on a raspberry pi with a monitor and keyboard attached. Zukebox was run on a linux pc in the same LAN Network attached to a sound system.

CAVEAT: You can't interact or exit the kiosk mode so set up a ssh server first!

## Dependencies
requires a working zukebox server (can be run on the same machine e. g. with gnu screen)

requires these python packages:
youtube-search-python
click
```
pip install youtube-search-python click 
```

### Optional Dependencies
#### cool-retro-term
Nice retro / vintage look like in the picture
https://github.com/Swordfish90/cool-retro-term

Note: when using a Raspberry Pi without desktop environment you must start it like this:
```bash
cool-retro-term -platform eglfs
```

#### a second device for zukebox_admin
Since the kiosk can't be exited and e. g. cannot remove songs from the playlist you want to have a second device for zukebox_admin.py

## Run
Clone the Repository and edit config.py with a text editor.

Start zukebox (either same or different device).

Run zukebox_interactive.py (kioskmode)

Optionally run zukebox_admin.py on another device.
