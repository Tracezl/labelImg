import json
from libs.constants import DEFAULT_ENCODING


JSON_EXT = '.json'
ENCODE_METHOD = DEFAULT_ENCODING

class JSONWriter:

    def __init__(self, foldername, filename, imgSize,databaseSrc='Unknown', localImgPath=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath
        self.verified = False

    def addBndBox(self, xmin, ymin, xmax, ymax, name, difficult,group="-1"):
        bndbox={}
        bndbox["pos"] =[xmin,ymin, xmax, ymax]
        bndbox['label'] = name
        bndbox['group'] =group
        self.boxlist.append(bndbox)

    def save(self, targetFile=None):
        if targetFile is None:
            with open(self.filename + JSON_EXT, "w+",encoding=ENCODE_METHOD) as txt:
                txt.write(json.dumps(self.boxlist, ensure_ascii=False))
        else:
            with open(targetFile, "w+",encoding=ENCODE_METHOD) as txt:
                txt.write(json.dumps(self.boxlist, ensure_ascii=False))
class JSONReader:

    def __init__(self, filepath):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color, difficult]
        self.shapes = []
        self.filepath = filepath
        self.verified = False
        try:
            self.parseJSON()
        except:
            pass

    def getShapes(self):
        return self.shapes

    def addShape(self, label, bndbox, difficult,group):
        xmin = int(bndbox[0])
        ymin = int(bndbox[1])
        xmax = int(bndbox[2])
        ymax = int(bndbox[3])
        points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        # print((label, points, None, None, difficult))
        self.shapes.append((label, points, None, None, difficult,group))

    def parseJSON(self):
        assert self.filepath.endswith(JSON_EXT), "Unsupport file format"
        with open(self.filepath, "r+") as txt:
            txtContent = txt.read()
            if len(txtContent) > 0:
                results = json.loads(txtContent)
            else:
                results = {}
        # print(results)
        # print(results[0])
        for object_iter in results:
            bndbox = object_iter["pos"]
            label = str(object_iter["label"])
            group=str(object_iter["group"])
            # Add chris
            difficult = False
            self.addShape(label, bndbox, difficult,group)
        try:
            verified =results['verified']
            if verified == 'yes':
                self.verified = True
        except KeyError:
            self.verified = False
        return True