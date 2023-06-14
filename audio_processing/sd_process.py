import librosa
import numpy as np
from scipy.spatial.distance import cdist
from scipy.signal import resample
import soundfile as sf

# 读取人声和原音乐文件，转换为单声道，采样率为22050Hz
voice, sr1 = librosa.load('audio.wav', mono=True)
music, sr2 = librosa.load('music.mp3', mono=True)
voice = librosa.resample(voice, orig_sr=sr1, target_sr=sr2)

sr = sr2
# 计算两个音频的长度差
diff = len(voice) - len(music)
# 如果人声比原音乐长，就在原音乐后面补零
if diff > 0:
    music = np.pad(music, (0, diff), 'constant')
# 如果原音乐比人声长，就在人声后面补零
elif diff < 0:
    voice = np.pad(voice, (0, -diff), 'constant')

# 提取人声和原音乐的梅尔频谱特征，用于计算相似度矩阵
voice_mfcc = librosa.feature.mfcc(y=voice, sr=sr, n_mfcc=20)
music_mfcc = librosa.feature.mfcc(y=music, sr=sr, n_mfcc=20)

# 计算相似度矩阵，使用欧氏距离的倒数作为相似度
similarity_matrix = 1 / (1 + cdist(voice_mfcc.T, music_mfcc.T, 'euclidean'))


# 使用动态时间规整算法（dtw）来寻找人声和原音乐的对齐路径
def dtw(similarity_matrix):
    # 初始化累积距离矩阵和回溯矩阵
    accumulated_cost = np.zeros(similarity_matrix.shape)
    backtrack = np.zeros(similarity_matrix.shape, dtype=int)
    # 边界条件
    accumulated_cost[0, 0] = similarity_matrix[0, 0]
    backtrack[0, 0] = -1
    for i in range(1, similarity_matrix.shape[0]):
        accumulated_cost[i, 0] = similarity_matrix[i, 0] + accumulated_cost[i - 1, 0]
        backtrack[i, 0] = 2
    for j in range(1, similarity_matrix.shape[1]):
        accumulated_cost[0, j] = similarity_matrix[0, j] + accumulated_cost[0, j - 1]
        backtrack[0, j] = 1
    # 动态规划递推公式
    for i in range(1, similarity_matrix.shape[0]):
        for j in range(1, similarity_matrix.shape[1]):
            # 选择累积距离最小的方向作为回溯方向
            direction = np.argmin(
                [accumulated_cost[i - 1, j], accumulated_cost[i, j - 1], accumulated_cost[i - 1, j - 1]])
            # 更新累积距离矩阵和回溯矩阵
            accumulated_cost[i, j] = similarity_matrix[i, j] + accumulated_cost[
                i - 1 + direction // 2, j - 1 + direction % 2]
            backtrack[i, j] = direction
    # 回溯寻找对齐路径
    alignment_path = []
    i = similarity_matrix.shape[0] - 1
    j = similarity_matrix.shape[1] - 1
    while backtrack[i, j] != -1:
        alignment_path.append((i, j))
        direction = backtrack[i, j]
        i -= direction // 2
        j -= direction % 2
    alignment_path.append((0, 0))
    alignment_path.reverse()
    return alignment_path


# 调用dtw函数，得到对齐路径
alignment_path = dtw(similarity_matrix)

# 根据对齐路径，调整人声的时间和音高，使其与原音乐匹配
aligned_voice = []
for i, j in alignment_path:
    # 计算人声和原音乐在当前帧的音高比例
    voice_pitch = librosa.hz_to_midi(librosa.feature.rms(y=voice_mfcc[:, i]))
    music_pitch = librosa.hz_to_midi(librosa.feature.rms(y=music_mfcc[:, j]))
    pitch_ratio = music_pitch / voice_pitch if voice_pitch > 0 else 1.0
    print('pitch_ratio:', pitch_ratio)
    pitch_ratio = max(0.5, min(2.0, pitch_ratio))

    # 计算人声在当前帧的采样点数
    voice_frame_length = voice_mfcc.shape[1] * sr // voice_mfcc.shape[0]
    # 提取人声在当前帧的信号
    voice_frame = voice[i * voice_frame_length:(i + 1) * voice_frame_length]
    # 调整人声的音高，使用线性插值法进行重采样
    voice_frame = resample(voice_frame, int(len(voice_frame) * pitch_ratio))

    # 将调整后的人声帧添加到对齐后的人声信号中
    aligned_voice.extend(voice_frame)

# 将对齐后的人声信号转换为numpy数组
aligned_voice = np.array(aligned_voice)

# 保存对齐后的人声信号到文件
sf.write('aligned_voice.wav', aligned_voice, samplerate=sr)

