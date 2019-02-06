import java.io.File
import java.util.ArrayList
import qupath.lib.objects.*
import qupath.lib.gui.ImageWriterTools
import qupath.lib.io.PathIO
import qupath.lib.regions.RegionRequest
import qupath.lib.gui.models.ObservableMeasurementTableData
import qupath.lib.objects.classes.PathClass
import qupath.lib.common.ColorTools
import qupath.lib.roi.interfaces.*
import qupath.lib.roi.PathROIToolsAwt

def server = getCurrentImageData().getServer()
def path = server.getPath()
def imgName = server.getShortServerName()
def dirName = _REPLACE_DIR_

// Create the result directories if not exist
File resDir = new File(dirName+"ES_TileWise")
if(!resDir.exists())
    resDir.mkdirs()

File qpdataDir =  new File(dirName+"ES_TileWise_qpdata")
if(!qpdataDir.exists())
    qpdataDir.mkdirs()

////// Start with SP_before_qpdata ///////
// read the classification result and save it into a hashmap
res = new File(dirName+'SP_filtered_data/'+imgName+'.csv')
HashMap<String, String> map = new HashMap<>()
for (line in res.readLines()) {
    String[] items = line.split(',')
    map.put(items[1], items[2])
}

// apply the classification result
SPs = getDetectionObjects()
for (sp in SPs) {
    id = String.valueOf((int)sp.getMeasurementList().getMeasurementValue('Object Id'))
    trueClass = map.get(id)

    if(trueClass=='"Tumor"')
        sp.setPathClass(new PathClass("Tumor", ColorTools.makeRGB(200, 0, 0)))
    else if(trueClass=='"Stroma"')
        sp.setPathClass(new PathClass("Stroma", ColorTools.makeRGB(150, 200, 150)))
    else
        getCurrentHierarchy().removeObject(sp,true)
}
fireHierarchyUpdate()

// delete master annotation and load tile objects
clearAnnotations()
tiles = null
new File(dirName+'Tile_object/'+imgName+'.tiles').withObjectInputStream {
    tiles = it.readObject()
}
addObjects(tiles)
fireHierarchyUpdate()

// convert SP detection objects to annotation
selectAnnotations()
tiles = getAnnotationObjects() // save for later use
runPlugin('qupath.lib.analysis.objects.TileClassificationsToAnnotationsPlugin', '{"pathClass": "All classes",  "deleteTiles": true,  "clearAnnotations": true,  "splitAnnotations": false}')

// Load cells
cells = null
new File(dirName+'Cell_object/'+imgName+'.cells').withObjectInputStream {
    cells = it.readObject()
}
addObjects(cells)
fireHierarchyUpdate()

// Save data of each superpixel with the name of its parent (tile id) attached
StringBuilder sb = new StringBuilder()
SPs = getAnnotationObjects().findAll({it.getParent().getName()!=null})
ObservableMeasurementTableData model = new ObservableMeasurementTableData()
model.setImageData(getCurrentImageData(), getCurrentImageData().getHierarchy().getObjects(null, PathAnnotationObject.class))

// column names
List<String> names = new ArrayList<>(model.getAllNames())
int nColumns = names.size()
sb.append('Parent Tile,')
for (int col = 0; col < nColumns; col++) {
    sb.append(names.get(col))
    if (col < nColumns - 1)
        sb.append(',')
}
sb.append("\n")

for (sp in SPs) {
    sb.append(sp.getParent().getName()+',')
    for (int col = 0; col < nColumns; col++) {
        String val = model.getStringValue(sp, names.get(col))
        if (val != null)
            sb.append(val)
        if (col < nColumns - 1)
            sb.append(',')
    }
    sb.append("\n");
}

File fileOutput = new File(resolvePath(dirName+'ES_TileWise/'+imgName+'.csv'))
PrintWriter writer = new PrintWriter(fileOutput)
writer.println(sb.toString())
writer.close()

// save qpdata
File img_2 = new File(dirName+'ES_TileWise_qpdata/'+imgName+'.qpdata')
PathIO.writeImageData(img_2, getCurrentImageData())
