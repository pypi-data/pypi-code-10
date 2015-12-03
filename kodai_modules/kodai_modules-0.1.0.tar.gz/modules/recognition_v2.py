# -*- coding: UTF-8 -*-

#-------------------------------------------------------------------------
# Name:        recognition_v2
# Purpose:     GreyNaoのマイクを利用した音声認識モジュール
#                 開発が困難で認識率が上がらないので, 現状ではAmiVoiceは無効化
#              NaoQi2.1でのモジュール変更に伴うプログラムの変更
#
# Author:      y_mori
#
# Created:     19/09/2014
# Copyright:   (c) y_mori 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------

import os
import subprocess
import re
import sys
import time
import datetime
import paramiko
import urllib2
import socket

# from ip import IP

from naoqi import *
#import dynamicDict

pat = re.compile("\d+")
pat2 = re.compile("sentence1: silB.+silE")

#GOOGLEAPI = "https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=ja-JP&maxresults=5"
#GOOGLEAPI = "https://www.google.com/speech-api/v2/recognize?xjerr=1&client=chromium&lang=ja-JP&maxresults=5&key=AIzaSyAj-KXSdwDRWadwB7DtvoD8Z87McwY9uk4"
#GOOGLEAPI = "https://www.google.com/speech-api/v2/recognize?=json&lang=ja-JP&key=AIzaSyAj-KXSdwDRWadwB7DtvoD8Z87McwY9uk4"
GOOGLEAPI = "https://www.google.com/speech-api/v2/recognize?output=json&lang=ja&key=AIzaSyB62cr1jxkHEsmi3SHj2jJmFWD1usdwrIk"


ANDROIDIP = "192.168.128.41"
ORANGE_NAO = "192.168.11.7"
"""
hikawaandroid_ip:192.168.11.30
lifetouchandroid_ip:192168.11.6
"""


class Recognition():

    # コンストラクタ
    def __init__(self, naoip):
        self.nao_ip = naoip  # 接続するNaoのipアドレス

        """
        # Amivoiceエディタの起動
        subprocess.Popen("C:/Aldebaran/SDK-2.1/modules/Japanese/Recognition/Engine/editor.vtxt", shell = True) # editor.vtxtのフルパス
        #time.sleep(1)
        """
        while True:
            try:
                # ALProxy
                self.audioProxy = ALProxy("ALAudioDevice", self.nao_ip, 9559)
                self.memProxy = ALProxy("ALMemory", self.nao_ip, 9559)
                self.leds = ALProxy("ALLeds", self.nao_ip, 9559)
                self.aup = ALProxy("ALAudioPlayer", self.nao_ip, 9559)
                #self.soundProxy = ALProxy("ALSoundProcessing", self.nao_ip, 9559)
                self.soundProxy = ALProxy(
                    "ALSpeechRecognition", self.nao_ip, 9559)
                self.frame = ALProxy("ALFrameManager", self.nao_ip, 9559)
                break
            except RuntimeError, e:
                raise e
                print exit(0)
                #raise ValueError("ERROR when creating some proxys")

        # 目のLEDを白に
        self.leds.fadeRGB("FaceLeds", 256 * 256 * 255 + 256 * 255 + 255, 0.5)

        """
        # pywinautoを接続
        self.app = application.Application()
        self.processID = self._getPID("AmiVoice")
        self.app.connect_(process = self.processID)
        """

        # start SSH (to send speechdata from Nao to PC)
        self.conn = None
        try:
            # SSHで接続
            print "..:: NOW CONNECTING ::.."
            self.conn = paramiko.SSHClient()
            self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.conn.connect(self.nao_ip, username="nao", password="nao")
            print "..:: SUCCESS CONNECTING ::.."

            # sftpセッションを開く
            self.sftp = self.conn.open_sftp()
            print self.sftp.listdir()
            self.sftp.chdir("VoiceFile")
        except IOError as e:
            print e
            raise ValueError("ERROR when SSH connecting")
            print exit(1)

        self.soundProxy.subscribe("Recog")

        # 閾値を取得 (1秒間)
        print "Measuring noise..."
        noiseVolumeList = list()
        self.audioProxy.enableEnergyComputation()
        for i in range(5):
            # noiseVolumeList.append(self.memProxy.getData("ALSoundProcessing/frontMicEnergy"))
            # #SDK1.14ver
            noiseVolumeList.append(self.audioProxy.getFrontMicEnergy())

            time.sleep(0.2)

        # NAOQi2.1はしゃべる前のピコンがうるさいので、リストの最初を削除
        noiseVolumeList.pop(0)

        self.threshold = max(noiseVolumeList) + 20
        print noiseVolumeList
        print "Threshold -> ", self.threshold

    #############################################
    ##
    # 音声入力の録音 (ogg形式)
    ##
    #############################################
    # ユーザが話している間録音するメソッド
    def _record(self):
        # print self.threshold

        # rasta
        self.rasta_id = self.leds.post.rasta(600)

        # 話している部分だけ録音
        d = datetime.datetime.today()
        filename = d.strftime("%Y%m%d_%H%M%S")
        oggname = filename + ".ogg"

        # 録音開始
        self.audioProxy.startMicrophonesRecording(
            "/home/nao/VoiceFile/" + oggname)  # oggで録音すれば1ch
        time.sleep(1)

        # 録音が開始されるまで待機
        # print "STEP 1"
        while True:
            # power = self.memProxy.getData("ALSoundProcessing/frontMicEnergy")  #SDK1.12ver
            # self.audioProxy.enableEnergyComputation()
            power = self.audioProxy.getFrontMicEnergy()
            # print "power", power
            # print "threshold", self.threshold

            if power < self.threshold:
                time.sleep(0.5)
            else:
                print "Step1 -> Finish"
                # time.sleep(0.5)
                break

        # 録音が終了するまで待機
        # print "STEP 2"
        while True:
            # power = self.memProxy.getData("ALSoundProcessing/frontMicEnergy")  #SDK1.12ver
            # self.audioProxy.enableEnergyComputation()
            power = self.audioProxy.getFrontMicEnergy()

            if power < self.threshold:
                print "Step2 -> Finish"
                # time.sleep(0.5)
                break
            else:
                time.sleep(0.5)

        # 録音終了
        self.audioProxy.stopMicrophonesRecording()

        # stop rasta
        self.leds.stop(self.rasta_id)
        print oggname

        return oggname

    #############################################
    ##
    # Googleによる認識
    ##
    #############################################
    def recognizeGoogle(self, android=False):
        print "<< Please Speak >>"

        # 音声を録音
        oggname = self._record()

        # 録音終了後からの処理時間を計測
        start_time = datetime.datetime.now()

        # 音声ファイル(ogg)をローカルにコピー
        self.sftp.get(oggname, os.path.join("./", oggname))

        # 解析
        print 1
        resultList = self._analyzeOggGoogle(oggname)
        end_time = datetime.datetime.now()
        print "Requied Time for Recognition -> " + str((end_time - start_time).seconds + (end_time - start_time).microseconds / 1000000.0) + " sec"

        # failedの場合
        if resultList == ["Failed"]:
            return "Failed"

        # android端末で認識結果を選択させる場合
        if android == True:
            pass

        # android端末を利用しない -> 第一候補を返す
        else:
            return resultList[0]

    def _analyzeOggGoogle(self, oggname):
        # 目を黄色
        # self.leds.fadeRGB("FaceLeds", 256*256*255 + 256*255 + 0 , 0.5)

        # flacに変換
        cmd = "sox " + os.path.join("./", oggname) + \
            " ./input.flac rate 8000 >nul 2>&1"
        subprocess.Popen(cmd, shell=True)

        # flacができるまで待ち
        while True:
            if os.path.exists("./input.flac"):
                break
            else:
                time.sleep(0.5)

        # Google speech API
        flac = open("./input.flac", "rb").read()
        header = {'Content-Type': 'audio/x-flac; rate=8000'}
        req = urllib2.Request(GOOGLEAPI, flac, header)
        data = urllib2.urlopen(req)

        # 認識結果の取得
        recog = data.read().decode("utf8")
        print recog

        # 認識結果のパース
        resultList = list()
        pat = re.compile('"transcript":".+?"')

        for result in pat.findall(recog):
            result = result.replace('"transcript":"', '')
            result = result.replace('"', '')
            # print result
            resultList.append(result)


        # flac削除
        os.remove("./input.flac")

        if len(resultList) == 0:
            return ["Failed"]

        return resultList

    #############################################
    ##
    # 後処理
    ##
    #############################################
    def finish(self):
        #os.system("pskill " + str(self.processID) + ">nul 2>&1")

        # localの音声ファイルを削除
        for filename in os.listdir("./"):
            os.remove(os.path.join("./", filename))

        # Naoの音声ファイルを削除
        for filename in self.sftp.listdir():
            self.sftp.remove(filename)

        self.sftp.close()
        self.conn.close()

        # 目のLEDを白に
        self.leds.fadeRGB("FaceLeds", 256 * 256 * 255 + 256 * 255 + 255, 0.5)

        self.soundProxy.unsubscribe("Recog")  # for ver1.12.11
        print "...::: Japanese Recognition Module Finished :::..."

    """
    #引数のプロセスidを取得 (for AmiVoice)
    def _getPID(self, processName):
        s = subprocess.Popen("tasklist", shell=True, stdout = subprocess.PIPE)
        stdout_value = s.communicate()[0]

        for line in stdout_value.split("\n"):
            if line.startswith(processName):
                return int(pat.findall(line)[0])

    """


########################
##
# Main
##
########################
if __name__ == "__main__":
    rec = Recognition(IP.Nao_Blue)

    try:
        for i in range(1):
            print rec.recognizeGoogle()
            #recResult = rec.recognizeKeybord()
            # print type(recResult)
    except:
        pass

    """
    # Creates a proxy on the speech-recognition module
    asr = ALProxy("ALSpeechRecognition", ROBOT_IP, 9559)
    audioProxy = ALProxy("ALAudioDevice", ROBOT_IP, 9559)
    asr.setLanguage("Japanese")
    """

    rec.finish()
