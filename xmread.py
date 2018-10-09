from pattern import Pattern
from pprint import pprint

class XMReader:
    def __init__(self, fileName):
        self.fileName = fileName
        self.noteDict = {
            '\x81': 'p',
            '\x83': 'pi',
            '\x84': 'v',
            '\x85': 'pv',
            '\x87': 'piv',
            '\x88': '1',
            '\x8A': 'i1',
            '\x8D': 'pv1',
            '\x90': '2',
            '\x91': 'p2',
            '\x92': 'i2',
            '\x93': 'piv1',
            '\x94': 'v2',
            '\x95': 'pv2',
            '\x96': 'iv2',
            '\x98': '12',
            '\x99': 'p12',
            '\x9A': 'i12',
            '\x9C': 'v12',
            '\x9D': 'pv12',
            '\x9E': 'iv12'
        }
        self.patList = []

        # 80 = blank note
        #
        # 01-60 = pitch, instrument, volume, Fx1, Fx2 !!no note type value!!
        # 81 = pitch (or stop if pitch value 61)
        # 82 = ???
        # 83 = pitch, instrument
        # 84 = volume
        # 85 = pitch, volume
        # 86 = ??? (Instrument set to 128)
        # 87 = pitch, instrument, volume
        # 88 = Fx1
        # 89 = ??? (Doesn't appear in OpenMPT)
        # 8A = instrument, Fx1
        # 8B = ???
        # 8C = ???
        # 8D = pitch, volume, Fx1
        # 8E = ???
        # 8F = ???
        # 90 = Fx2
        # 91 = pitch, Fx2
        # 92 = instrument, Fx2
        # 93 = pitch, instrument, volume, Fx1
        # 94 = volume, Fx2
        # 95 = pitch, volume, Fx2
        # 96 = instrument, volume, Fx2
        # 97 = ???
        # 98 = Fx1, Fx2
        # 99 = pitch, Fx1, Fx2
        # 9A = instrument, Fx1, Fx2
        # 9B = ???
        # 9C = volume, Fx1, Fx2
        # 9D = pitch, volume, Fx1, Fx2
        # 9E = instrument, volume, Fx1, Fx2
        # 9F = ???
        #
        #
        #   noteDict{}
        #
        # Still have to figure out how to tell which pattern is which
        # (some can be dupes at a diff number i think too???)
        #
        #
        #
        # patternDict
        # each pattern has channels
        # each channel has notes
        # patDict = {}
        # patDict[] = {}
        # patDict[][] = {}
        # patDict[][][] = {}
        # patDict[][][][]
        # patDict[1][2][542]['volume']
        #
        #
        #
        #

    def readXM(self):
        # opens the XM file and stores all of it in bytes
        with open(self.fileName, 'rb') as f:
            content = f.read()

            # finds the # of channels used in the song
            numChannel = content[68]

            # finds when the pattern listing in the file ends
            pattStopNum = content.find(b'\x09\x00\x00')

            patArray = []
            num = 80
            # adds all patterns into array, used for organizing the song later
            while (num < pattStopNum):
                patArray.append(content[num])
                num = num + 1
            print(patArray)

            i = 0
            # creates a dictionary for each pattern
            while(i < len(patArray)):
                if patArray[i] not in self.patList:
                    pNum = patArray[i]
                    self.patList.append(Pattern(pNum, numChannel))
                i += 1

            # checks if there's any patterns left to extract notes from
            curPat = 0
            while(content.find(b'\x09\x00\x00') > -1):
                # stores the start of pattern info
                i = content.find(b'\x09\x00\x00')

                # cuts out old info/pattern stuff we don't need anymore
                content = content[i + 1:]

                # if valid area, row and space counts found at these hexes w/ math
                rowCount = content[4] + (content[5] * 256)
                spaceCount = content[6] + (content[7] * 256)

                print("{}: {}".format("rowCount", rowCount))
                print("{}: {}".format("spaceCount", spaceCount))

                # stores value at end of pattern
                endVal = content[8 + spaceCount]
                print("{}: {}".format("endValue", endVal))

                # checks if the end value is 7 or 9 (end-of-pattern indicators)
                if ((endVal == 9 or endVal == 7) and spaceCount > 0):
                    print("Valid Area!")
                    content = content[8:]

                    j = 0
                    curCh = 0
                    curNote = 0
                    # loop that checks each note individually
                    while(j < spaceCount):
                        # stores a blank if there's no note played
                        if (content[j] == 128):
                            self.patList[curPat].ch[curCh].addNote(b'\x80')
                            j += 1
                        # stores note information if it's a note
                        elif chr(content[j]) in self.noteDict:
                            # add stop note
                            if (hex(content[j]) == b'\x81' and hex(content[j + 1]) == b'\x61'):
                                self.patList[curPat].ch[curCh].addNote(b'\x81')
                                self.patList[curPat].ch[curCh].notes[curNote].isStop = True
                                j += 2
                            # add any note besides stop
                            else:
                                self.patList[curPat].ch[curCh].addNote(hex(content[j]))
                                self.patList[curPat].ch[curCh].notes[curNote].isNote = True
                                self.patList[curPat].ch[curCh].notes[curNote].isStop = False
                                valLib = self.noteDict[chr(content[j])]
                                k = 0
                                while (k < len(valLib)):
                                    valType = valLib[k]
                                    # adds pitch value
                                    if valType == 'p':
                                        self.patList[curPat].ch[curCh].notes[curNote].pitch = content[j + k + 1]
                                    # adds instrument value
                                    elif valType == 'i':
                                        self.patList[curPat].ch[curCh].notes[curNote].ins = content[j + k + 1]
                                    # adds volume value
                                    elif valType == 'v':
                                        self.patList[curPat].ch[curCh].notes[curNote].vol = content[j + k + 1]
                                    # adds Fx1 value
                                    elif valType == '1':
                                        self.patList[curPat].ch[curCh].notes[curNote].fx1 = content[j + k + 1]
                                    # adds Fx2 value
                                    elif valType == '2':
                                        self.patList[curPat].ch[curCh].notes[curNote].fx2 = content[j + k + 1]
                                    k += 1
                                j += len(valLib) + 1
                        else:
                            print('Error at value {} pattern {}!'.format(content[j], curPat))
                            j += 1
                        if (curCh == (numChannel - 1)):
                            curCh = 0
                            curNote += 1
                        else:
                            curCh += 1

                    curPat += 1
                else:
                    print("Invalid Area :(")
                print(content)

                print(" ")

        pprint(vars(self.patList[0].ch[0]))
