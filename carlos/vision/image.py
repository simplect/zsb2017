# image.py

# Merijn Testroote, 11173106
# Babette Mooij, 10740414
# Alexandra Spruit, 11262273
# Hannah Min, 11011580

# This code has been developed for the course ZSB 2017
# at the University of Amsterdam

# 30-06-2017 - We take no responsibility for the 
# effects of this software nor if Carlos is taking over the
# world or getting around in fancy cars and winning all poker games.
# The code is served as is.

import sys
import time
from PIL import Image

from naoqi import ALProxy

# To get the constants relative to the video.
import vision_definitions

class Vision:

    # sets the volume to a default value
    def __init__(self):
        self._videoProxy = ALProxy("ALVideoDevice")

    def getImage(self, img_name):
        resolution = vision_definitions.k960p  # 1280
        resolution = 2
        colorSpace = vision_definitions.kRGBColorSpace
        colorSpace = 11

        imgClient = self._videoProxy.subscribe("python_client", resolution, colorSpace, 5)

        # Select camera.
        self._videoProxy.setParam(vision_definitions.kCameraSelectID,
                                  1)

        naoImage = self._videoProxy.getImageRemote(imgClient)

        self._videoProxy.unsubscribe(imgClient)

        imageWidth = naoImage[0]
        imageHeight = naoImage[1]
        array = naoImage[6]

        # Create a PIL Image from our pixel array.
        im = Image.frombytes("RGB", (imageWidth, imageHeight), array)

        # Save the image.
        im.save(img_name, "JPeG")
