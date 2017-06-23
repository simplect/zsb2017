from naoqi import ALProxy
photoProxy = ALProxy("ALPhotoCapture", "169.254.35.27", 9559)
photoProxy.setResolution(3)
photoProxy.setPictureFormat("jpg")
print(photoProxy.takePictures(1, "images/", "image"))
