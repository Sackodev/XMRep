from pattern import Pattern
from pprint import pprint

class XMReader:
    def __init__(self, fileName):
        self.fileName = fileName
        self.noteDict = {
            '\x81': 'p',
            '\x82': 'i',
            '\x83': 'pi',
            '\x84': 'v',
            '\x85': 'pv',
            '\x86': 'iv',
            '\x87': 'piv',
            '\x88': '1',
            '\x89': 'p1',
            '\x8A': 'i1',
            '\x8B': 'pi1',
            '\x8C': 'v1',
            '\x8D': 'pv1',
            '\x8E': 'vi1',
            '\x8F': 'piv1',
            '\x90': '2',
            '\x91': 'p2',
            '\x92': 'i2',
            '\x93': 'pi2',
            '\x94': 'v2',
            '\x95': 'pv2',
            '\x96': 'iv2',
            '\x97': 'piv2',
            '\x98': '12',
            '\x99': 'p12',
            '\x9A': 'i12',
            '\x9B': 'pi12',
            '\x9C': 'v12',
            '\x9D': 'pv12',
            '\x9E': 'iv12'
        }
        self.patList = []
        self.defaultBPM = None

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
        # 8B = ??? pitch ins fx1
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
        # 97 = pitch, instrument, volume, fx2
        # 98 = Fx1, Fx2
        # 99 = pitch, Fx1, Fx2
        # 9A = instrument, Fx1, Fx2
        # 9B = pitch, instrument, fx1, fx2
        # 9C = volume, Fx1, Fx2
        # 9D = pitch, volume, Fx1, Fx2
        # 9E = instrument, volume, Fx1, Fx2
        # 9F = ???
        # 94 20 CC
        #
        #   noteDict{}
        #
        # Still have to figure out how to tell which pattern is which
        # (some can be dupes at a diff number i think too???)
        #
        #
        #
        #https://www.fileformat.info/format/xm/corion.htm for reference

    def readXM(self):
        # opens the XM file and stores all of it in bytes
        with open(self.fileName, 'rb') as f:
            content = f.read()

            # finds the # of channels used in the song
            numChannel = content[68]

            #finds the BPM
            self.defaultBPM = content[78]
            print(self.defaultBPM)

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
                if((8+spaceCount) < len(content)):
                    endVal = content[8 + spaceCount]
                else:
                    endVal = 0
                print("{}: {}".format("endValue", endVal))

                # checks if the end value is 7 or 9 (end-of-pattern indicators)
                if ((endVal == 9 or endVal == 7)):
                    print("Valid Area!")
                    content = content[8:]

                    j = 0
                    curCh = 0
                    curNote = 0
                    # loop that checks each note individually
                    while(j < spaceCount):
                        # stores a blank if there's no note played
                        if (chr(content[j]) == '\x80'):
                            self.patList[curPat].ch[curCh].addNote(content[j])
                            j += 1
                        # stores note information if it's a note
                        elif chr(content[j]) in self.noteDict:
                            # add stop note
                            if (chr(content[j]) == '\x81' and chr(content[j + 1]) == '\x61'):
                                self.patList[curPat].ch[curCh].addNote(content[j])
                                self.patList[curPat].ch[curCh].notes[curNote].isStop = True
                                j += 2
                            # add any note besides stop
                            else:
                                self.patList[curPat].ch[curCh].addNote(content[j])
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


                        #if note has all settings selected
                        elif (1 <= content[j] <= 96):
                            self.patList[curPat].ch[curCh].addNote(content[j])
                            self.patList[curPat].ch[curCh].notes[curNote].pitch = content[j]
                            self.patList[curPat].ch[curCh].notes[curNote].ins = content[j + 1]
                            self.patList[curPat].ch[curCh].notes[curNote].vol = content[j + 2]
                            self.patList[curPat].ch[curCh].notes[curNote].fx1 = content[j + 3]
                            self.patList[curPat].ch[curCh].notes[curNote].fx2 = content[j + 4]

                            j += 5
                        else:
                            print('Error at value {}, pattern {}, channel {}, note {}! Next 10 values: {}'.format(hex(content[j]), self.patList[curPat].pNum, curCh + 1, curNote +1, content[j:j+9]))
                            print(" Last note: {}".format(dir(self.patList[curPat].ch[curCh - 1].notes[curNote])))
                            print("2nd to last note: {}".format(dir(self.patList[curPat].ch[7].notes[curNote-1])))
                            print(" ")
                            print("{}".format(dir(self.patList[curPat])))
                            print(" ")
                            print(content[j:j+200])
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
