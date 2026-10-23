# !!! UNFINISHED & UNMAINTAINED !!!

# Rail Roulette 🚉
### A simple TUI program to randomly pick stations on the Melbourne Metro network + other useful related things.

I have tasked myself with visiting every Melbourne train station served by Metro (I'm hoping to knock one off every couple of weeks or so) but how was I meant to choose which stations to visit? I don't have the braincells for that sort of decision-making, so instead I'm gonna make this program to do that for me and more! (o゜▽゜)o☆

This program is now functional, but I plan on sprucing it up a lot and there may be bugs! If you end up using this lil program and enjoying it, please let me know so I can feel super cool! ヾ(⌐■_■)ノ♪

### The Plan:
- ~~Simple terminal interface (maybe using colours?)~~ - **done!**
- ~~Import and modify a .json file for data storage~~ - **done!**
- ~~Options to reroll if I don't like the choice~~ - **done!**
- ~~Show what line the station is on and it's distance from the CBD/Southern Cross~~ - **done!**
- ~~Counter for how many stations visited/how many remaining, in total and by line (maybe a small hooray msg if a line is completed)~~ **done!**
- ~~Maybe a "queue" that doesn't clear a station until I confirm I visited it?~~ - **done!**
- ~~Option to manually mark a station as visited~~ **done!**
- ~~If a station is served by all lines in a group, display the group name rather than the line names individually to avoid clutter~~ **done!**
- ~~Option to change between accurate and default terminal colours~~ **done!**
- ~~Log date a station was visited (can take user input for this)~~ **done!**
- ~~Option to reset visited station data to default~~ **done!**
- ~~Display which station was queued to be visited in the screen that shows if to_visit contains a value~~ **done!**
- ~~Fix stats screen as it currently displays wonky numbers due to lines sharing stations~~ **done!**
- ~~Look up info on stations~~ **done!**
- Add more info to stations:
    - Station zone
    - Location (suburb)
    - History (date opened, rebuild dates, previous names, etc.)
    - Amount of platforms
    - Preceding/following stations. If station has multiple having a way to display this (maybe have a special character prepending the station names to display this?)
    - Transport links (bus/tram/vline)
    - City loop info (could attach this to group/line instead to avoid useless repeated k:v in json)
    - stopping patterns
    - Station status (premium/host/unstaffed)
    - Misc for other interesting tidbits
- Prettier formatting of nearby PT tables (lay them out nicer if one is much larger than the other)
- A way to look up what stations have been visited (their names)
- fancy TUI using Rich (or Blessing? or Textual?)
- Maybe a GUI eventually?
- More?
 

Please keep in the mind I will most likely forget to keep the above up-to-date. Check the code yourself if it's been a few commits since I messed with this README. If anyone except me is even reading this. I wanna be thrown into a wall by chimera Falin ouuuhghbbghghhh

### Releases:
Standalone .exe releases are generated using the following pyinstaller command: `pyinstaller --noconfirm --onedir --console --name "Rail Roulette"  "main.py"`


### Screenshots:
![Screenshot 2024-07-10 231922](https://github.com/mudkipscience/rail_roulette/assets/37792540/c0c40bf5-82f0-4137-8cc8-a5a8bd59072e)
![Screenshot 2024-07-10 233152](https://github.com/mudkipscience/rail_roulette/assets/37792540/e66cde8e-f9c4-43da-bf62-10a956ee0d6f)
![Screenshot 2024-07-10 233359](https://github.com/mudkipscience/rail_roulette/assets/37792540/19030bc9-dd1c-4a3c-b9b9-56865bbb5bcb)
