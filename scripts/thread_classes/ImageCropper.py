import cv2
import threading
import random
from scripts.helper_tools import displayImage

class ImageCropper(threading.Thread):
    def __init__(self, imageNames, path, output, res, split):
        threading.Thread.__init__(self)
        self.__imageNames = imageNames
        self.__path = path
        self.__output = output
        self.__res = res
        self.__numImages = len(self.__imageNames)
        self.__progress = 0
        self.__alive = True
        self.__split = split

    def isAlive(self):
        return self.__alive

    def kill(self):
        self.__alive = False

    def getProgress(self):
        return (self.__progress / self.__numImages) * 100

    def run(self):
        '''
        (w, h) = self.__res
        w_new = w - self.__split
        w_split = -1 * self.__split
        sizes = ['full', 'half', 'quarter']
        #print(f'width: {w} | height: {h} | new width: {w_new}')
        for imageName in self.__imageNames:
            images_X = []
            images_Y = []
            image = cv2.imread(self.__path + imageName)
            images_X.append(image[:, :w_new])
            images_X.append(cv2.resize(images_X[0], (w_new//2, h//2)))
            images_X.append(cv2.resize(images_X[0], (w_new//4, h//4)))
            images_Y.append(image[:, w_split:])
            images_Y.append(cv2.resize(images_Y[0], (self.__split//2, h//2)))
            images_Y.append(cv2.resize(images_Y[0], (self.__split//4, h//4)))
            for i, size in enumerate(sizes):
                cv2.imwrite(f'{self.__output}{size}/X/{imageName[:-4]}.jpg', images_X[i])
                cv2.imwrite(f'{self.__output}{size}/Y/{imageName[:-4]}.jpg', images_Y[i])
            if(not self.__alive):
                return
            self.__progress += 1
        '''
        ####
        sizes = ['full', 'half', 'quarter']
        for imageName in self.__imageNames:
            image = cv2.imread(self.__path + imageName)
            w = image.shape[0]
            h = image.shape[1]
            image = cv2.resize(image, (h//4, w//4))
            cv2.imwrite(f'{self.__output}{sizes[2]}/{imageName[:-4]}.jpg', image)
            if(not self.__alive):
                return
            self.__progress += 1
        ####
        self.__progress = 100
        self.__alive = False

