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
def width = server.getWidth()
double downsample = width/1600
def dirName = _REPLACE_DIR_
def projName = _REPLACE_PROJECT_DIR_

// Create the result directories if not exist
File snapshot = new File(dirName+"IS_snapshot")
if(!snapshot.exists())
    snapshot.mkdirs()

File tileObj =  new File(dirName+"Tile_object")
if(!tileObj.exists())
    tileObj.mkdirs()

////// Start with tile optiization & select IM tiles ///////
def IMTiles = getSelectedObjects().findAll({it.isAnnotation()})

// Save ROI with IMs highlighted
File file = new File(dirName+'IS_snapshot/'+imgName+'.png')
overlayOptions = getCurrentViewer().getOverlayOptions()
request = RegionRequest.createInstance(getCurrentImageData().getServerPath(), downsample, 0, 0, width, server.getHeight())
ImageWriterTools.writeImageRegionWithOverlay(getCurrentImageData(), overlayOptions, request, file.getAbsolutePath())

// Rename IM tiles for later use and save
int idx=1;
for(t in IMTiles) {
    t.setName('IM'+String.valueOf(idx));
    idx+=1;
}

// save .qpdata :: IS tiles + unfiltered cells
File img = new File(projName+'data/'+imgName+'.qpdata')
PathIO.writeImageData(img, getCurrentImageData())

// save tile object
tiles = getAnnotationObjects()
new File(dirName+'Tile_object/'+imgName+'.tiles').withObjectOutputStream {
    it.writeObject(tiles)
}
