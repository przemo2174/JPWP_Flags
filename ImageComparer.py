import numpy as np
import cv2
import urllib2
from scipy.spatial import distance as dist
import argparse
import glob
import Image
import os


class ImageComparer:
    def __init__(self):
        pass

    @staticmethod
    def download_image(image_url, file_name):
        file_name += '.gif'
        print file_name
        page = urllib2.build_opener().open(image_url)
        image = page.read()
        fout = open(file_name, 'wb')
        fout.write(image)
        fout.close()
        ImageComparer.process_image(file_name)

    @staticmethod
    def process_image(file_name):  # Converts gif to png
        try:
            fh = open(file_name, 'rb')
            im = Image.open(fh)
            im.load()
        except IOError:
            print "Cant load", file_name
            return
        i = 0
        my_palette = im.getpalette()

        try:
            while 1:
                im.putpalette(my_palette)
                new_im = Image.new("RGBA", im.size)
                new_im.paste(im)
                new_im.save(file_name[:-4] + '.png')

                i += 1
                im.seek(im.tell() + 1)

        except EOFError:
            fh.close()
            os.remove(file_name)

if __name__ == '__main__':
    img = cv2.imread('unknown.png', cv2.IMREAD_GRAYSCALE)
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    print hist[255]
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
