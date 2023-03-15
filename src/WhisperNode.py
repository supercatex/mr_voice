#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import rospy
from std_msgs.msg import String
from mr_voice.msg import Voice
from threading import Thread
import whisper
import os


class WhisperNode(object):
    def __init__(self):
        self.topic_audio_path = rospy.get_param("topic_audio_path", "/respeaker/audio_path")
        self.topic_text = rospy.get_param("topic_text", "~text")
        self.lang = rospy.get_param("lang", "en")
        rospy.loginfo("Language: %s" % self.lang)

        self.queue = []
        rospy.Subscriber(self.topic_audio_path, String, self.callback_audio_path)
        self.pub_voice = rospy.Publisher(self.topic_text, Voice, queue_size=10)
        rospy.Rate(1).sleep()
        
        # tiny, base, small, medium, large
        self.sr = whisper.load_model("base", download_root="/home/pcms/models/openai/")
        
        
    def callback_audio_path(self, msg):
        speaking = rospy.get_param("/speaker/is_saying")
        if not speaking:
            self.queue.append(msg.data)
        
    def run(self):
        while True:
            rospy.Rate(5).sleep()
            if len(self.queue) == 0: continue
            
            path = self.queue.pop(0)
            print("%s(%d)" % (path, len(self.queue)))
            
            text = ""
            direction = 0
            try:
                direction = int(path.split(".")[0].split("-")[1])
            except Exception as e:
                rospy.logerr("path error: %s" % e)

            try:
                res = self.sr.transcribe(path, language=self.lang, fp16=False)
                text = res["text"]
                if len(text) > 0:
                    rospy.loginfo("%s: %s" % (path, text))
                    for s in res["segments"]:
                        # print(s)
                        rospy.loginfo("\t%s (%.2f)" % (s["text"], s["no_speech_prob"]))
                    
            except Exception as e:
                rospy.logerr("whisper error: %s" % e)
            
            os.remove(path)
            
            if len(text) > 0:
                voice = Voice()
                voice.time = rospy.Time.now()
                voice.text = text
                voice.direction = direction
                self.pub_voice.publish(voice)
            else:
                rospy.logerr("nothing")
            

if __name__ == "__main__":
    rospy.init_node("voice")
    node = WhisperNode()
    rospy.loginfo(rospy.get_name() + " OK.")
    node.run()
    
