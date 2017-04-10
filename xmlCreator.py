from lxml import etree

class xmlCreator:
    # Create a signal Myo node

    root = etree.Element("ROOT")
    root.set('ID', 'ROOT0')

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