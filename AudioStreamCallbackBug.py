import pyaudio
import wave

def callback_stream(in_data, frame_count, time_info, status):
    return None, pyaudio.paContinue

 
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

RESPEAKER_INDEX = -1
for i in range(0, numdevices):
    device = p.get_device_info_by_host_api_device_index(0, i)
    print "Input Device id %2d - (%4d) - %s" % (i, device.get('maxInputChannels'), device.get('name'))
    if "ReSpeaker" in device.get('name') and device.get('maxInputChannels') > 0:
        RESPEAKER_INDEX = i


RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 6 # change base on firmwares, 1_channel_firmware.bin as 1 or 6_channels_firmware.bin as 6
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
# RESPEAKER_INDEX = 5  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
 
p = pyaudio.PyAudio()
 
stream = p.open(
            rate=RESPEAKER_RATE,
            format=p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            input_device_index=RESPEAKER_INDEX,
            frames_per_buffer=1024,
            stream_callback=callback_stream)
 
print("* recording")
 
frames = []
 
for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
 
print("* done recording")
 
stream.stop_stream()
stream.close()
p.terminate()
 
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(RESPEAKER_CHANNELS)
wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
wf.setframerate(RESPEAKER_RATE)
wf.writeframes(b''.join(frames))
wf.close()
