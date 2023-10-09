import numpy as np
import wave
import matplotlib.pyplot as plt

# sampling frequency
sf = 48000
# signal time 
totalTime = 60
# signal frequency
freq = 18000

# generate CW signal 
totalPoint = sf * totalTime
# np.arange(n) 生成包含 n 个元素，分别为 0 ~ n-1 的数组
t = np.arange(totalPoint)/sf
# 生成 振幅为(65536/2 - 1)，频率为 freq 的 cos 波
audioData = (65536/2 - 1) * np.cos(2 * np.pi * freq * t)
audioData = audioData.astype(np.short)

# save audio file
file = wave.open("CW18000.wav", "wb")
file.setnchannels(1)
file.setsampwidth(2)
file.setframerate(sf)
file.writeframes(audioData.tobytes())
file.close()

# plot the generated waveform
# this may cost over 20 seconds
plt.figure(1)
plt.plot(t, audioData)
plt.show()



