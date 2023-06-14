# -*- coding: utf-8 -*-
import noisereduce as nr
def remove_noise(data,rate):
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    return reduced_noise
