import java.util.HashMap
import java.io.File
import java.nio.file.*
import static java.nio.file.StandardCopyOption.*;
import java.io.PrintWriter
import java.util.ArrayList
import java.util.Collections
import java.util.Comparator
import qupath.lib.objects.*
import qupath.lib.regions.RegionRequest
import qupath.lib.gui.ImageWriterTools
import qupath.lib.io.PathIO
import qupath.lib.objects.classes.PathClassFactory
import qupath.lib.gui.models.ObservableMeasurementTableData


def imageData = getCurrentImageData()
def server = imageData.getServer()
def path = server.getPath()
def imgName = server.getShortServerName()
def dirName = _REPLACE_DIR_
def projName = _REPLACE_PROJECT_DIR_

// Create the result directories if not exist
File cellObjDir = new File(dirName+"Cell_object")
if(!cellObjDir.exists())
    cellObjDir.mkdirs()

File qpdataDir =  new File(dirName+"Cell_filtered_qpdata")
if(!qpdataDir.exists())
    qpdataDir.mkdirs()


// read the classification result and save it into a hashmap
res = new File(dirName+'Cell_filtered_data/'+imgName+'.csv')
HashMap<String, String> map = new HashMap<>()
for (line in res.readLines()) {
    String[] items = line.split(',')
    map.put(items[1], items[2])
}

// apply the classification result
cells = getDetectionObjects()
for (cell in cells) {
    id = String.valueOf((int)cell.getMeasurementList().getMeasurementValue('Object Id'))
    trueClass = map.get(id)

    if(trueClass=='"Positive"')
        cell.setPathClass(PathClassFactory.getPositive(null, null))
    else if(trueClass=='"Negative"')
        cell.setPathClass(PathClassFactory.getNegative(null, null))
    else
        getCurrentHierarchy().removeObject(cell,true)
}

// Compute measurements after classification
ObservableMeasurementTableData model = new ObservableMeasurementTableData()
model.setImageData(imageData, imageData.getHierarchy().getObjects(null, PathAnnotationObject.class))

// Save the filtered result
File img_2 = new File(dirName+'Cell_filtered_qpdata/'+imgName+'.qpdata')
PathIO.writeImageData(img_2, imageData)

// Save the filtered cells
cells = getDetectionObjects().findAll({it.getPathClass().getName()=='Positive'})
new File(dirName+'Cell_object/'+imgName+'.cells').withObjectOutputStream {
    it.writeObject(cells)
}

// copy SP_before.qpdata for the next step
Files.copy(Paths.get(dirName+'SP_before_qpdata/'+imgName+'.qpdata'),Paths.get(projName+'data/'+imgName+'.qpdata'),REPLACE_EXISTING)
