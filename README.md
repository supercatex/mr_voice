# mr_voice

[![python](https://camo.githubusercontent.com/0e449eedd9902ecde0cacc2e8e0cf4f9cd5b6331cad8556064ddfdd9a29779db/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f4d61726b646f776e2e737667)]()]

1. RespeakerNode.py -- saving raw audio file
   - https://wiki.seeedstudio.com/ReSpeaker_Mic_Array_v2.0/
   - https://github.com/furushchev/respeaker_ros
   ![ReSpeaker Mic Array v2.0](https://files.seeedstudio.com/wiki/ReSpeaker_Mic_Array_V2/img/Hardware%20Overview.png)
   - update firmware
      ```bash
      sudo apt-get update
      sudo pip install pyusb click
      git clone https://github.com/respeaker/usb_4_mic_array.git
      cd usb_4_mic_array
      sudo python dfu.py --download 6_channels_firmware.bin  # The 6 channels version 

      # if you want to use 1 channel,then the command should be like:
      # sudo python dfu.py --download 1_channel_firmware.bin
      ```
   - add udev rules
      ```bash
      sudo cp -f $(rospack find mr_voice)/config/60-respeaker.rules /etc/udev/rules.d/60-respeaker.rules
      sudo service udev restart
      ```

2. SpeechToTextNode.py
   - https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py
   - install packages
      ```bash
      pip install SpeechRecognition
      ```
