'''
Copyright (c) 2025 Cameron S. Bodine
'''

#########
# Imports
import os
import time
import datetime

start_time = time.time()

# Set MONSTURMAPPER utils dir
USER_DIR = os.path.expanduser('~')
MM_UTILS_DIR = os.path.join(USER_DIR, '.monsturmapper')
os.makedirs(MM_UTILS_DIR, exist_ok=True)


def gui():
    '''
    Placeholder GUI launcher.
    '''

    #################
    # NEED TO ADD GUI

    # FOR DEVELOPMENT
    #############################
    seg_model = 'monstur_substrate_v2'
    inDir = r'/mnt/z/UDEL/Projects/HudsonRiver_Substrate/data/data_PINGMapper/20260601_HUD_CAT_Rec00007/sonar_mosaic'
    mosaicFileType = '.tif'
    outDirTop = r'/mnt/z/scratch/MonSturMapper_Debug'
    projName = 'monstur_mapper_test'
    mapRast = True
    mapShp = True

    epsg = 32618

    windowSize_m = (18, 18)
    window_stride = 9
    minArea_percent = 0.75
    threadCnt = 0.75

    predBatchSize = 30

    minPatchSize_m2 = 18
    smoothShp = True
    smoothTol_m = 0.3

    deleteIntData = True

    ################
    # Run MonSturMapper

    modelDir = os.path.join(MM_UTILS_DIR, 'models')

    supported_models = [
        'monstur_substrate_v2',
    ]

    if seg_model in supported_models:
        modelDir = os.path.join(modelDir, seg_model)
    else:
        raise ValueError(
            'seg_model not recognized: {}. Supported models: {}'.format(
                seg_model,
                ', '.join(supported_models),
            )
        )

    from monsturmapper.monstur_mapper import do_work

    print('\n\nMapping habitat with MONSTURMAPPER model...\n\n')
    do_work(
        inDir=inDir,
        outDirTop=outDirTop,
        projName=projName,
        mapRast=mapRast,
        mapShp=mapShp,
        epsg=epsg,
        windowSize_m=windowSize_m,
        window_stride=window_stride,
        minArea_percent=minArea_percent,
        threadCnt=threadCnt,
        mosaicFileType=mosaicFileType,
        modelDir=modelDir,
        predBatchSize=predBatchSize,
        deleteIntData=deleteIntData,
        minPatchSize=minPatchSize_m2,
        smoothShp=smoothShp,
        smoothTol_m=smoothTol_m,
    )

    print(
        "\n\nGrand Total Processing Time: ",
        datetime.timedelta(seconds=round(time.time() - start_time, ndigits=0)),
    )


if __name__ == "__main__":
    gui()
