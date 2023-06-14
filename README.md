# EZsinging

> The current version of this software is a very early version and will continue to be developed

English / [简体中文](https://github.com/xy_cloud/EZsinging/blob/main/README_zh_hans.md)

Sing in the easiest way possible - leave the rest to the computer

`The files in audio_processing are all audio processing functions, but they are not completed, so they are not added to the main program.`

# How to use

## For Developers

use normal mode

    git clone https://github.com/xy-cloud-cn/EZsinging.git
    cd EZsinging
    python main.py

use debug mode(Automatic open devtools)

    git clone https://github.com/xy-cloud-cn/EZsinging.git
    cd EZsinging
    python main.py -debug

## For users

https://github.com/xy-cloud-cn/EZsinging/releases

## Where is the recorded audio

/resources/audio.wav

# How to add plugins

clone repo to plugins folder

# How to add lyrics and music

Copy your music and lyrics files and name them:music.mp3 and lyric.lyc respectively, and place them in the templates/resources folder

But I recommend the plugin [EZsinging-soundsource](https://github.com/xy-cloud-cn/EZsinging-soundsource) even more! It taps into [UnblockNeteaseMusic](https://github.com/UnblockNeteaseMusic) and can automatically search for music to sing!
