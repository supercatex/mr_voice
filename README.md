# mr_voice

1. RespeakerNode.py -- saving raw audio file
- https://wiki.seeedstudio.com/ReSpeaker_Mic_Array_v2.0/
- https://github.com/furushchev/respeaker_ros

![ReSpeaker Mic Array v2.0](https://files.seeedstudio.com/wiki/ReSpeaker_Mic_Array_V2/img/Hardware%20Overview.png)

```bash
sudo cp -f $(rospack find mr_voice)/config/60-respeaker.rules /etc/udev/rules.d/60-respeaker.rules
sudo service udev restart
```

2. SpeechToTextNode.py

https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py
