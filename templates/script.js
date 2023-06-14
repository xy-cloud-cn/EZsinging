document.addEventListener('DOMContentLoaded', () => {
    window.addEventListener('pywebviewready', function () {
        window.pywebview.api.load_plugins();
    });
    const lyricsContainer = document.getElementById('lyrics');
    const startButton = document.querySelector('.start');
    const pauseButton = document.querySelector('.pause');
    const audio = document.getElementById('audio');
    const seekBar = document.getElementById('progress');
    const currentTime = document.getElementById('currentTime');
    const duration = document.getElementById('duration');
    let isPlaying = true;
    let isStop = false;
    let lyrics = [];
    let lyricsIndex = 0;
    let currentLyricIndex = -1;

    function loadLyrics(lyricsText) {
        lyrics = parseLyrics(lyricsText);
        renderLyrics(lyrics);
    }

    function parseLyrics(lyricsText) {
        const lines = lyricsText.split('\n');
        const lyrics = [];
        for (const line of lines) {
            const match = line.match(/\[(\d+:\d+\.\d+)\](.*)/);
            if (match) {
                const timestamp = match[1];
                const content = match[2];
                lyrics.push({timestamp, content});
            }
        }
        return lyrics;
    }


    function getCurrentLyric() {
        const currentTime = audio.currentTime;
        for (let i = lyrics.length - 1; i >= 0; i--) {
            if (convertTimestampToSeconds(lyrics[i].timestamp) <= currentTime) {
                return i;
            }
        }
        return -1;
    }

    function renderLyrics(lyrics) {
        const html = lyrics
            .map((lyric, index) => `<div data-timestamp="${lyric.timestamp}">${lyric.content}</div>`)
            .join('');
        lyricsContainer.innerHTML = html;

        const lyricElements = lyricsContainer.querySelectorAll('div[data-timestamp]');
        lyricElements.forEach((element, index) => {
            element.addEventListener('click', () => jumpToTimestamp(index));
        });
    }

    function jumpToTimestamp(index) {
        const timestamp = lyrics[index].timestamp;
        const currentTime = convertTimestampToSeconds(timestamp);
        if (currentTime > audio.currentTime) {
            alert("你还没有完成录音！");
            return;
        }
        audio.currentTime = currentTime;
        window.pywebview.api.rollback_recording(currentTime);
    }

    function convertTimestampToSeconds(timestamp) {
        const [minutes, seconds] = timestamp.split(':');
        return parseInt(minutes) * 60 + parseFloat(seconds);
    }

    function scrollAndHighlightLyric() {
        const currentLyric = getCurrentLyric();
        if (currentLyric !== currentLyricIndex) {
            const lyricsElements = document.querySelectorAll('#lyrics div');
            for (let i = 0; i < lyricsElements.length; i++) {
                lyricsElements[i].classList.remove('highlight');
                lyricsElements[i].classList.remove('animate-shrink');
            }
            if (currentLyric >= 0) {
                lyricsElements[currentLyric].classList.add('highlight');
                lyricsElements[currentLyric].classList.add('animate-shrink');
                lyricsElements[currentLyric].style.transformOrigin = 'left';
                lyricsContainer.scrollTo({
                    top: lyricsElements[currentLyric].offsetTop - lyricsContainer.offsetHeight / 2,
                    behavior: 'smooth',
                });

                const lyricElement = lyricsElements[currentLyric];
                lyricElement.classList.remove('animate-shrink');
            }
            currentLyricIndex = currentLyric;
        }
    }


    function loadLyricsFromFile() {
        fetch('resources/lyric.lyc')
            .then((response) => response.text())
            .then((lyricsText) => {
                loadLyrics(lyricsText);
            })
            .catch((error) => {
                console.error('Failed to load lyrics:', error);
            });
    }

    function updateSeekBar() {
        const progress = (audio.currentTime / audio.duration) * 100;
        seekBar.value = progress;
        currentTime.textContent = formatTime(audio.currentTime);
        duration.textContent = formatTime(audio.duration);
    }

    function formatTime(time) {
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60).toString().padStart(2, '0');
        return `${minutes}:${seconds}`;
    }

    audio.addEventListener('timeupdate', () => {
        isStop = false
        updateSeekBar();
        scrollAndHighlightLyric();
    });
    audio.addEventListener('ended', () => {
        isStop = true
        audio.pause();
        window.pywebview.api.pause_recording();
        pauseButton.innerText = '继续'
        isPlaying = false
        startButton.innerText = '停止'
        startButton.style.display = 'block'
    });
    startButton.addEventListener('click', startButtonClick)

    function startButtonClick() {
        if (isStop) {
            audio.pause();
            window.pywebview.api.stop_recording();
        } else {
            audio.play();
            window.pywebview.api.start_recording();
            startButton.style.display = 'none';
        }
    }

    pauseButton.addEventListener('click', pauseButtonClick)

    function pauseButtonClick() {
        if (isPlaying) {
            audio.pause();
            window.pywebview.api.pause_recording();
            pauseButton.innerText = '继续'
            isPlaying = false
        } else {
            if (audio.currentTime !== audio.duration) {
                audio.play();
                window.pywebview.api.resume_recording();
                pauseButton.innerText = '暂停'
                isPlaying = true
            }
        }
    }

    seekBar.addEventListener('input', () => {
        alert("请不要使用进度条跳转！请点击歌词跳转！")
    });

    loadLyricsFromFile();
});

function openSettingWindow() {
    pywebview.api.open_setting_window();
}
