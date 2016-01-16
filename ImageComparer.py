import numpy as np
import cv2
import urllib2
from scipy.spatial import distance as dist
import argparse
import glob
import Image
import os


class ImageType:
    GIF = 0
    JPEG = 1
    PNG = 2


class ImageComparer:
    @staticmethod
    def download_image(image_url, file_name):
        page = urllib2.build_opener().open(image_url)
        image = page.read()

        if 'gif' in image_url:
            file_name += '.gif'
        elif 'jpg' in image_url or 'jpeg' in image_url:
            file_name += '.jpg'
        elif 'png' in image_url:
            file_name += '.png'

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

        return cv2.resize(img1, (width, height)),  cv2.resize(img2, (width, height))

    @staticmethod
    def compare_images(img1_path, img2_path):
        img1 = cv2.imread(img1_path, cv2.IMREAD_COLOR)
        img2 = cv2.imread(img2_path, cv2.IMREAD_COLOR)
        img1, img2 = ImageComparer._change_images_to_equal_size(img1, img2)

        cv2.imwrite('orig.png', img1)
        cv2.imwrite('rep.png', img2)

        hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

        print hist1.shape

        res = cv2.compareHist(hist1, hist2, 0)
        print res
        return res


if __name__ == '__main__':
    ImageComparer.download_image('http://www.flagipanstw.eu/images/1/flaga-austrii.png', 'unknown')
    aus = cv2.imread('austria.png', cv2.IMREAD_COLOR)
    img = cv2.imread('unknown.png', cv2.IMREAD_COLOR)
    aus, img = ImageComparer._change_images_to_equal_size(aus, img)

    hist1 = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.calcHist([aus], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

    res = cv2.compareHist(hist1, hist2, 0)
    print res

    cv2.waitKey(0)
    cv2.destroyAllWindows()
