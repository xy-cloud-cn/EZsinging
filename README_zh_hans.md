# EZsinging

> 现在的此软件属于非常早期的版本，会继续保持开发

[English]((https://github.com/xy-cloud-cn/EZsinging/blob/master/README.md)) / 简体中文

尽可能用最简单的方式唱歌--其余的交给电脑处理

`audio_processing中的文件都是音频处理函数，但它们还没有完成，所以没有加入到主程序中。`

# 如何使用

## 对于开发者

使用普通模式

    git clone https://github.com/xy-cloud-cn/EZsinging.git
    cd EZsinging
    python main.py

使用开发者模式( 自动打开调试工具(devtools) )

    git clone https://github.com/xy-cloud-cn/EZsinging.git
    cd EZsinging
    python main.py -debug

## 对于普通用户

https://github.com/xy-cloud-cn/EZsinging/releases

## 录制的音频在哪里？

/resources/audio.wav

# 如何添加插件

克隆对应的插件仓库到 plugins 文件夹

# 如何添加歌词和音乐

复制你的音乐和歌词文件，分别命名为：music.mp3和lyric.lyc，并将它们放在templates/resources文件夹中。

但我更推荐插件[EZsing-soundsource](https://github.com/xy-cloud-cn/EZsinging-soundsource)! 它接入了[UnblockNeteaseMusic](https://github.com/UnblockNeteaseMusic)，可以自动搜索音乐来演唱!
