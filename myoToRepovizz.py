import csv
import os
from os import listdir
from os.path import isfile, join

type = "emg"

def crateFile(name, counter, inData):
    type = name
    #for row in inData:
    #    print(row)
    inName = "myo_recordings/data/"+type+"["+str(counter)+"]" ".csv"
    f = open(inName, 'wt')
    try:
        writer = csv.writer(f, quoting = csv.QUOTE_NONE, delimiter=',', escapechar=' ')
        writer.writerow( inData )
    finally:
        f.close()
    addHeaderFormat(inName)

def addHeaderFormat(openfile):
    with file(openfile, 'r') as original: data = original.read()
    with file(openfile, 'w') as modified: modified.write("repovizz,framerate=200\n" + data)


with open('myo_recordings/myo_record.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    header = reader.next()
    data = [row for row in reader]
    firstData = []

    for i in range(0,8):
        firstData.append([])
        for row in data:
            inData = str(row[i+1:i+2][0])
            firstData[i].append(inData)
        crateFile(type, i + 1, firstData[i])

from lxml import etree
mypath = "myo_recordings/data/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print onlyfiles

#get duration on seconds from csv
def get_csv_duration(csv_path):
    with open(csv_path, 'r') as f:
        header = f.next().split(",")
        data = f.next()
        # Get the sampling rate and number of samples
        sr = float(header[1].split("framerate=")[1])
        num_samples = float(data.count(","))
    return float(num_samples)*(1/sr)

print get_csv_duration(mypath + onlyfiles[1])

root = etree.Element("ROOT")
root.set('ID', 'ROOT0')

# Create a signal Myo node
def addMyoSignalNode(parentNode, _inName, _myo_number, _maxVal, _minVal):
    sr = 200
    in_name = _inName
    myo_number = _myo_number
    maxVal = _maxVal
    minVal = _minVal
    numSamples = 1
    myo_node = etree.Element('Signal')
    myo_node.set('BytesPerSample', '')
    myo_node.set('Category', 'EMG')
    myo_node.set('DefaultPath', '0')
    myo_node.set('EstimatedSampleRate', '0.0')
    myo_node.set('Expanded', '1')
    myo_node.set('FileType', 'CSV')
    myo_node.set('Filename', str(in_name))
    myo_node.set('FrameSize', '1')
    myo_node.set('ID', 'ROOT0_Mult0_MYOD0_EMG0_EMG'+str(myo_number))
    myo_node.set('MaxVal', str(maxVal))
    myo_node.set('MinVal', str(minVal))
    myo_node.set('name', str(myo_number))
    myo_node.set('NumChannels', '')
    myo_node.set('NumSamples', str(numSamples))
    myo_node.set('ResampledFlag', '-1')
    myo_node.set('SampleRate', str(sr))
    myo_node.set('SpecSampleRate', '0.0')
    myo_node.set('_Extra', 'canvas=-1,color=0,selected=1')
    parentNode.insert(len(parentNode), myo_node)
    return parentNode[0]

 # Create a Generic node
def createGenericNode(parentNode, _category, _name, _id):
    iName = _name
    iCategory = _category
    iId = _id
    external_myo_node = etree.Element('Generic')
    external_myo_node.set('Category', iCategory)
    external_myo_node.set('Expanded', '1')
    external_myo_node.set('ID', _id)
    external_myo_node.set('Name', iName)
    external_myo_node.set('_Extra', '')
    parentNode.insert(0, external_myo_node)
    return parentNode[0]

myoChild = createGenericNode(root, "MultimodalRecording", "MYO_various", "ROOT0_Mult0")
child = createGenericNode(myoChild, "EMG", "Electromyography", "ROOT0_Mult0")

counter = 0
for data in onlyfiles:
    if (data.split(".")[1] == "csv"):
        addMyoSignalNode(child, str(data), counter, 1.0, -1.0)
        counter += 1

print etree.tostring(root, pretty_print=True)
outputFile=etree.tostring(root, pretty_print=False)

# Write the updated XML structure
file_handle = open(mypath+"MYO_File.xml","wb")
file_handle.write(outputFile)
file_handle.close()

import zipfile
# Zips an entire directory using zipfile

def zipdir(path, zip_handle):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_handle.write(os.path.join(root, file),file)

# Re-zip the datapack
with zipfile.ZipFile("MYO_File.zip", 'w') as z:
    zipdir(mypath, z)

import requests
# You can adapt any of these fields, for a reference go to the http://repovizz.upf.edu/repo/Manage
# to see the "Upload" form
fname = "MYO_File.zip"
folderName = (fname).split(".")

toload = {
    'folder': 'testing_uploading',
    'name': folderName[0],
    'desc': 'testing, sending data from python to repoVizz',
    'user': 'Dazzid',
    'api_key':'9fc3d7152ba9336a670e36d0ed79bc43',
    'computeaudiodesc': '0',
    'computemocapdesc': '0',
    'keywords':'myo',
    'file': open(fname,'rb')}

# Open an HTTP session
s = requests.Session()
# Upload the datapack
r = requests.post("https://repovizz.upf.edu/repo/api/datapacks/upload",files=toload,stream=True)
print r

# Unfortunately, the POST request doesn't return the upload link, so we have to search for it ourselves
r2 = s.get("https://repovizz.upf.edu/repo/api/datapacks/search",params={'q':folderName[0]})
result = str(r2).split(" ")
result =  result[1][1:-2]

# If the response body isn't empty
if result == "200":
    # Get a description of the datapack
    r3 = requests.get("https://repovizz.upf.edu/repo/api/datapacks/" + str(r2.json()['datapacks'][0]['id']) + "/brief")
    # If the datapack was uploaded succesfully
    if (r3.json()['duration'] != 0):
        # Get the datapack ID and construct a working link to the datapack
        response = 'https://repovizz.upf.edu/repo/Vizz/' + str(r2.json()['datapacks'][0]['id'])
    else:
        response = 'ERROR'
    print response