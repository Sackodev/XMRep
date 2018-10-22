from xmread import XMReader
from sampshifter import SampShifter
import wave
import numpy as np

poop = XMReader('Shuric_Scan.xm')
poop.readXM()
#print(poop.patList[-1].ch[-1].notes[-1].type)

sampWav = wave.open('samples/sine-440hz-A4.wav', 'r')
sampFrames = sampWav.getnframes()
sampSRate = sampWav.getframerate()
sampWidth = sampWav.getsampwidth()
sampChannels = sampWav.getnchannels()
sampData = sampWav.readframes(sampFrames)
sampWav.close()

#shifted samples are created here (original sample should be pitched to 440 hz)
SShift = SampShifter('samples/sine-440hz-A4.wav')

trackWav = wave.open('test.wav', 'w')
trackWav.setnchannels(1)
trackWav.setframerate(sampSRate)
trackWav.setsampwidth(sampWidth)
trackWav.setnchannels(2)
trackWav.writeframes(sampData)

trackWav.close()
