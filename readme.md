
# EReputation
[![Python version](https://img.shields.io/badge/python-3.9-blue.svg)](https://python.org)
[![GitHub stars](https://img.shields.io/github/stars/Enzo2991/LReputation.svg)](https://github.com/Enzo2991/LReputation/stargazers)

EReputation, a bot to manage the reputation points of a community in order to promote its good behavior.

## Install

* [Python 3.9+](https://www.python.org/downloads/)

* Install requirements or manual install package
```
pip install -r requirements.txt
```
```
# manual install package
pip install discord-py-interactions
pip install requests
```

* edit config.json
```
  "token": "",
  "ClientId": ,
  "guildId":,
  "rolestaff":[],
  "roleverif":[],
  "SlashCommand": true
```

* in your [developer discord portal](https://discord.com/developers/applications/), go to O2Auth, then in general, activate the scope applications.commands and give it the necessary rights
![Developers portals discord](https://i.imgur.com/bDdNzoE.png)


* Run the bot
```
python main.py
```

## Usage

| Command                       | Action                                                                                                     |
| :---------------------------- | :--------------------------------------------------------------------------------------------------------- |
| `/show`  | allows to show the reputation |
| `/rep`  | gives 1 point of reputation to a player |
| `/reset`  | allows to reset the player's reputation  |
| `/rep-`  | allows you to remove points from a player  |

## Libs
[interactions.py](https://github.com/interactions-py)
