from concurrent.futures.thread import ThreadPoolExecutor

import numpy as np


class Algorithm:
    def __init__(self):

        self.__rgb2lms = np.zeros((3,3), dtype='float')
        self.__rgb2lms = np.array([[17.8824, 43.5161, 4.11935], [3.45565, 27.1554, 3.86714], [0.0299566, 0.184309, 1.46709]])
        self.__lms2rgb = np.linalg.inv(self.__rgb2lms)

        self.__lmsPro = np.array([[0, 2.02344, -2.52581], [0, 1, 0], [0, 0, 1]])
        self.__lmsDeu = np.array([[1, 0, 0], [0.494207, 0, 1.24827], [0, 0, 1]])
        self.__lmsTri = np.array([[1, 0, 0], [0, 1, 0], [-0.395913, 0.801109, 0]])

        self.__corrPro = np.array([[0, 0, 0], [0.7, 1, 0], [0.7, 0, 1]])
        self.__corrDeu = np.array([[1, 0.7, 0], [0, 0, 0], [0, 0.7, 1]])
        self.__corrTri = np.array([[1, 0, 0.7], [0, 1, 0.7], [0, 0, 0]])

        self.__imgP = self.__lms2rgb @ (self.__lmsPro @ self.__rgb2lms)
        self.__imgD = self.__lms2rgb @ (self.__lmsDeu @ self.__rgb2lms)
        self.__imgT = self.__lms2rgb @ (self.__lmsTri @ self.__rgb2lms)

    def imgPro(self, img, x, y, z):
        imgt = img.transpose(2, 0, 1).reshape(3, -1)
        img = self.__imgP @ imgt
        img[img > 255] = 255
        img[img < 0] = 0
        img += self.__corrPro @ (imgt - img)
        img[img > 255] = 255
        img[img < 0] = 0
        img = img.reshape(z, x, y).transpose(1, 2, 0).astype('uint8')
        return img

    def imgDeu(self, img, x, y, z):
        imgt = img.transpose(2, 0, 1).reshape(3,-1)
        img = self.__imgD @ imgt
        img[img>255]=255
        img[img<0]=0
        img += self.__corrDeu @ (imgt - img)
        img[img>255]=255
        img[img<0]=0
        img = img.reshape(z, x, y).transpose(1, 2, 0).astype('uint8')
        return img

    def imgTri(self, img, x, y, z):
        imgt = img.transpose(2, 0, 1).reshape(3,-1)
        img = self.__imgT @ imgt
        img[img>255]=255
        img[img<0]=0
        img += self.__corrTri @ (imgt - img)
        img[img>255]=255
        img[img<0]=0
        img = img.reshape(z, x, y).transpose(1, 2, 0).astype('uint8')
        return img

    def threadPro(self, img, x, y, z, threads):
        executor = ThreadPoolExecutor(max_workers=threads)

        yh = int(y / int(threads / 2))
        xh = int(x / 2)

        newList = []

        for i in range(int(threads/2)):
            newList.append(executor.submit(self.imgPro, img[0:xh, i * yh:yh * (i + 1)], xh, yh, z))
            newList.append(executor.submit(self.imgPro, img[xh:x, i * yh:yh * (i + 1)], xh, yh, z))

        for i in range(int(threads/2)):
            img[0:xh, i * yh:yh * (i + 1)] = newList[i*2].result()
            nr=i*2+1
            img[xh:x, i * yh:yh * (i + 1)] = newList[nr].result()

        return img

    def threadDeu(self, img, x, y, z, threads):
        executor = ThreadPoolExecutor(max_workers=threads)

        yh = int(y / int(threads / 2))
        xh = int(x / 2)

        newList = []

        for i in range(int(threads/2)):
            newList.append(executor.submit(self.imgDeu, img[0:xh, i * yh:yh * (i + 1)], xh, yh, z))
            newList.append(executor.submit(self.imgDeu, img[xh:x, i * yh:yh * (i + 1)], xh, yh, z))

        for i in range(int(threads/2)):
            img[0:xh, i * yh:yh * (i + 1)] = newList[i*2].result()
            nr=i*2+1
            img[xh:x, i * yh:yh * (i + 1)] = newList[nr].result()

        return img

    def threadTri(self, img, x, y, z, threads):
        executor = ThreadPoolExecutor(max_workers=threads)

        yh = int(y / int(threads / 2))
        xh = int(x / 2)

        newList = []

        for i in range(int(threads/2)):
            newList.append(executor.submit(self.imgTri, img[0:xh, i * yh:yh * (i + 1)], xh, yh, z))
            newList.append(executor.submit(self.imgTri, img[xh:x, i * yh:yh * (i + 1)], xh, yh, z))

        for i in range(int(threads/2)):
            img[0:xh, i * yh:yh * (i + 1)] = newList[i*2].result()
            nr=i*2+1
            img[xh:x, i * yh:yh * (i + 1)] = newList[nr].result()

        return img
