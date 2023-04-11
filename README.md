# Launch-Tracker

This is my new version of my old [SpaceX-Tracker](https://github.com/Jonathan357611/SpaceX-Launch-Tracker), which just showed SpaceX-Launches as the name implies. Reason is that the r/SpaceX-API has been discontinued.
The new version uses the https://thespacedevs.com/ API. One advantage is, that the program is now able to receive all rocket launches.

Here is an image of what it looks like
![IMG_20230411_134614](https://user-images.githubusercontent.com/63909127/231153512-ae863d13-a6f3-4a26-84c7-fb4e7c42f18b.jpg)

# Hardware

This project utilizes the Raspberry Pi Zero W and a 2.13" Dual-Color (Black/Red in my case) E-Ink display from Waveshare. [This](https://www.waveshare.com/2.13inch-e-paper-hat-b.htm) is the exact one I bought.

# Install

It is recommended to install this on a fresh debian-install on the Raspberry Pi Zero (Not tested on V2!).

To install, just SSH into your Pi and run these commands:

First, make sure your system is up to date and you have git installed

```bash
sudo apt update && sudo apt install git
```

Then run this, it clones the remote repo onto your machine.

```bash
git clone https://github.com/Jonathan357611/Launch-Tracker.git
```

To simplify things, I created a simple installer, this will automatically add the required cronjobs to run the script every few minutes after boot for you.
It just asks you how often you want to let it run (default=10minutes).

```bash
cd Launch-Tracker
./install.sh
```

That's really it. The program should now periodically start :)
If you encounter any issues or have any ideas, just report them here!
