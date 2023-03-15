#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from TTS.api import TTS
import rospy
from std_msgs.msg import String
import pyaudio
import wave


class Speaker(object):
    def __init__(self):
        model_name = TTS.list_models()[0]
        self.tts = TTS(model_name)
        self.is_running = False
        self.buffer = []
        self.output = "/tmp/output.wav"

    def say(self, message):
        self.buffer.append(message)
        if not self.is_running:
            while len(self.buffer) > 0:
                self.tts.tts_to_file(
                    text = message, 
                    speaker = self.tts.speakers[0], 
                    language = self.tts.languages[0], 
                    file_path = self.output
                )
                self.buffer.pop(0)
                
                self.is_running = True
                f = wave.open(self.output, "rb")
                p = pyaudio.PyAudio()
                s = p.open(
                    format = p.get_format_from_width(f.getsampwidth()),
                    channels = f.getnchannels(),
                    rate = f.getframerate(),
                    output = True
                )
                data = f.readframes(1024)
                while data:
                    s.write(data)
                    data = f.readframes(1024)
                s.stop_stream()
                s.close()
                p.terminate()
                self.is_running = False
            return False
        return True


class SpeakerNode(object):
    def __init__(self):
        self.param_is_saying = "~is_saying"
        self.topic_say = "~say"

        self.speaker = Speaker()

        rospy.set_param(self.param_is_saying, False)
        rospy.Subscriber(self.topic_say, String, self.callback_say)

    def callback_say(self, msg):
        rospy.set_param(self.param_is_saying, True)
        is_saying = self.speaker.say(msg.data)
        rospy.set_param(self.param_is_saying, is_saying)


if __name__ == "__main__":
    rospy.init_node("speaker")
    SpeakerNode()
    rospy.loginfo(rospy.get_name() + " OK.")
    rospy.spin()
    
