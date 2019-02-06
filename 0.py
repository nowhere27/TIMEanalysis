import os

inDir = os.path.dirname(os.path.realpath(__file__))
dirNames = inDir.split("\\")
outDirRoot = ('/').join(dirNames[:-1])
outDir = outDirRoot+'/Project/scripts/'
dataDir = '"'+outDirRoot+'/Data/'+'"'
projDir = '"'+outDirRoot+'/Project/'+'"'

fList = os.listdir(inDir)
for f in fList:
    if('.rds' in f):
        os.rename(outDirRoot+"/code/"+f,outDir+f)
    elif('classifiers' not in f):
        if(f!='0.py'):
            file = open(inDir+"\\"+f)
            line = file.readlines()

            outFile = open(outDir+f,'w')
            for l in line:
                if('_REPLACE_DIR_' in l):
                    outFile.write(l.replace('_REPLACE_DIR_',dataDir))
                elif('_REPLACE_PROJECT_DIR_' in l):
                    outFile.write(l.replace('_REPLACE_PROJECT_DIR_',projDir))
                else:
                    outFile.write(l)

            outFile.close()

