import shutil
import os
from os import listdir, walk
from os.path import isfile, join

# TODO: copy short songs, covers, mashups
# 
 
# Rename song (Lonely -> Joanie)
# Keep each version (for major versions)

srcDir = "/Users/bencelsi/LocalDrive/MUSIC•••••••••••••••••••••••••/Audio/Bounces/Songs"
destDir = "/Users/bencelsi/LocalDrive/CODE•••••••••••••••••••••••••/github/bencelsi.github.io/music/songs"

# map of SongName to list of bounce files

def copyNewestSongsToDir(src, dest, listName):
    songMap = {}
    for filename in listdir(src):
        if not filename.endswith(".mp3"):
            continue
        filename = filename[:-4]
        tokens = filename.split()
        # print(filename)
        songName = ""
        songNumber = ""
        for token in tokens:
            if (token[0].isdigit() or token[0] == "("):
                if (token[0].isdigit()):
                    songNumber = token
                break
            else:
                songName += token + " "
        songName = songName[:-1]

        if songName not in songMap:
            songMap[songName] = []
        
        songMap[songName].append(filename)
    
    

    # Write to listFile
    listFile = listName + ".js"
    if os.path.exists(listFile):
        os.remove(listFile)
    f = open(listFile, "a")
    f.write("let " + listName + " = [\n")
    
    # Clear src dir
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)

    for songName in songMap:
        maxBounce = songMap[songName][0]
        for bounce in songMap[songName]:
            if (isGreaterThan(bounce, maxBounce)):
                maxBounce = bounce
        print(maxBounce)
        shutil.copyfile(src + "/" + maxBounce +  ".mp3", dest + "/" + songName + ".mp3")
        f.write("\"" + songName + "\",\n")
    f.write("]")
    f.close()

# Next - for each song, find 'newest' version
   
def parseSongNumber(songNumber):
    if (songNumber == -1):
        return (-1, -1, -1)
    tokens = songNumber.split(".")
    number1 = tokens[0]
    if (len(tokens) == 1):
        return (number1, -1, -1)
    tokens = tokens[1].split("-")
    number2 = tokens[0]
    if (len(tokens) == 1):
        return (number1, number2, -1)
    number3 = tokens[1]
    return (number1, number2, number3)

def isGreaterThan(a, b):
    (a1, a2, a3) = parseSongNumber(getNumberFromSong(a))
    (b1, b2, b3) = parseSongNumber(getNumberFromSong(b))
    if a1 == b1 :
        if a2 == b2: 
            if a3 == b3:
                return True
            else:
                return int(a3) > int(b3)
        else:
            return int(a2) > int(b2)
    else:
        return int(a1) > int(b1)

def getNumberFromSong(song):
    splitSong = song.split(" ")
    for i in range(0, len(splitSong)):
        if (splitSong[i][0].isnumeric()):
            return splitSong[i]
    return -1

#print ("\n".join(songMap.keys()))
copyNewestSongsToDir(srcDir, destDir, "all-songs")