import cv2
import numpy as np
import random
import progressbar
import time
import os

from .thread_classes.ImageCropper import ImageCropper
from .helper_tools import displayImage, getImageNames
from data.data import getData

def cropper():
    files = getData()
    if (files == 0):
        return 0
    
    path = files['output']+files['number']
    path_frames = files['path']+files['number']

    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(path+"full/"):
        os.mkdir(path+"full/")
        os.mkdir(path+"full/"+"X")
        os.mkdir(path+"full/"+"Y")
    if not os.path.exists(path+"half/"):
        os.mkdir(path+"half/")
        os.mkdir(path+"half/"+"X")
        os.mkdir(path+"half/"+"Y")
    if not os.path.exists(path+"quarter/"):
        os.mkdir(path+"quarter/")
        os.mkdir(path+"quarter/"+"X")
        os.mkdir(path+"quarter/"+"Y")

    imageNames = getImageNames(path_frames)
    threads = []
    NUM_THREADS = 16
    length = len(imageNames)

    for i in range(0, NUM_THREADS):
        imagesNames_i = imageNames[i*length//NUM_THREADS:(i+1)*length//NUM_THREADS]
        #print(len(imagesNames_i))
        #print(imagesNames_i[:5])
        #print(path_frames)
        imageCropper = ImageCropper(
            imagesNames_i,
            path_frames, files['output']+files['number'],
            files['resolution'], files['split'])
        threads.append(imageCropper)
    for t in threads:
        t.start()

    try:
        with progressbar.ProgressBar(max_value=100.0) as bar:
            active = True
            while(active):
                isDead = True
                progress = 0.
                for t in threads:
                    isDead = isDead and not t.isAlive()
                    progress += t.getProgress()
                if(isDead):
                    active = False
                progress = min(round(progress / NUM_THREADS, 2), 100)
                bar.update(progress)
                time.sleep(0.1)
    except KeyboardInterrupt:
        for t in threads:
            t.kill()
            t.join()
        return 0

    for t in threads:
        t.join()

    return 1