from selenium import webdriver
import os
import glob
import subprocess
import time

class slide2pdf:
    def __init__(self, url, no_of_slides, height, width):
        self.url = url
        self.slides = int(no_of_slides)
        self.browser = webdriver.Firefox()
        self.browser.set_window_size(height, width)
        self.browser.get(self.url)

    def snap_shot(self):
        subprocess.call(["xdotool", "key", "Return"])

        for num in range(self.slides):
            self.browser.save_screenshot("frame%02d.png" % num)
            subprocess.call(["xdotool", "key", "space"])
            time.sleep(1)

    def convert_pdf(self):
        filepath = os.path.basename(self.url)
        filename = os.path.splitext(filepath)[0]
        subprocess.call(["convert", "frame*.png", filename + ".pdf"])
        self.__remove_files()
        self.browser.quit()

    def __remove_files(self):
        files = glob.glob("*.png")
        for f in files:
            os.remove(f)
