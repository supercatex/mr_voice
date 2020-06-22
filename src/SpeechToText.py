#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import speech_recognition as sr
from threading import Thread
import rospy
from std_msgs.msg import String


class SpeechToText(object):
    def __init__(self):
        self.topic_audio_path = rospy.get_param("topic_audio_path", "/respeaker/audio_path")
        self.topic_text = rospy.get_param("topic_text", "~text")
        self.lang = rospy.get_param("lang", "yue-Hant-HK")

        rospy.Subscriber(self.topic_audio_path, String, self.callback_audio_path)
        self.pub_text = rospy.Publisher(self.topic_text, String)

        self.sr = sr.Recognizer()
        self.threads = [] 

    def callback_audio_path(self, msg: String):
        t = Thread(target=self._recognize_thread, args=(msg.data,))
        t.start()

    def _recognize_thread(self, path):
        text = ""
        direction = 0
        try:
            direction = int(path.split(".")[0].split("-")[1])
        except Exception as e:
            rospy.logerr(e.message)

        with sr.AudioFile(path) as source:
            audio = self.sr.record(source)
        try:
            rospy.loginfo(f"recognizing file: {path}")
            text = self.sr.recognize_google(audio, language=self.lang)
        except sr.UnknownValueError:
            rospy.logerr("Voice Recognition could not understand audio")
        except sr.RequestError as e:
            rospy.logerr("Could not request results from Voice Recognition service; {0}".format(e))
        rospy.loginfo(f"{path}: {text}")
        if len(text) > 0:
            self.pub_text.publish(text + "-" + direction)
        else:
            rospy.logerr("nothing")


if __name__ == "__main__":
    rospy.init_node("voice")
    SpeechToText()
    rospy.spin()
