import numpy as np
from scipy import signal
import wave
import matplotlib.pyplot as plt

# 1. read the audio file to get wave data
# read audio file recorded
file = wave.open("CW18000.wav", "rb")
# get sampling frequency
sf = file.getframerate()
# get audio data total length
nLength = file.getnframes()
print(nLength)
# read audio data
audioDataRaw = file.readframes(nLength)
# transfer to python list
audioDataRaw = list(audioDataRaw)
# transfer to numpy array
audioDataRaw = np.array(audioDataRaw).astype(np.int8)
# set the data type to int16
audioDataRaw.dtype = "int16"
# calculate audio length in second
audioDataRawTotalTime = nLength/sf
# close the file
file.close()
 
# 2. cut the middle part of the audio data
timeOffset = 2
totalTime = np.int32(np.ceil(audioDataRawTotalTime - timeOffset - 2))
totalPoint = totalTime * sf
timeOffsetPoint = timeOffset * sf
audioData = audioDataRaw[range(timeOffsetPoint, timeOffsetPoint + totalPoint)]


# 3. Recall the key step
# set frequency
freq = 18000
# calculate time t
t = np.arange(totalPoint)/sf
# get cos and -sin used in demodulation
signalCos = np.cos(2 * np.pi * freq * t)
signalSin = -np.sin(2 * np.pi * freq * t)
# get a butteworth filter  带通滤波器
b, a = signal.butter(3, 50/(sf/2), 'lowpass')
# multiply received signal (audioData) and demodulation signal, also apply the filter
signalI = signal.filtfilt(b, a, audioData * signalCos)
signalQ = signal.filtfilt(b, a, audioData * signalSin)
# remove static vector
signalI = signalI - np.mean(signalI)
signalQ = signalQ - np.mean(signalQ)
# calculate the phase angle
phase = np.arctan(signalQ/signalI)
# unwrap the phase angle 
phase = np.unwrap(phase * 2)/2
# calculate the wave length
waveLength = 342/freq
# calculate distance
distance = phase/2/np.pi*waveLength/2

print("distance = " + str(distance))


# plot the generated waveform
plt.figure(1)
plt.plot(t, distance)
plt.show()

# # sampling frequency
# sf = 48000
# # signal time 
# totalTime = 60
# # signal frequency
# freq = 18000
# 
# # generate CW signal 
# totalPoint = sf * totalTime
# # np.arange(n) 生成包含 n 个元素，分别为 0 ~ n-1 的数组
# t = np.arange(totalPoint)/sf
# # 生成 振幅为(65536/2 - 1)，频率为 freq 的 cos 波
# audioData = (65536/2 - 1) * np.cos(2 * np.pi * freq * t)
# audioData = audioData.astype(np.short)
# 
# # save audio file
# file = wave.open("CW18000.wav", "wb")
# file.setnchannels(1)
# file.setsampwidth(2)
# file.setframerate(sf)
# file.writeframes(audioData.tobytes())
# file.close()


# # plot the generated waveform
# # this may cost over 20 seconds
# plt.figure(1)
# plt.plot(t, audioData)
# plt.show()


