# -*- coding: utf-8 -*-
import numpy as np
import pyroomacoustics as pra
def reverb(wav_data,rate):
    room_dim = [5, 5, 5]
    source = [2.5, 2.5, 4]
    mic = [2.5, 2.5, 3]
    room = pra.ShoeBox(room_dim,max_order=8)
    room.add_source(source, signal=wav_data)
    room.add_microphone(mic)
    room.compute_rir()
    room.simulate()
    reverb_data = room.mic_array.signals
    reverb_data = reverb_data.flatten()
    reverb_data = reverb_data / np.max(np.abs(reverb_data))
    return reverb_data
