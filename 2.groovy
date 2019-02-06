import java.io.File
import java.util.ArrayList
import qupath.lib.objects.*
import qupath.lib.gui.ImageWriterTools
import qupath.lib.io.PathIO
import qupath.lib.regions.RegionRequest
import qupath.lib.gui.models.ObservableMeasurementTableData

def server = getCurrentImageData().getServer()
def path = server.getPath()
def imgName = server.getShortServerName()
def dirName = _REPLACE_DIR_
def projName = _REPLACE_PROJECT_DIR_

// Create the result directories if not exist
File cell_before_data = new File(dirName+"Cell_before_data")
if(!cell_before_data.exists())
    cell_before_data.mkdirs()

File cell_before_qpdata = new File(dirName+"Cell_before_qpdata")
if(!cell_before_qpdata.exists())
  cell_before_qpdata.mkdirs()

File SP_before_data = new File(dirName+"SP_before_data")
if(!SP_before_data.exists())
  SP_before_data.mkdirs()

File SP_before_qpdata = new File(dirName+"SP_before_qpdata")
if(!SP_before_qpdata.exists())
  SP_before_qpdata.mkdirs()
  
def IMTiles = getAnnotationObjects().findAll({it.getName().contains('IM')})

// Identify cells
setImageType('BRIGHTFIELD_H_DAB')
setColorDeconvolutionStains('{"Name" : "H-DAB default", "Stain 1" : "Hematoxylin", "Values 1" : "0.65111 0.70119 0.29049 ", "Stain 2" : "DAB", "Values 2" : "0.26917 0.56824 0.77759 ", "Background" : " 255 255 255 "}')
selectAnnotations()
runPlugin('qupath.imagej.detect.nuclei.PositiveCellDetection', '{"detectionImageBrightfield": "Optical density sum",  "requestedPixelSizeMicrons": 0.5,  "backgroundRadiusMicrons": 20.0,  "medianRadiusMicrons": 0.0,  "sigmaMicrons": 1.5,  "minAreaMicrons": 30.0,  "maxAreaMicrons": 200.0,  "thresholdh": 0.1,  "maxBackground": 2.0,  "watershedPostProcess": true,  "excludeDAB": false,  "cellExpansionMicrons": 5.0,  "includeNuclei": true,  "smoothBoundaries": true,  "makeMeasurements": true,  "thresholdCompartment": "Nucleus: DAB OD mean",  "thresholdPositive1": 0.4,  "thresholdPositive2": 0.5,  "thresholdPositive3": 0.6,  "singleThreshold": true}')
selectDetections()
runPlugin('qupath.lib.algorithms.IntensityFeaturesPlugin', '{"pixelSizeMicrons": 0.5,  "region": "ROI",  "tileSizeMicrons": 25.0,  "colorOD": true,  "colorStain1": false,  "colorStain2": true,  "colorStain3": false,  "colorRed": false,  "colorGreen": false,  "colorBlue": false,  "colorHue": true,  "colorSaturation": true,  "colorBrightness": true,  "doMean": true,  "doStdDev": true,  "doMinMax": true,  "doMedian": true,  "doHaralick": true,  "haralickDistance": 1,  "haralickBins": 32}')
selectDetections()
runPlugin('qupath.lib.algorithms.CoherenceFeaturePlugin', '{"magnification": 5.0,  "stainChoice": "H-DAB",  "tileSizeMicrons": 25.0,  "includeStats": true,  "doCircular": false}')
selectCells()
runPlugin('qupath.lib.plugins.objects.ShapeFeaturesPlugin', '{"area": true,  "perimeter": true,  "circularity": true,  "useMicrons": true}')


// Retain only positively stained cells and save (before_filtering)
negs = getDetectionObjects().findAll({it.getPathClass().getName()=='Negative'})
getCurrentHierarchy().removeObjects(negs,true)

// add Id
def detections = getDetectionObjects()
detections.eachWithIndex{pathObject, i->
    pathObject.getMeasurementList().putMeasurement('Object Id', i)
    pathObject.getMeasurementList().closeList()
}
fireHierarchyUpdate()

// export features
StringBuilder sb = new StringBuilder();
ObservableMeasurementTableData model = new ObservableMeasurementTableData()
model.setImageData(getCurrentImageData(), getCurrentImageData().getHierarchy().getObjects(null, PathDetectionObject.class))

// column names
List<String> names = new ArrayList<>(model.getAllNames())
int nColumns = names.size()
for (int col = 0; col < nColumns; col++) {
    sb.append(names.get(col))
    if (col < nColumns - 1)
        sb.append(',')
}
sb.append("\n")

for (object in model.getEntries()) {
    for (int col = 0; col < nColumns; col++) {
        String val = model.getStringValue(object, names.get(col))
        if (val != null)
            sb.append(val)
        if (col < nColumns - 1)
            sb.append(',')
    }
    sb.append("\n");
}

File fileOutput = new File(resolvePath(dirName+'Cell_before_data/'+imgName+'.csv'))
PrintWriter writer = new PrintWriter(fileOutput)
writer.println(sb.toString())
writer.close()

// save .qpdata :: IS tiles + unfiltered cells
File img = new File(dirName+'Cell_before_qpdata/'+imgName+'.qpdata')
PathIO.writeImageData(img, getCurrentImageData())
File img_data = new File(projName+'data/'+imgName+'.qpdata')
PathIO.writeImageData(img_data, getCurrentImageData())

// delete cells and merge tiles
clearDetections()
selectAnnotations()
mergeSelectedAnnotations()
selectAnnotations()
runPlugin('qupath.imagej.superpixels.DoGSuperpixelsPlugin', '{"downsampleFactor": 8.0,  "sigmaMicrons": 10.0,  "minThreshold": 10.0,  "maxThreshold": 230.0,  "noiseThreshold": 1.0}');
selectDetections();
runPlugin('qupath.lib.algorithms.IntensityFeaturesPlugin', '{"pixelSizeMicrons": 2.0,  "region": "ROI",  "tileSizeMicrons": 25.0,  "colorOD": true,  "colorStain1": true,  "colorStain2": true,  "colorStain3": false,  "colorRed": false,  "colorGreen": false,  "colorBlue": false,  "colorHue": true,  "colorSaturation": true,  "colorBrightness": true,  "doMean": true,  "doStdDev": true,  "doMinMax": true,  "doMedian": true,  "doHaralick": true,  "haralickDistance": 1,  "haralickBins": 32}');
selectDetections();
runPlugin('qupath.lib.algorithms.CoherenceFeaturePlugin', '{"magnification": 5.0,  "stainChoice": "Optical density",  "tileSizeMicrons": 25.0,  "includeStats": true,  "doCircular": false}');
selectDetections();
runPlugin('qupath.lib.algorithms.LocalBinaryPatternsPlugin', '{"magnification": 5.0,  "stainChoice": "Optical density",  "tileSizeMicrons": 25.0,  "includeStats": true,  "doCircular": false}');
selectAnnotations();
runPlugin('qupath.lib.plugins.objects.SmoothFeaturesPlugin', '{"fwhmMicrons": 25.0,  "smoothWithinClasses": false,  "useLegacyNames": false}');

// add Id
def superpixels = getDetectionObjects()
superpixels.eachWithIndex{pathObject, i->
    pathObject.getMeasurementList().putMeasurement('Object Id', i)
    pathObject.getMeasurementList().closeList()
}
fireHierarchyUpdate()

// export features
StringBuilder sb_sp = new StringBuilder();
model.setImageData(getCurrentImageData(), getCurrentImageData().getHierarchy().getObjects(null, PathDetectionObject.class))

// column names
List<String> names_sp = new ArrayList<>(model.getAllNames())
int nColumns_sp = names_sp.size()
for (int col = 0; col < nColumns_sp; col++) {
    sb_sp.append(names_sp.get(col))
    if (col < nColumns_sp - 1)
        sb_sp.append(',')
}
sb_sp.append("\n")

for (object in model.getEntries()) {
    for (int col = 0; col < nColumns_sp; col++) {
        String val = model.getStringValue(object, names_sp.get(col))
        if (val != null)
            sb_sp.append(val)
        if (col < nColumns_sp - 1)
            sb_sp.append(',')
    }
    sb_sp.append("\n");
}

File fileOutput_sp = new File(resolvePath(dirName+'SP_before_data/'+imgName+'.csv'))
PrintWriter writer_sp = new PrintWriter(fileOutput_sp)
writer_sp.println(sb_sp.toString())
writer_sp.close()

// save .qpdata :: Superpixels
File img_sp = new File(dirName+'SP_before_qpdata/'+imgName+'.qpdata')
PathIO.writeImageData(img_sp, getCurrentImageData())
