import numpy as np
import cv2
import urllib2
from scipy.spatial import distance as dist
import argparse
import glob
import Image
import os


class ImageComparer:
    @staticmethod
    def download_image(image_url, file_name):
        page = urllib2.build_opener().open(image_url)
        image = page.read()
        print 'im here'

        if '.gif' in image_url:
            file_name += '.gif'
        elif '.jpg' in image_url or '.jpeg' in image_url:
            file_name += '.png'
        elif '.png' in image_url:
            file_name += '.png'

        print file_name
        fout = open(file_name, 'wb')
        fout.write(image)
        fout.close()

        if 'gif' in file_name:  # convert gif to png
            ImageComparer.convert_gif_to_png(file_name)
            return file_name[:-4] + '.png'
        return file_name

    @staticmethod
    def convert_gif_to_png(file_name):  # Converts gif to png
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

    @staticmethod
    def _change_images_to_equal_size(img1, img2):
        rows1, cols1, colors1 = img1.shape
        rows2, cols2, colors2 = img2.shape

        height = min(rows1, rows2)
        width = min(cols1, cols2)

        return cv2.resize(img1, (height, width)),  cv2.resize(img2, (height, width))

    @staticmethod
    def compare_images(img1_path, img2_path):
        img1 = cv2.imread(img1_path, cv2.IMREAD_COLOR)
        img2 = cv2.imread(img2_path, cv2.IMREAD_COLOR)
        img1, img2 = ImageComparer._change_images_to_equal_size(img1, img2)

        #cv2.imwrite('orig.png', img1)
        #cv2.imwrite('rep.png', img2)

        img1_tpl = ImageComparer.split_image(img1)
        img2_tpl = ImageComparer.split_image(img2)
        sum_corr = 0

        for i in range(0, 4):
            img = img1_tpl[i]
            img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
            hist1 = ImageComparer.calculate_histogram(img, 2)
            img = img2_tpl[i]
            img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
            hist2 = ImageComparer.calculate_histogram(img, 2)
            res = cv2.compareHist(hist1, hist2, 0)
            sum_corr += res

        print sum_corr / 4.0
        return sum_corr / 4.0

    @staticmethod
    def split_image(img):
        r = 2

        height, width, _ = img.shape
        split1 = img[0:height/r, 0:width/r]
        split2 = img[0:height/r, width/r:]
        split3 = img[height/r:, 0:width/r]
        split4 = img[height/r:, width/r:]

        return split1, split2, split3, split4

    @staticmethod
    def calculate_histogram(img, num=3):
        if num == 3:
            return cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        elif num == 2:
            return cv2.calcHist([img], [0, 1], None, [16, 16], [0, 256, 0, 256])
        else:
            return cv2.calcHist([img], [0], None, [8], [0, 256])


if __name__ == '__main__':
    im1 = cv2.imread('germany.png')
    ImageComparer.download_image('https://40.media.tumblr.com/tumblr_lnska0FOKO1qakbgvo1_500.jpg', 'test')
    im2 = cv2.imread('test.png')

    im1, im2 = ImageComparer._change_images_to_equal_size(im1, im2)

    print im1.shape

    lst = ImageComparer.split_image(im1)
    for i in range(0, 4):
        cv2.imshow(str(i), lst[i])
        print lst[i].shape

    lst = ImageComparer.split_image(im2)
    for i in range(0, 4):
        cv2.imshow(str(i+10), lst[i])
        print lst[i].shape

    print ImageComparer.compare_images('germany.png', 'test.png')

    cv2.waitKey(0)
    cv2.destroyAllWindows()
