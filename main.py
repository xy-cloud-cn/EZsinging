# -*- coding: utf-8 -*-
# @Author: xy_cloud
import importlib
import json
import threading
import time
import wave
import sys
import os
import pyaudio
import webview

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORDING = False
PAUSED = False
start_time = 0
pause_start_time = 0
paused_duration = 0
device_index = 0
if '-debug' in sys.argv:
    DEBUG_MODE = True
else:
    DEBUG_MODE = False


class SET:

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.device_info = None

    def enumerate_audio_devices(self):
        device_count = self.p.get_device_count()
        devices = []

        for i in range(device_count):
            self.device_info = self.p.get_device_info_by_index(i)
            if self.device_info['maxInputChannels'] > 0:
                devices.append({
                    'index': i,
                    'name': self.device_info['name']
                })

        return devices

    def send_device_index(self, d_index):
        global device_index, RATE, CHANNELS
        device_index = int(d_index)
        deviceinfo = self.p.get_device_info_by_index(device_index)
        print(f"{self.p.get_device_info_by_index(device_index)}")
        RATE = int(deviceinfo['defaultSampleRate'])
        CHANNELS = int(deviceinfo['maxInputChannels'])


def load_plugins():
    plugins_folder = 'plugins/'
    for folder_name in os.listdir(plugins_folder):
        try:
            with open(plugins_folder + folder_name + '/manifest.json', 'r', encoding='utf-8') as f:
                manifest = json.loads(f.read())
        except FileNotFoundError:
            manifest = None
        if manifest is not None:
            if manifest['type'] == 'python':
                if manifest['method'] == 'run':
                    print(
                        (plugins_folder + '.' + folder_name + '.' + manifest['index']).replace('/',
                                                                                                    '').replace(
                            '.py', ''))
                    __import__(
                        (plugins_folder + '.' + folder_name + '.' + manifest['index']).replace('/',
                                                                                                    '').replace(
                            '.py', ''))
class API:
    def __init__(self):
        self.frames = []
        self.RECORDING = False
        self.PAUSED = False
        self.start_time = 0
        self.pause_start_time = 0
        self.device_index = 0
        self.plugins_folder = 'plugins/'

    def load_plugins(self):
        for folder_name in os.listdir(self.plugins_folder):
            try:
                with open(self.plugins_folder + folder_name + '/manifest.json', 'r', encoding='utf-8') as f:
                    manifest = json.loads(f.read())
            except FileNotFoundError:
                manifest = None
            if manifest is not None:
                if manifest['type'] == 'javascript':
                    if manifest['method'] == 'evaluate':
                        if len(manifest['libs']) > 0:
                            for lib in manifest['libs']:
                                if lib.endswith('.css'):
                                    try:
                                        with open(self.plugins_folder + folder_name + lib, 'r',
                                                  encoding='utf-8') as f:
                                            window.load_css(f.read())
                                    except FileNotFoundError:
                                        continue
                                if lib.endswith('.js'):
                                    try:
                                        with open(self.plugins_folder + folder_name + lib, 'r',
                                                  encoding='utf-8') as f:
                                            window.evaluate_js(f.read())
                                    except FileNotFoundError:
                                        continue
                                if lib.endswith('.html'):
                                    try:
                                        with open(self.plugins_folder + folder_name + lib, 'r',
                                                  encoding='utf-8') as f:
                                            window.load_html(f.read())
                                    except FileNotFoundError:
                                        continue
                        try:
                            with open(self.plugins_folder + folder_name + manifest['index'], 'r',
                                      encoding='utf-8') as f:
                                window.evaluate_js(f.read())
                        except FileNotFoundError:
                            continue

    def start_recording(self):
        if self.RECORDING:
            return

        self.start_time = time.time()

        if self.PAUSED:
            self.PAUSED = False

        self.RECORDING = True

        threading.Thread(target=self.record_audio).start()

    def record_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=self.device_index,
                        frames_per_buffer=CHUNK)

        self.frames = []

        while self.RECORDING:
            if not self.PAUSED:
                data = stream.read(CHUNK)
                self.frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        self.save_audio()

    def save_audio(self):
        wf = wave.open("resources/audio.wav", "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(self.frames))
        wf.close()
        window.destroy()
        open_playback()

    def stop_recording(self):
        if not self.RECORDING:
            return

        self.RECORDING = False

    def pause_recording(self):
        if not self.RECORDING or self.PAUSED:
            return

        self.PAUSED = True
        self.pause_start_time = time.time()

    def resume_recording(self):
        if not self.RECORDING or not self.PAUSED:
            return

        self.PAUSED = False

    def rollback_recording(self, seconds):
        if not self.RECORDING:
            return

        frames_to_delete = len(self.frames) - int(seconds * RATE / CHUNK)

        if len(self.frames) > frames_to_delete:
            self.frames = self.frames[:-frames_to_delete]
        else:
            self.frames = []

    def open_setting_window(self):

        threading.Thread(target=open_setting).start()


setting_api = None


def open_setting():
    global setting_api
    # 创建新窗口
    setting_api = SET()
    setting_window = webview.create_window('设置', 'templates/setting/setting.html', width=640, height=480,
                                           resizable=False, js_api=setting_api)
    setting_window.show()

def open_playback():
    pass
    # api = API()
    # playback = webview.create_window('EZsinging', 'templates/window.html', width=640, height=960, resizable=False,
    #                                js_api=api)


# 创建webview窗口，并加载HTML文件
load_plugins()
api = API()
window = webview.create_window('EZsinging', 'templates/window.html', width=640, height=960,
                                           resizable=False, js_api=api)
if DEBUG_MODE:
    webview.start(debug=True)
else:
    webview.start(debug=True)
    # webview.start()

# from audio_processing import *
#
# voice_path = 'test/test.wav'
# song_path = 'test/song.mp3'
# voice, voice_rate = librosa.load(voice_path)
# song, song_rate = librosa.load(song_path)
# # data = remove_noise(data, rate)
# # data = reverb(data, rate)
# data, rate = voice_mod(voice, song, song_rate, voice_rate)
# sf.write("test_output.wav", data, rate)
