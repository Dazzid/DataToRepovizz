#!/Users/David/anaconda2/bin/python
#David Dalmazzo
#MTG UPF
#April 2017

import sys
import os
import csv

def main(argv):
    if (len(argv) <= 1):
        print "-----> ERROR: you need to specify the folder path to upload"
        quit()
    fn = sys.argv[1]
    head, tail = os.path.split(os.path.split(fn)[0])
    empty, file = os.path.split(os.path.split(fn)[1])
    interPath = (head + "/" + tail + "/")
    #atention to the name of the csv file to know the type of file emg, acc, gyro etc...
    myType = file.split(".")

    directory = interPath + "/data/"
    if not os.path.exists(directory):
        os.makedirs(directory)
        # open the file to format
        with open(fn, 'rU') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            header = reader.next()
            data = [row for row in reader]
            firstData = []

            for i in range(0, 8):
                firstData.append([])
                for row in data:
                    inData = str(row[i + 1:i + 2][0])
                    firstData[i].append(inData)
                crateFile(directory, myType[0], i + 1, firstData[i])
        print "Process SUCCEED!"
    else:
        print "-----> data already generated"

# create single files for data to adapt the format to repovizz
def crateFile(location, name, counter, inData):
    type = name
    # for row in inData:
    #    print(row
    inName = location + type + "[" + str(counter) + "]" ".csv"
    f = open(inName, 'wt')
    try:
        writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=',', escapechar=' ')
        writer.writerow(inData)
    finally:
        f.close()
    addHeaderFormat(inName)

# add the header information needed for repovizz
def addHeaderFormat(openfile):
    with file(openfile, 'r') as original: data = original.read()
    with file(openfile, 'w') as modified: modified.write("repovizz,framerate=200\n" + data)
    print "---> recording: " +openfile

if __name__ == "__main__":
   main(sys.argv)