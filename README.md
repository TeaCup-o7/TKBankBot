#Discord NexusTk Bank Bot

Discord NexusTk Bank Bot is a Python 3.11 based web scraper used to track 
changes in individual characters and report them into defined discord channels.

Install

1) Set up a Discord application at https://discord.com/developers/applications
2) Copy your API key from the Discord developer portal for your new application
3) Create a key.py file with a get def to return when called.
def GetKey():
	key = 'api key here'
	return(key)
4) Generate the bot URL with permissions "Read Messages/ View Channels" and "Send Messages"
5) Add the Discord bot to the desired guild where it will report. 
6) Get the desired channel ID that is to recieve update messages.
6.1) Ensure the bot has permissions to read/write in the channel to be reported to.
7) Open the Channels.py and add the character and channel into the dictionary "dicChan".
dicChan = {'character' : [channel ID]}
Note the channel ID must be in a list []
7.1) The bot can handle reporting to multiple channels, to do this simply add more channel ID
into the list. This will cause the bot to report that character's results to multiple channels.
Note the bot must be present in the guild and channel that is to be reported to.
dicChan = {'character' : [channel ID1, channel ID2]}
8) open dbm.py and set the path to where you wish to store the database file.
Example: db = '/home/pi/Desktop/BankerBot2/Inv.db'
9) Ensure the target character has the INVENTORY and BANK options enabled on it's user page.
Note: Missing one or both, will cause the bot to ignore reporting that character.
10) Run main.py

Operation/Use:

The NexusTK Bank Bot will not require user input. The user just has to watch the targeted discord
channel for updates.

Notes on operation:

First run, the bot will not be able to report any changes because it doesn't have data to
compare things to. However, if there are few enough items, it will report from zero.
The bot will: Scrape http://users.nexustk.com/userfiles/YOURUSERNAMEHERE.html every hour.
***The user pages update once an hour.
The bot will: Wait 15 seconds between each scrape and 3 seconds between sending messages in a channel.
*** The bot can handle these operations a lot faster than 15 and 3 seconds. The delay is to not Discord API and webserver
with lots of requests.
Additionally, if the bot runs into a connection issue while scraping a page, it will wait 10 seconds
before trying again until it is successful.
