#!/bin/bash

python3 -m pip install empy
python3 -m pip install pyusb click
python3 -m pip install pyttsx3 SpeechRecognition
python3 -m pip install pixel_ring

cd ~
curl -L http://files.portaudio.com/archives/pa_stable_v190700_20210406.tgz > portaudio.tgz
tar -xvzf portaudio.tgz
sudo rm -rf portaudio.tgz

cd ~/portaudio/
./configure
make
sudo make install
python3 -m pip install pyaudio

sudo apt install -y espeak

source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash

cd ~/catkin_ws/src/
git clone https://github.com/supercatex/mr_voice.git

cd ~/catkin_ws/
catkin_make
source ~/catkin_ws/devel/setup.bash

roscd mr_voice
./create_udev_rules

echo "mr_voice installed!"
