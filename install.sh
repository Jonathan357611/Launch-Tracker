#!/bin/bash

echo "INFORMATION: It is recommended to run this on a fresh system, as this will, for example, clear your crontabs"
script_dir=$(realpath "$(dirname "$0")")

# Ask the user for input and default to 10 if no input is given
read -p "How often should the script run? (10 minutes): " input
input=${input:-10}

# Use a while loop to validate the input
while ! [[ "$input" =~ ^[1-9][0-9]*$ ]]; do
    read -p "Invalid input. Please enter a non-zero positive integer: " input
done

schedule="*/$input * * * *"
crontab -r
command="/usr/bin/python3 $script_dir/main.py"
echo "$(crontab -l)" | { cat; echo "@reboot $command"; } | crontab -
echo "$(crontab -l)" | { cat; echo "$schedule $command"; } | crontab -

echo "Crontab added!"
echo
echo "All done! If you have any suggestions or find any bugs, report them on github:"
echo "https://github.com/Jonathan357611/Launch-Tracker/"
echo "Thanks for using my program :)"

read -p "In order to run, your raspberry pi has to reboot. Press enter to reboot." input
sudo su -
sudo reboot now