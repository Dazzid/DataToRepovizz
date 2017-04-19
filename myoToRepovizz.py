import sys
import os
from xmlCreator import xml
from os import listdir
from os.path import isfile, join
from collections import defaultdict

def main(argv):
    fn = sys.argv[1]
    myLocalPath = os.path.abspath(sys.argv[0])
    head, tail = os.path.split(os.path.split(myLocalPath)[0])
    interPath = (head + "/" + tail + "/")

    myXml = xml()
    myData = defaultdict(list)
    typeOfNode = 'Signal'
    nameFile = "multimodalData"
    fileType = {
        'Signal': ('myo_emg','myo_accel','myo_gyro','myo_orientation'),
        'Audio': ('Audio', 'audio'),
        'Video': ('Video', 'video'),
        'File': ('Other', 'pd')
    }

    if os.path.exists(fn):
        only_files = [f for f in listdir(fn) if isfile(join(fn, f))]
        genericNode = xml.createGenericNode(myXml, myXml.getRoot(), 'MultimodalRecording', 'MYO_lifting', 'ROOT0_Mult0')
        for files in only_files:
            #this populate myData dictionary with all files on the folder with their type
            filetype = str(files).split(".")
            if (filetype[1] != "DS_Store") and (filetype[1] != "xml"):
                myResult = getType(files)
                myData[myResult[0]].append(myResult[1])

    for row in myData:
        if (row != 'Video') and (row != 'Audio'):
            newGenericNode = xml.createGenericNode(myXml, genericNode, "Data", row, "ROOT0_Mult0_MYOD0")
        for child_key in myData[row]:
            #file = fn + "/"+ child_key
            #with open(file) as f:
            #    print f.read().splitlines()
            name = str(child_key).split(".")
            for intype, format in fileType.iteritems():
                for elements in format:
                    if elements == row:
                        typeOfNode = intype
            if(name[1] == 'wav'):
                audioInfo = getAudioInfo(fn + "/" + child_key)
                audioChild = xml.addAudioNode(myXml, genericNode, typeOfNode, name[0]+'.'+name[1], '0', name[1], '2', audioInfo[0]*2, audioInfo[1])
            elif(name[1] == 'mp4'):
                videoChild = xml.addVideoNode(myXml, genericNode, typeOfNode, name[0] + '.' + name[1], '0', name[1])
            else:
                child = xml.addChildNode(myXml, newGenericNode, typeOfNode, name[0]+'.'+name[1], name[0], name[1], '4', '-4')
    print xml.printXml(myXml)
    outputFile = xml.fileToSave(myXml)

    # Write the updated XML structure
    file_handle = open(fn + '/' + nameFile + ".xml", "wb")
    file_handle.write(outputFile)
    file_handle.close()
    zippedFile = make_zipfile(fn)
    uploadFileToRepovizz(zippedFile)

def getAudioInfo(audioFile):
    import wave
    import contextlib
    fname = audioFile
    with contextlib.closing(wave.open(fname, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        result = frames, rate, duration
        print("Audio info: ")
        print( "frames: " + str(frames) + " rate: " + str(rate) + " duration: " + str(duration))
    return result


# Zips an entire directory using zipfile -----------------------------------------
def make_zipfile(_path):
    import zipfile
    if os.path.isdir(_path):
        inName = os.path.basename(_path) + '.zip'
        #head, tail = os.path.split(os.path.split(_path)[0])

        print "saving: " + inName
        def zipdir(_path, zip_handle):
            for root, dirs, files in os.walk(_path):
                for file in files:
                    zip_handle.write(os.path.join(root, file), file)
        with zipfile.ZipFile(inName, 'w',compression=zipfile.ZIP_DEFLATED, allowZip64=True) as z:
            zipdir(_path, z)
    return inName

#upload into repovizz all the file -----------------------------------------------
def uploadFileToRepovizz(file):
    import requests
    print 'uploading data into repoVizz...'
    fname = file
    folderName = (fname).split(".")

    toload = {
        'folder': 'testing_uploading',
        'name': folderName[0],
        'desc': 'testing, sending data from python to repoVizz',
        'user': 'Dazzid',
        'api_key': '9fc3d7152ba9336a670e36d0ed79bc43',
        'computeaudiodesc': '0',
        'computemocapdesc': '0',
        'keywords': 'myo',
        'file': open(fname, 'rb')}

    # Open an HTTP session
    s = requests.Session()
    # Upload the datapackh
    r = requests.post("https://repovizz.upf.edu/repo/api/datapacks/upload", files=toload, stream=True)
    # Unfortunately, the POST request doesn't return the upload link, so we have to search for it ourselves
    r2 = s.get("https://repovizz.upf.edu/repo/api/datapacks/search", params={'q': folderName[0]})
    result = str(r2).split(" ")
    result = result[1][1:-2]

    # If the response body isn't empty
    if result == "200":
        # Get a description of the datapack
        r3 = requests.get(
            "https://repovizz.upf.edu/repo/api/datapacks/" + str(r2.json()['datapacks'][0]['id']) + "/brief")
        # If the datapack was uploaded succesfully
        if (r3.json()['duration'] != 0):
            # Get the datapack ID and construct a working link to the datapack
            response = 'https://repovizz.upf.edu/repo/Vizz/' + str(r2.json()['datapacks'][0]['id'])
        elif r3 == "<Response [404]>":
            response = "Datapack not found"
        else:
            response = 'ERROR'
        print response

    elif result == "400":
        print "Invalid datapack ID supplied"

    elif result == "404":
        print "Datapack not found"

#------------------------------------------------------------------------------------
def getType(inFile):
    dataType = {
        'MYO': ('emg', 'accel', 'gyro', 'orientation'),
        'AUDIO': ('wav', 'aiff', 'mp3', 'ogg'),
        'VIDEO': ('mp4', 'mov'),
        'EEG': 'null', #to be completed
        'KINECT': 'null' #to be completed
    }
    type = str(inFile).split(".")
    if type[0][:-3] == dataType['MYO'][0]:
        result = "myo_emg", inFile
    elif type[0][:-3] == dataType['MYO'][1]:
        result = "myo_accel", inFile
    elif type[0][:-3] == dataType['MYO'][2]:
        result = "myo_gyro", inFile
    elif type[0][:-3] == dataType['MYO'][3]:
        result = "myo_orientation", inFile
    elif (type[1] == dataType['AUDIO'][0]) or (type[1] == dataType['AUDIO'][1]) or (type[1] == dataType['AUDIO'][2]) or (type[1] == dataType['AUDIO'][3]):
        result = "Audio", inFile
    elif (type[1] == dataType['VIDEO'][0]) or (type[1] == dataType['VIDEO'][1]):
        result = "Video", inFile
    else:
        result = "Other", inFile
    return result

if __name__ == "__main__":
   main(sys.argv)