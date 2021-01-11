#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/Spacebot2
tmux new-session -d -s SpaceBot 'python3 spacebot2.py'
cd /
