import numpy as np
import cv2
import urllib2
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import argparse
import glob



class ImageComparer:
    def __init__(self):
        pass

    @staticmethod
    def download_image(image_url, file_name):
        page = urllib2.build_opener().open(image_url)
        image = page.read()
        fout = open(file_name, 'wb')
        fout.write(image)
        fout.close

if __name__ == '__main__':
    index = {}
    images = {}

    image = cv2.imread('russian_federation.gif')
    images['russian_federation.gif'] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    print images

