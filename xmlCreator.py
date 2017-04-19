from lxml import etree

class xml(object):
    
    def __init__(self):
        self.root = etree.Element("ROOT")
        self.root.set('ID', 'ROOT0')
    
    def getRoot(self):
        return self.root
    
    def get_csv_duration(self, csv_path):
        with open(csv_path, 'r') as f:
            header = f.next().split(",")
            data = f.next()
            # Get the sampling rate and number of samples
            sr = float(header[1].split("framerate=")[1])
            num_samples = float(data.count(","))
        return float(num_samples)*(1/sr)
    
    # Create a signal Myo node
    def addChildNode(self, parentNode, _signal, _inName, _in_number, _type,  _maxVal, _minVal):
        sr = 200
        in_name = _inName
        #  myo_number = _myo_number
        maxVal = _maxVal
        minVal = _minVal
        numSamples = 1
        typeNode = _signal
        sub_node = etree.Element(typeNode)
        sub_node.set('BytesPerSample', '')
        sub_node.set('Category', typeNode)
        sub_node.set('DefaultPath', '0')
        sub_node.set('EstimatedSampleRate', '0.0')
        sub_node.set('Expanded', '1')
        sub_node.set('FileType', _type)
        sub_node.set('Filename', _inName)
        sub_node.set('FrameSize', '')
        sub_node.set('ID', 'ROOT0_Mult0_MYOD0_EMG0_EMG' + str(_in_number))
        sub_node.set('MaxVal', str(maxVal))
        sub_node.set('MinVal', str(minVal))
        sub_node.set('name', _in_number)
        sub_node.set('NumChannels', '')
        sub_node.set('NumSamples', str(numSamples))
        sub_node.set('ResampledFlag', '-1')
        sub_node.set('SampleRate', str(sr))
        sub_node.set('SpecSampleRate', '0.0')
        sub_node.set('_Extra', 'canvas=-1,color=0,selected=1')
        parentNode.insert(len(parentNode), sub_node)
        return parentNode[0]
    
    # Create a signal Audio node
    def addAudioNode(self, parentNode, _signal, _inName, _inNumber, _type, _numChannels, _numSamples, _sampleRate):
        _bytePerSample = 2
        typeNode = _signal
        sub_node = etree.Element(typeNode)
        sub_node.set('BytesPerSample', str(_bytePerSample))
        sub_node.set('Category', typeNode)
        sub_node.set('DefaultPath', '0')
        sub_node.set('EstimatedSampleRate', '0.0')
        sub_node.set('Expanded', '1')
        sub_node.set('FileType', _type)
        sub_node.set('Filename', _inName)
        sub_node.set('FrameSize', '1')
        sub_node.set('ID', 'ROOT0_Mult0_Micr' + str(_inNumber))
        sub_node.set('name', _inName)
        sub_node.set('NumChannels', str(_numChannels))
        sub_node.set('NumSamples', str(_numSamples))
        sub_node.set('ResampledFlag', '-1')
        sub_node.set('SampleRate', str(_sampleRate))
        sub_node.set('SpecSampleRate', '0.0')
        sub_node.set('_Extra', 'canvas=-1,color=0,selected=1')
        parentNode.insert(len(parentNode), sub_node)
        return parentNode[0]
    
    # Create a signal Video node
    def addVideoNode(self, parentNode, _signal, _inName, _inNumber, _type):
        _bytePerSample = 2
        typeNode = _signal
        sub_node = etree.Element(typeNode)
        sub_node.set('Category', typeNode)
        sub_node.set('DefaultPath', '0')
        sub_node.set('Expanded', '1')
        sub_node.set('FileType', _type)
        sub_node.set('Filename', _inName)
        sub_node.set('ID', 'ROOT0_Mult0_HQ' + str(_inNumber))
        sub_node.set('name', _inName)
        sub_node.set('_Extra', 'canvas=-1,color=0,selected=1')
        parentNode.insert(len(parentNode), sub_node)
        return parentNode[0]
    
    # Create a Generic node
    def createGenericNode(self, parentNode, _category, _name, _id):
        iName = _name
        iCategory = _category
        iId = _id
        external_node = etree.Element('Generic')
        external_node.set('Category', iCategory)
        external_node.set('Expanded', '1')
        external_node.set('ID', _id)
        external_node.set('Name', iName)
        external_node.set('_Extra', '')
        parentNode.insert(0, external_node)
        return parentNode[0]
    
    def printXml(self):
        print etree.tostring(self.root, pretty_print=True)
    
    def fileToSave(self):
        return etree.tostring(self.root, pretty_print=False)
