import wave
import os
import numpy as np
from pydub import AudioSegment

class SampShifter:
    def __init__(self, sampFilePath):
        #source for this: https://stackoverflow.com/questions/43963982/python-change-pitch-of-wav-file

        i = 0
        shiftHz = 32.703195662574835 #C0
        while(i < 72):
            fileName = os.path.splitext(os.path.basename(sampFilePath))[0]
            fileName += '-'
            fileName += str(i)
            fileName += '.wav'

            wavPath = "temp/"
            wavPath += fileName

            wr = wave.open(sampFilePath, 'r')
            # Set the parameters for the output file.
            par = list(wr.getparams())
            par[3] = 0  # The number of samples will be set by writeframes.
            par = tuple(par)

            ww = wave.open(wavPath, 'w')
            ww.setparams(par)

            if(i != 0):
                shiftHz = shiftHz * (2**(1/12))

            print(i)
            print(shiftHz)
            shiftHzRounded = int(round(shiftHz, 2))

            if(shiftHzRounded < 440):
                shiftByVal = -440 + shiftHzRounded
            elif(shiftHzRounded > 440):
                shiftByVal = shiftHzRounded - 440
            elif(shiftHzRounded == 440):
                shiftByVal = 0

            fr = 20
            sz = wr.getframerate()//fr  # Read and process 1/fr second at a time.
            # A larger number for fr means less reverb.
            c = int(wr.getnframes()/sz)  # count of the whole file

            shift = shiftByVal//fr  # shifting 100 Hz
            for num in range(c):
                #read data
                da = np.fromstring(wr.readframes(sz), dtype=np.int16)
                #split into left and right channels
                left, right = da[0::2], da[1::2]
                #Extract frequencies using Fast Fourier Transform built into numpy
                lf, rf = np.fft.rfft(left), np.fft.rfft(right)
                #Rolls array to increase pitch
                lf, rf = np.roll(lf, shift), np.roll(rf, shift)
                #Gets rid of the sound made from the highest frequencies rolling over to the lowest ones??
                #lf[0:shift], rf[0:shift] = 0, 0 Don't need this???
                #Inverse the FFT to convert the signal back to amplitude
                nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
                #Combine the two channels
                ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
                #Write output data
                ww.writeframes(ns.tostring())
            wr.close()
            ww.close()
            i += 1

        #Source for this part: https://stackoverflow.com/questions/42492246/how-to-normalize-the-volume-of-an-audio-file-in-python-any-packages-currently-a

        #might want to increase the low pitch dB and lower the high pitch dB later
        i = 0
        while (i < 64):
            fileToNorm = 'temp/'
            fileToNorm += os.path.splitext(os.path.basename(sampFilePath))[0]
            fileToNorm += '-'
            fileToNorm += str(i)
            fileToNorm += '.wav'

            sound = AudioSegment.from_file(fileToNorm, "wav")

            wanted_dBFS = -5
            change_in_dBFS = wanted_dBFS - sound.dBFS
            normalizedSound = sound.apply_gain(change_in_dBFS)
            normalizedSound.export(fileToNorm, format="wav")
            i += 1
