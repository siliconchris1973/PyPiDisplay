**PyPiDisplay [pronounced püpidisplay]**


PyPiDisplay is a very tiny Python Flask Application that aims to proivide an 
easy way of displaying various stuff on very tiny displays.

Currently it supports:
* Nokia5110 via Adafruit LCD Library
* Dummy Display, which does not output on any device but only provides the web interface

**Python 2 vs. Python 3**

The Adafruit library I use to drive the Nokia5110 tiny LCD display is designed to be used with Python2. In case you want to drive a Nokia5110 display with PyPiDisplay an Python3 you need to make sure to adapt the PCD8544 library.
 
 In this file at or around line 172 in function 'clear', there is a statement like this:
 
    self._buffer = [0] * (LCDWIDTH * LCDHEIGHT / 8)
    
You will need to change this to read

    self._buffer = [0] * int((LCDWIDTH * LCDHEIGHT / 8))

I included a modified PCD8544.py in package ShowStuff to already incorporates this change.

**Installation**

To make it run check it out from github

    git clone https://github.com/siliconchris1973/PyPiDisplay

cd into directory

    cd PyPiDisplay

install all requirements

    pip install -r requirements.txt

check the wiring in __setup__.py

and start the app

    python3 app.py

enjoy - at least the very little stuff there is to enkoy :-)

Send feedback/issues/bugs to

   chris dot guenther at mac dot com


