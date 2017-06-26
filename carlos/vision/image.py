import sys
import time

from naoqi import ALProxy

# To get the constants relative to the video.
import vision_definitions

class Image:

    # sets the volume to a default value
    def __init__(self, IP, PORT):
        self._videoProxy = ALProxy("ALVideoDevice", IP, PORT)
        
    def start(self):
        resolution = vision_definitions.k960p  # 1280
        colorSpace = vision_definitions.kRGBColorSpace

        self._imgClient = self._videoProxy.subscribe("_client", resolution, colorSpace, 5)

        # Select camera.
        self._videoProxy.setParam(vision_definitions.kCameraSelectID,
                                  0)

    def stop(self):
        if self._imgClient != "":
            self._videoProxy.unsubscribe(self._imgClient)
    
    def getImage(self):
        return self._videoProxy.getImageRemote(self._imgClient)
