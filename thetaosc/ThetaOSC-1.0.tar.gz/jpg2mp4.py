#!python
#-*- coding:utf-8 -*

import cv2
import os
import glob

writer = cv2.VideoWriter ()
if not writer.open("animation.mp4v",
                   cv2.VideoWriter_fourcc(*"mp4v"),
                   1,#fps
                   (963,448), #frame_size
                   isColor=True):
    print ("failed to open writer")
    sys.exit()

for imgfile in glob.iglob("../Images/*[!-thmb].JPG"):
    img=cv2.imread(imgfile)
    h,w,d=img.shape
    simg=cv2.resize(img,(963,448))
    cv2.imshow("image",simg)
    cv2.waitKey(10)
    writer.write(simg)


writer.release()

if ext == "mp4v":
    # "Free MP4 Converter" does not recognise ".mp4v" extension.
    newfname=os.path.join(os.path.abspath("."),"converted.mp4")
    os.rename(fname,newfname)
