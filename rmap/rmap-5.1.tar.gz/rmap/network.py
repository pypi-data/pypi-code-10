#!/usr/bin/python

# Copyright (c) 2014 Paolo Patruno <p.patruno@iperbole.bologna.it>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# 3. Neither the name of mosquitto nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import subprocess

class wifi():

   def  __init__(self):
      self.stdout=""
      self.stderr=""

   def create(self,ssid=None,password=None):

      proc=subprocess.Popen(('nmcli','device','wifi','connect', ssid ,'password', password),stdout=subprocess.PIPE,stderr=subprocess.PIPE)

      self.stdout,self.stderr=proc.communicate()

      status=proc.wait()
      if status != 0:
         print "There were some errors setting wifi: ",status,self.stderr

      return status

def main():
   net=wifi()
   stato=net.create(ssid="pat",password="test")
   print "stato:",stato
   print "stdout=",net.stdout
   print "stderr=",net.stderr

if __name__ == '__main__':
   main()  # (this code was run as script)
