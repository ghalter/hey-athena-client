# Hey Athena
[![https://travis-ci.org/hey-athena/hey-athena-client.svg?branch=connor-branch](https://travis-ci.org/hey-athena/hey-athena-client.svg?branch=connor-branch)](https://travis-ci.org/hey-athena/hey-athena-client)
[![PyPI version](https://badge.fury.io/py/heyathena.svg)](https://badge.fury.io/py/heyathena)
[![GitHub license](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://raw.githubusercontent.com/hey-athena/hey-athena-client/connor-branch/LICENSE)

## Overview
Your personal voice assistant.

"Hey Athena" is a 100% open-source, cross-platform, modular voice assistant framework. It aims to do everything that Siri, Cortana, and Echo can do -- and more.

Written in Python 3

Under Development:  
Website: http://heyathena.com  
Documentation: http://pythonhosted.org/HeyAthena/  

## Usage Examples: 
- "Athena *(double beep)* tweet What's good Twitter homies?" (IFTTT key required)
- "Athena *(double beep)* what's the weather like in DFW?" 
- "Athena *(double beep)* what is the capital of Tanzania?"
- "Athena *(double beep)* turn up *(plays music)*" 
- "Athena *(double beep)* open facebook.com" 

Our modular templates make it easy to add new "skills" to Athena. Write a simple Python "skill" module to control your house with your voice. Write a module to post a tweet with your voice. 

Don't like the name "Athena"? Change it to anything you want, like "Swagger Bot" or "Home Slice".

## How can I make my own Athena?
- Download and install Hey Athena using the directions below
- Write your own modules so Athena can respond to different commands

## How can I help?
- Write modules and contribute them by submitting a pull request to this repository
- Find errors and post issues
- If you modify the framework software, submit a pull request
- Give feedback and help us build a community!

## Core Dependencies
- Python 3
- Pocketsphinx (SWIG required in your PATH during installation)
- SpeechRecognition
- Pyglet (AVBin required)
- PyAudio (unofficial windows build: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- gTTS
- PyYAML
- Selenium

## Normal Installation
- Install SWIG (only required to install pocketsphinx and can be removed afterward)
    - Mac: using Homebrew package manager, type `brew install swig`
    - Linux: sudo apt-get install swig
    - Windows: http://www.swig.org/download.html (download swigwin-3.X.X and place swig.exe in your environment PATH)
- Install PyAudio:
    - Mac: `brew install portaudio` `pip install pyaudio`
    - Linux: `sudo apt-get install libasound2-dev libportaudio-dev python3-pyaudio`
    - Windows: `python -m pip install pyaudio`
- Install AVBin:
    - http://avbin.github.io/AVbin/Download.html
- `pip3 install HeyAthena`
- If all goes well, open the Python shell and run `>>> import athena.brain as brain` `>>> brain.start()`
- You can add modules/edit the client in Python's site-packages/athena folder
- Try write your own module using the directions below.

## Developer Installation
- Install SWIG, PyAudio, and AVBin using the directions above
- `pip3 install pocketsphinx pyaudio SpeechRecognition pyglet gTTS pyyaml wolframalpha selenium`
- Clone or download the `hey-athena-client` repository
- Add `C:\path\to\hey-athena-client` to your `PYTHONPATH` system or user environment variable
    - Eclipse (PyDev) has an option for this while importing the project from Git
- `cd hey-athena-client-master\client`
- If all goes well, run `__main__.py`, create a user, say "Athena", and ask her a question!
- Now try write your own module using the directions below.

## Active Modules
An active module is simply a collection of tasks. Tasks look for patterns in user text input (generally through "regular expressions"). If a pattern is matched, the task executes its action. Note: module priority is taken into account first, then task priority.

### Active Module Example
```python
"""
    Finds and returns the latest bitcoin price

    Usage Examples:
        - "What is the price of bitcoin?"
        - "How much is a bitcoin worth?"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.api_library import bitcoin_api

# Only a unique name parameter is required
# See other parameters in athena/classes/module.py
MOD_PARAMS = {
    'name': 'bitcoin',
    'priority': 2,
}

# A task matches text patterns and executes Python code accordingly
class GetValueTask(ActiveTask):
    
	def __init__(self):
		# Give regex patterns to match text input
		super().__init__(patterns=[r'.*\b(bitcoin)\b.*'])
    
		def match(self, text):
		# See if the text matches any pattern
		return self.match_any(text)
    
	def action(self, text):
		# If any pattern matched, speak the bitcoin price
		val = str(bitcoin_api.get_data('last'))
		self.speak(val)

# This is a bare-minimum module
class Bitcoin(Module):
    
	def __init__(self):
		tasks = [GetValueTask()]
		super().__init__(MOD_PARAMS, tasks)
```

### Module Ideas
- Context module (remembers location and important stuff)
- Smart Home API/modules (Hook outlets)
- RESTful API services
- Oauth API
- Canvas module (for college grades/assignments info)
- Gmail (and other google modules)
- Calender (regular)
- Facebook
- Cooking module (hands-free cooking)
- Movies/Showing Times
- Sports-related modules
- Phone Texting (for multiple carriers)
- Text-based Games (zork, etc.)
- Movement (passive, active, API)
- Play music based on mood (and weather)

If you create a module, submit a pull request! We'd love to add it to the repository.
You can also email it to connor@heyathena.com

## Passive Modules
(not implemented yet)

- Passive modules will be scheduled tasks run in the background.
- Useful for notifications (e.g. - Twitter, Facebook, GMail updates).
- Future versions may have event triggers for modules as well.

## Common Errors

**Error:** "no module named athena"  
**Fix:** Make sure the athena project directory is in your PYTHONPATH

**Error:** "AVbin is required to decode compressed media"  
**Fix:** Pyglet needs the avbin.dll file to be installed. On Windows, sometimes the file is wrongfully placed in System32 instead of SysWOW64.
