import os, csv, time
import numpy as np
import scipy.stats as sci

# Methods
def CoV(X):
    value = np.std(X)/np.mean(X)
    if(np.isnan(value)):
        return 0
    else:
        return value

def QD(X):
    first = np.percentile(X,25)
    third = np.percentile(X,75)

    value = (third-first)/(third+first)
    if(np.isnan(value)):
        return 0
    else:
        return value

def ratio(CD8,CD3):
    if(CD3==0):
        return 1
    elif(CD8==0):
        return 0
    elif(CD8/CD3>1):
        return 1 # by definition, maximum needs to be 1
    else:
        return CD8/CD3

def clearDir(path):
    dirName = path.split('/')[-2]

    if(dirName not in os.listdir(superDir)):
    	os.mkdir(path)
    else:
        fList = os.listdir(path)
        for f in fList:
            os.remove(path+f)

# Variables
superDir = _REPLACE_DIR_
resDir_cell= superDir+'Cell_filtered_data/'
resDir = superDir+'ES_TileWise/'
tileDir = superDir+'Tilewise_data/'
clearDir(tileDir)

## Step 0. create result file
start = time.time()
resF = open(superDir+'count.csv', 'wb')
res = csv.writer(resF, delimiter=',', lineterminator='\n')
res.writerow(['Case Id', 'CD3_ie_density', 'CD3_str_density', 'CD3_ie_str', 'CD3_ie_density_mean', 'CD3_str_density_mean', 'CD3_ie_str_mean','CD3_ie_density_min', 'CD3_str_density_min', 'CD3_ie_str_min','CD3_ie_density_median', 'CD3_str_density_median', 'CD3_ie_str_median','CD3_ie_density_max', 'CD3_str_density_max', 'CD3_ie_str_max','CD3_ie_density_QD', 'CD3_str_density_QD',  'CD3_ie_str_QD', 'CD3_ie_density_CoV', 'CD3_str_density_CoV', 'CD3_ie_str_CoV', 'CD8_ie_density', 'CD8_str_density', 'CD8_ie_str', 'CD8_ie_density_mean', 'CD8_str_density_mean', 'CD8_ie_str_mean', 'CD8_ie_density_min', 'CD8_str_density_min', 'CD8_ie_str_min','CD8_ie_density_median', 'CD8_str_density_median', 'CD8_ie_str_median','CD8_ie_density_max', 'CD8_str_density_max', 'CD8_ie_str_max','CD8_ie_density_QD', 'CD8_str_density_QD', 'CD8_ie_str_QD', 'CD8_ie_density_CoV', 'CD8_str_density_CoV', 'CD8_ie_str_CoV','CD8_CD3_ie', 'CD8_CD3_str', 'CD8_CD3_ie_mean', 'CD8_CD3_str_mean','CD8_CD3_ie_min', 'CD8_CD3_str_min','CD8_CD3_ie_median', 'CD8_CD3_str_median','CD8_CD3_ie_max', 'CD8_CD3_str_max','Stroma_percentage', 'Stroma_mean', 'Stroma_min', 'Stroma_median', 'Stroma_max', 'Stroma_QD', 'Stroma_CoV','CD3_mean', 'CD3_min', 'CD3_median', 'CD3_max', 'CD3_CoV', 'CD3_QD', 'CD3_IM_mean', 'CD3_IM_min', 'CD3_IM_median', 'CD3_IM_max', 'CD3_IM_CoV', 'CD3_IM_QD', 'CD3_IM_mean_ie', 'CD3_IM_min_ie', 'CD3_IM_median_ie', 'CD3_IM_max_ie', 'CD3_IM_CoV_ie', 'CD3_IM_QD_ie', 'CD3_IM_mean_str', 'CD3_IM_min_str', 'CD3_IM_median_str', 'CD3_IM_max_str', 'CD3_IM_CoV_str', 'CD3_IM_QD_str', 'CD3_CT_mean', 'CD3_CT_min', 'CD3_CT_median', 'CD3_CT_max', 'CD3_CT_CoV', 'CD3_CT_QD','CD3_CT_mean_ie', 'CD3_CT_min_ie', 'CD3_CT_median_ie', 'CD3_CT_max_ie', 'CD3_CT_CoV_ie', 'CD3_CT_QD_ie', 'CD3_CT_mean_str', 'CD3_CT_min_str', 'CD3_CT_median_str', 'CD3_CT_max_str', 'CD3_CT_CoV_str', 'CD3_CT_QD_str', 'CD3_ie_str_IM_mean', 'CD3_ie_str_IM_min', 'CD3_ie_str_IM_median', 'CD3_ie_str_IM_max', 'CD3_ie_str_IM_CoV', 'CD3_ie_str_IM_QD', 'CD3_ie_str_CT_mean', 'CD3_ie_str_CT_min', 'CD3_ie_str_CT_median', 'CD3_ie_str_CT_max', 'CD3_ie_str_CT_CoV', 'CD3_ie_str_CT_QD', 'CD8_mean', 'CD8_min', 'CD8_median', 'CD8_max', 'CD8_CoV', 'CD8_QD','CD8_IM_mean', 'CD8_IM_min', 'CD8_IM_median', 'CD8_IM_max', 'CD8_IM_CoV', 'CD8_IM_QD', 'CD8_IM_mean_ie', 'CD8_IM_min_ie', 'CD8_IM_median_ie', 'CD8_IM_max_ie', 'CD8_IM_CoV_ie', 'CD8_IM_QD_ie', 'CD8_IM_mean_str', 'CD8_IM_min_str', 'CD8_IM_median_str', 'CD8_IM_max_str', 'CD8_IM_CoV_str', 'CD8_IM_QD_str','CD8_CT_mean', 'CD8_CT_min', 'CD8_CT_median', 'CD8_CT_max', 'CD8_CT_CoV', 'CD8_CT_QD','CD8_CT_mean_ie', 'CD8_CT_min_ie', 'CD8_CT_median_ie', 'CD8_CT_max_ie', 'CD8_CT_CoV_ie', 'CD8_CT_QD_ie', 'CD8_CT_mean_str', 'CD8_CT_min_str', 'CD8_CT_median_str', 'CD8_CT_max_str', 'CD8_CT_CoV_str', 'CD8_CT_QD_str', 'CD8_ie_str_IM_mean', 'CD8_ie_str_IM_min', 'CD8_ie_str_IM_median', 'CD8_ie_str_IM_max', 'CD8_ie_str_IM_CoV', 'CD8_ie_str_IM_QD', 'CD8_ie_str_CT_mean', 'CD8_ie_str_CT_min', 'CD8_ie_str_CT_median', 'CD8_ie_str_CT_max', 'CD8_ie_str_CT_CoV', 'CD8_ie_str_CT_QD', 'CD8_CD3_mean', 'CD8_CD3_min', 'CD8_CD3_median', 'CD8_CD3_max', 'CD8_CD3_IM_mean', 'CD8_CD3_IM_min', 'CD8_CD3_IM_median', 'CD8_CD3_IM_max', 'CD8_CD3_IM_mean_ie', 'CD8_CD3_IM_min_ie', 'CD8_CD3_IM_median_ie', 'CD8_CD3_IM_max_ie', 'CD8_CD3_IM_mean_str', 'CD8_CD3_IM_min_str', 'CD8_CD3_IM_median_str', 'CD8_CD3_IM_max_str', 'CD8_CD3_CT_mean', 'CD8_CD3_CT_min', 'CD8_CD3_CT_median', 'CD8_CD3_CT_max', 'CD8_CD3_CT_mean_ie', 'CD8_CD3_CT_min_ie', 'CD8_CD3_CT_median_ie', 'CD8_CD3_CT_max_ie', 'CD8_CD3_CT_mean_str', 'CD8_CD3_CT_min_str', 'CD8_CD3_CT_median_str', 'CD8_CD3_CT_max_str', 'Stroma_IM_mean', 'Stroma_IM_min', 'Stroma_IM_median', 'Stroma_IM_max', 'Stroma_IM_CoV', 'Stroma_IM_QD', 'Stroma_CT_mean', 'Stroma_CT_min', 'Stroma_CT_median', 'Stroma_CT_max', 'Stroma_CT_CoV', 'Stroma_CT_QD'])

## Step 1. ES : whole
fList = os.listdir(resDir)
CD3_Dict = {}
CD8_Dict = {}
print 'analyzing the entire tumor area...'
for f in fList:
    print f
    items = f.split('_')
    caseId = items[0]
    stain = items[1]

    # Construct tile dict
    # Id: tile name
    # Item: [[list of #Positive], [list of area]]
    tileDict_tumor = {}
    tileDict_stroma = {}
    tileList = []
    data = open(resDir+f).readlines()[1:]
    for d in data:
        items = d.split(',')
        if(len(items)>1):
            tileList.append(items[0])
            if(items[1]=='Tumor'):
                if(items[0] in tileDict_tumor.keys()):
                    #tileDict_tumor[items[0]]=[a+b for a, b in zip(tileDict_tumor[items[0]],[float(items[6]),float(items[-4]),float(items[-3])])]
                    tileDict_tumor[items[0]]=[a+b for a, b in zip(tileDict_tumor[items[0]],[[float(items[6])],[float(items[-3])]])]
                else:
                    #tileDict_tumor[items[0]]=[float(items[6]),float(items[-4]),float(items[-3])]
                    tileDict_tumor[items[0]]=[[float(items[6])],[float(items[-3])]]
            elif(items[1]=='Stroma'):
                if(items[0] in tileDict_stroma.keys()):
                    #tileDict_stroma[items[0]]=[a+b for a, b in zip(tileDict_stroma[items[0]],[float(items[6]),float(items[-4]),float(items[-3])])]
                    tileDict_stroma[items[0]]=[a+b for a, b in zip(tileDict_stroma[items[0]],[[float(items[6])],[float(items[-3])]])]
                else:
                    #tileDict_stroma[items[0]]=[float(items[6]),float(items[-4]),float(items[-3])]
                    tileDict_stroma[items[0]]=[[float(items[6])],[float(items[-3])]]

    # Record tile-wise info
    tumorTiles = tileDict_tumor.keys()
    strTiles = tileDict_stroma.keys()
    common = list(set(tumorTiles).intersection(set(strTiles)))
    tumorOnly = list(set(tumorTiles)-set(common))
    strOnly = list(set(strTiles)-set(common))

    # create tile-wise files
    tileF = open(tileDir+f,'wb')
    tileWriter = csv.writer(tileF, delimiter=',', lineterminator='\n')
    tileWriter.writerow(['tileName', 'density_ieTIL','density_strTIL','ie_str','count_total', 'count_ieTIL', 'count_strTIL', 'ratio_ie', 'ratio_str', 'Area_tumor', 'Area_stroma'])

    ie_count=[]
    ie_density=[] # numper / mm2
    str_count=[]
    str_density=[]
    ie_to_str = []
    total = []
    ie_ratio = []
    str_ratio = []
    tumor_area=[] # mm2
    str_area = []
    stroma_ratio = []

    for t in tumorOnly:
        ie_c = np.sum(tileDict_tumor[t][0])
        tumor_a = np.sum(tileDict_tumor[t][1])/100000
        ie_d = ie_c/tumor_a

        str_count.append(0)
        str_area.append(0)
        stroma_ratio.append(0)
        total.append(ie_c)

        # QC criteria: superpixel < 100um2 needs to be discarded
        if(ie_d<1000):
            ie_count.append(ie_c)
            ie_density.append(ie_d)
            tumor_area.append(tumor_a)

            # if ie_c==0, ratio becomes invalid
            # 'tileName', 'density_ieTIL','density_strTIL','ie_str','count_total', 'count_ieTIL', 'count_strTIL', 'ratio_ie', 'ratio_str', 'Area_tumor', 'Area_stroma'
            if(ie_c==0):
                tileWriter.writerow([t, ie_d,'NA','NA',ie_c, ie_c, 0, 'NA','NA',tumor_a,0])
            else:
                ie_ratio.append(1)
                str_ratio.append(0)
                tileWriter.writerow([t, ie_d,'NA','NA',ie_c, ie_c, 0, 1,0,tumor_a,0])
        else:
            ie_count.append(0)
            tumor_area.append(0)
            tileWriter.writerow([t, 'NA','NA','NA',ie_c, 0, 0, 'NA','NA',0,0])

    for t in strOnly:
        str_c = np.sum(tileDict_stroma[t][0])
        str_a = np.sum(tileDict_stroma[t][1])/100000
        str_d = str_c/str_a

        total.append(str_c)
        ie_count.append(0)
        tumor_area.append(0)

        if(str_d<1000):
            str_count.append(str_c)
            str_density.append(str_d)
            str_area.append(str_a)
            stroma_ratio.append(1)

            # if str_c==0, ratio becomes invalid
            # 'tileName', 'density_ieTIL','density_strTIL','ie_str','count_total', 'count_ieTIL', 'count_strTIL', 'ratio_ie', 'ratio_str', 'Area_tumor', 'Area_stroma'
            if(str_c==0):
                tileWriter.writerow([t, 'NA',str_d,'NA',str_c, 0, str_c, 'NA','NA',0,str_a])
            else:
                ie_ratio.append(0)
                str_ratio.append(1)
                tileWriter.writerow([t, 'NA',str_d,'NA',str_c, 0, str_c, 0,1,0,str_a])
        else:
            str_count.append(0)
            str_area.append(0)
            tileWriter.writerow([t, 'NA','NA','NA',str_c, 0, 0, 'NA','NA',0,0])

    for t in common:
        ie_c = np.sum(tileDict_tumor[t][0])
        tumor_a = np.sum(tileDict_tumor[t][1])/100000
        ie_d = ie_c/tumor_a

        str_c = np.sum(tileDict_stroma[t][0])
        str_a = np.sum(tileDict_stroma[t][1])/100000
        str_d = str_c/str_a

        total_c = ie_c+str_c
        total.append(total_c)

        if(ie_d<1000):
            ie_count.append(ie_c)
            ie_density.append(ie_d)
            tumor_area.append(tumor_a)

            if(str_d<1000):
                str_count.append(str_c)
                str_density.append(str_d)
                str_area.append(str_a)
                stroma_ratio.append(str_a/(str_a+tumor_a))

                # if total_c==0, ratio becomes invalid
                # 'tileName', 'density_ieTIL','density_strTIL','ie_str','count_total', 'count_ieTIL', 'count_strTIL', 'ratio_ie', 'ratio_str', 'Area_tumor', 'Area_stroma'
                if(total_c==0):
                    if(str_d!=0):
                        ie_to_str.append(ie_d/str_d)
                        tileWriter.writerow([t, ie_d,str_d,ie_to_str[-1],total_c, ie_c, str_c, 'NA','NA',tumor_a,str_a])
                    else: # ie_to_str becomes invalid
                        tileWriter.writerow([t, ie_d,str_d,'NA',total_c, ie_c, str_c, 'NA','NA',tumor_a,str_a])
                else:
                    ie_ratio.append(ie_c/total_c)
                    str_ratio.append(str_c/total_c)
                    if(str_d!=0):
                        ie_to_str.append(ie_d/str_d)
                        tileWriter.writerow([t, ie_d,str_d,ie_to_str[-1],total_c, ie_c, str_c, ie_ratio[-1],str_ratio[-1],tumor_a,str_a])
                    else:
                        tileWriter.writerow([t, ie_d,str_d,'NA',total_c, ie_c, str_c, ie_ratio[-1],str_ratio[-1],tumor_a,str_a])
            else: # stroma_a becomes invalid
                str_count.append(0)
                str_area.append(0)

                if(total_c==0):
                    tileWriter.writerow([t, ie_d,'NA','NA',total_c, ie_c, 0, 'NA','NA',tumor_a,0])
                else:
                    ie_ratio.append(ie_c/total_c)
                    tileWriter.writerow([t, ie_d,'NA','NA',total_c, ie_c, 0, ie_ratio[-1],'NA',tumor_a,0])
        else: # tumor_a becomes invalid
            ie_count.append(0)
            tumor_area.append(0)

            if(str_d<1000):
                str_count.append(str_c)
                str_density.append(str_d)
                str_area.append(str_a)
                stroma_ratio.append(1)

                if(total_c==0):
                    tileWriter.writerow([t, 'NA',str_d,'NA',total_c, 0, str_c, 'NA','NA',0,str_a])
                else:
                    str_ratio.append(str_c/total_c)
                    tileWriter.writerow([t, 'NA',str_d,'NA',total_c, 0, str_c, 'NA',str_ratio[-1],0,str_a])
            else: # stroma_a becomes invalid as well
                str_count.append(0)
                str_area.append(0)
                tileWriter.writerow([t, 'NA','NA','NA',total_c, 0, 0, 'NA','NA',0,0])

    # overall - mean - min - median - max - QD - CoV
    if('CD3' in stain):
        ieTIL = np.sum(ie_count)/np.sum(tumor_area)
        strTIL = np.sum(str_count)/np.sum(str_area)
        ie_str = ieTIL/strTIL
        CD3_Dict[caseId] = [ieTIL, strTIL, ie_str, np.mean(ie_density), np.mean(str_density), np.mean(ie_to_str), np.min(ie_density), np.min(str_density), np.min(ie_to_str), np.median(ie_density), np.median(str_density), np.median(ie_to_str),np.max(ie_density), np.max(str_density), np.max(ie_to_str), QD(ie_density), QD(str_density), QD(ie_to_str), CoV(ie_density), CoV(str_density), CoV(ie_to_str), np.sum(str_area)/(np.sum(str_area)+np.sum(tumor_area)), np.mean(stroma_ratio), np.min(stroma_ratio), np.median(stroma_ratio), np.max(stroma_ratio), QD(stroma_ratio), CoV(stroma_ratio)]
        #CD3_Dict[caseId] = [ieTIL, strTIL, ie_str, np.std(ie_density_rand)/np.mean(ie_density_rand), np.std(str_density_rand)/np.mean(str_density_rand), np.std(ie_to_str)/np.mean(ie_to_str), np.sum(str_area)/(np.sum(str_area)+np.sum(tumor_area)), np.std(str_rand)/np.mean(str_rand)]
    else:
        ieTIL = np.sum(ie_count)/np.sum(tumor_area)
        strTIL = np.sum(str_count)/np.sum(str_area)
        ie_str = ieTIL/strTIL
        CD8_Dict[caseId] = [ieTIL, strTIL, ie_str, np.mean(ie_density), np.mean(str_density), np.mean(ie_to_str), np.min(ie_density), np.min(str_density), np.min(ie_to_str), np.median(ie_density), np.median(str_density), np.median(ie_to_str),np.max(ie_density), np.max(str_density), np.max(ie_to_str), QD(ie_density), QD(str_density), QD(ie_to_str), CoV(ie_density), CoV(str_density), CoV(ie_to_str), np.sum(str_area)/(np.sum(str_area)+np.sum(tumor_area)), np.mean(stroma_ratio), np.min(stroma_ratio), np.median(stroma_ratio), np.max(stroma_ratio), QD(stroma_ratio), CoV(stroma_ratio)]
        #CD8_Dict[caseId] = [ieTIL, strTIL, ie_str, np.std(ie_density_rand)/np.mean(ie_density_rand), np.std(str_density_rand)/np.mean(str_density_rand), np.std(ie_to_str)/np.mean(ie_to_str), np.sum(str_area)/(np.sum(str_area)+np.sum(tumor_area)), np.std(str_rand)/np.mean(str_rand)]

    tileF.close()

## Step 2. ES : IM and CT
caseList = os.listdir(tileDir)
CD3_dict_ = {}
CD8_dict_ = {}
print 'analyzing IM and CT separately....'
for c in caseList:
    if('.csv' in c):
        cName = c.split('_')[0]
        print cName
        total = []
        IM = []
        CT = []
        IM_ie = []
        CT_ie = []
        IM_str = []
        CT_str = []
        IM_ie_str = []
        CT_ie_str = []
        Stroma_IM = []
        Stroma_CT = []

        tList = open(tileDir+c).readlines()[1:]
        for tile in tList:
            tInfo = tile.split(',')
            tName = tInfo[0]

            total.append(float(tInfo[4]))
            # IM
            if('IM' in tName):
                IM.append(float(tInfo[4]))

                if(tInfo[1]!='NA'):
                    IM_ie.append(float(tInfo[1]))

                if(tInfo[2]!='NA'):
                    IM_str.append(float(tInfo[2]))

                if(tInfo[3]!='NA'):
                    IM_ie_str.append(float(tInfo[3]))

                Stroma_IM.append(float(tInfo[10])/(float(tInfo[9])+float(tInfo[10])))
            else:
                CT.append(float(tInfo[4]))

                if(tInfo[1]!='NA'):
                    CT_ie.append(float(tInfo[1]))

                if(tInfo[2]!='NA'):
                    CT_str.append(float(tInfo[2]))

                if(tInfo[3]!='NA'):
                    CT_ie_str.append(float(tInfo[3]))

                Stroma_CT.append(float(tInfo[10])/(float(tInfo[9])+float(tInfo[10])))

        summary_total = [np.mean(total), np.min(total), np.median(total), np.max(total), CoV(total), QD(total)]
        if(len(IM)!=0):
            summary_IM = [np.mean(IM), np.min(IM), np.median(IM), np.max(IM), CoV(IM), QD(IM)]
        else:
            summary_IM = [0,0,0,0,0,0]
            print cName+": zero IM"


        if(len(IM_ie)!=0):
            summary_IM_ie = [np.mean(IM_ie), np.min(IM_ie), np.median(IM_ie), np.max(IM_ie), CoV(IM_ie), QD(IM_ie)]
        else:
            summary_IM_ie = [0,0,0,0,0,0]
            print cName+": zero IM_ie"

        if(len(IM_str)!=0):
            summary_IM_str = [np.mean(IM_str), np.min(IM_str), np.median(IM_str), np.max(IM_str), CoV(IM_str), QD(IM_str)]
        else:
            summary_IM_str = [0,0,0,0,0,0]
            print cName+": zero IM_str"

        if(len(CT)!=0):
            summary_CT = [np.mean(CT), np.min(CT), np.median(CT), np.max(CT), CoV(CT), QD(CT)]
        else:
            summary_CT = [0,0,0,0,0,0]
            print cName+": zero CT"

        if(len(CT_ie)!=0):
            summary_CT_ie = [np.mean(CT_ie), np.min(CT_ie), np.median(CT_ie), np.max(CT_ie), CoV(CT_ie), QD(CT_ie)]
        else:
            summary_CT_ie = [0,0,0,0,0,0]
            print cName+": zero CT_ie"

        if(len(CT_str)!=0):
            summary_CT_str = [np.mean(CT_str), np.min(CT_str), np.median(CT_str), np.max(CT_str), CoV(CT_str), QD(CT_str)]
        else:
            summary_CT_str = [0,0,0,0,0,0]
            print cName+": zero CT_str"

        if(len(IM_ie_str)!=0):
            summary_IM_ie_str = [np.mean(IM_ie_str), np.min(IM_ie_str), np.median(IM_ie_str), np.max(IM_ie_str), CoV(IM_ie_str), QD(IM_ie_str)]
        else:
            summary_IM_ie_str = [0,0,0,0,0,0]
            print cName+": zero IM_ie_str"

        if(len(CT_ie_str)!=0):
            summary_CT_ie_str = [np.mean(CT_ie_str), np.min(CT_ie_str), np.median(CT_ie_str), np.max(CT_ie_str), CoV(CT_ie_str), QD(CT_ie_str)]
        else:
            summary_CT_ie_str = [0,0,0,0,0,0]
            print cName+": zero CT_ie_str"

        if(len(Stroma_IM)!=0):
            summary_str_IM = [np.mean(Stroma_IM), np.min(Stroma_IM), np.median(Stroma_IM), np.max(Stroma_IM), CoV(Stroma_IM), QD(Stroma_IM)]
        else:
            summary_str_IM  = [0,0,0,0,0,0]
            print cName+": zero Stroma_IM"

        if(len(Stroma_CT)!=0):
            summary_str_CT = [np.mean(Stroma_CT), np.min(Stroma_CT), np.median(Stroma_CT), np.max(Stroma_CT), CoV(Stroma_CT), QD(Stroma_CT)]
        else:
            summary_str_CT  = [0,0,0,0,0,0]
            print cName+": zero Stroma_CT"

        if('CD3' in c):
            CD3_dict_[cName] = summary_total+summary_IM+summary_IM_ie+summary_IM_str+summary_CT+summary_CT_ie+summary_CT_str+summary_IM_ie_str+summary_CT_ie_str+summary_str_IM+summary_str_CT
        else:
            CD8_dict_[cName] = summary_total+summary_IM+summary_IM_ie+summary_IM_str+summary_CT+summary_CT_ie+summary_CT_str+summary_IM_ie_str+summary_CT_ie_str+summary_str_IM+summary_str_CT

## Record
caseList = CD3_Dict.keys()
for caseId in caseList:
    CD3_ie = CD3_Dict[caseId][0]
    CD3_str = CD3_Dict[caseId][1]
    CD8_ie = CD8_Dict[caseId][0]
    CD8_str = CD8_Dict[caseId][1]

    CD3_ie_mean = CD3_Dict[caseId][3]
    CD3_str_mean = CD3_Dict[caseId][4]
    CD8_ie_mean = CD8_Dict[caseId][3]
    CD8_str_mean = CD8_Dict[caseId][4]

    CD3_ie_min = CD3_Dict[caseId][6]
    CD3_str_min = CD3_Dict[caseId][7]
    CD8_ie_min = CD8_Dict[caseId][6]
    CD8_str_min = CD8_Dict[caseId][7]

    CD3_ie_median = CD3_Dict[caseId][9]
    CD3_str_median = CD3_Dict[caseId][10]
    CD8_ie_median = CD8_Dict[caseId][9]
    CD8_str_median = CD8_Dict[caseId][10]

    CD3_ie_max = CD3_Dict[caseId][12]
    CD3_str_max = CD3_Dict[caseId][13]
    CD8_ie_max = CD8_Dict[caseId][12]
    CD8_str_max = CD8_Dict[caseId][13]

    CD3_trunc = CD3_dict_[caseId][:-12]
    CD8_trunc = CD8_dict_[caseId][:-12]

    CD3_measures = CD3_trunc[0:4]+CD3_trunc[6:10]+CD3_trunc[12:16]+CD3_trunc[18:22]+CD3_trunc[24:28]+CD3_trunc[30:34]+CD3_trunc[36:40]
    CD8_measures = CD8_trunc[0:4]+CD8_trunc[6:10]+CD8_trunc[12:16]+CD8_trunc[18:22]+CD8_trunc[24:28]+CD8_trunc[30:34]+CD8_trunc[36:40]

    Str_CD3 = CD3_dict_[caseId][-12:]
    Str_CD8 = CD8_dict_[caseId][-12:]

    res.writerow([caseId]+CD3_Dict[caseId][:-7]+CD8_Dict[caseId][:-7]+[ratio(CD8_ie,CD3_ie), ratio(CD8_str,CD3_str), ratio(CD8_ie_mean,CD3_ie_mean), ratio(CD8_str_mean,CD3_str_mean), ratio(CD8_ie_min,CD3_ie_min), ratio(CD8_str_min,CD3_str_min), ratio(CD8_ie_median,CD3_ie_median), ratio(CD8_str_median,CD3_str_median), ratio(CD8_ie_max,CD3_ie_max), ratio(CD8_str_max,CD3_str_max)]+[np.mean([CD3_Dict[caseId][-7],CD8_Dict[caseId][-7]]), np.mean([CD3_Dict[caseId][-6],CD8_Dict[caseId][-6]]),np.mean([CD3_Dict[caseId][-5],CD8_Dict[caseId][-5]]),np.mean([CD3_Dict[caseId][-4],CD8_Dict[caseId][-4]]),np.mean([CD3_Dict[caseId][-3],CD8_Dict[caseId][-3]]),np.mean([CD3_Dict[caseId][-2],CD8_Dict[caseId][-2]]),np.mean([CD3_Dict[caseId][-1],CD8_Dict[caseId][-1]])]+CD3_trunc+CD8_trunc+[ratio(y,x) for x,y in zip(CD3_measures, CD8_measures)]+[np.mean([x,y]) for x, y in zip(Str_CD3,Str_CD8)])

## The end
resF.close()
end = time.time()
print str((end-start)/60)+' minutes'
