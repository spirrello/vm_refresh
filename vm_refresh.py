#!/usr/bin/env python
# VMware vSphere Python SDK
# Copyright (c) 2008-2015 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Python program refreshing VMs to a previous snapshot.
"""

from __future__ import print_function

from pyVim.connect import SmartConnect, Disconnect

import argparse
import atexit
import getpass
import ssl
import base64
import time
import json
import sys
import getpass
import encrypt


#filedir = '/home/spirrello/scripts/Rundeck-Network-Jobs/vcenter/'


def grab_info():
    with open('.kah') as json_data_file:
        data = json.load(json_data_file)
        data = data['roller']
        data=base64.b64decode(data)
    return data


def GetArgs():
   """
   Supports the command-line arguments listed below.
   """
   parser = argparse.ArgumentParser(
       description='Process args for retrieving all the Virtual Machines')
   parser.add_argument('-s', '--host', required=True, action='store',
                       help='Remote host to connect to')
   parser.add_argument('-o', '--port', type=int, default=443, action='store',
                       help='Port to connect on')
   parser.add_argument('-u', '--user', required=True, action='store',
                       help='User name to use when connecting to host')
   parser.add_argument('-p', '--password', required=False, action='store',
                       help='Password to use when connecting to host')
   args = parser.parse_args()
   return args

def refresh_vms(machine_list, environment):
   """This method will refresh the VMs in the office."""

   print ("VMs to be refreshed in the " + environment + " environment:")
   for machine in machine_list:
       print (machine)
   context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
   context.verify_mode = ssl.CERT_NONE
   if environment == "dev":
       user = "LIAISONTECH\svc_rdeckvm_tech"
       host = "at4m-lvvc01.liaison.tech"
       try:# open('office-playground.key', 'r') and open('office-playground.pem', 'r'):     
           password = encrypt.decrypt_login('tech-vmware.key')
       except Exception as e:
           #print (e)
           print ("\nERROR: Symmetric key and/or password file not found not found.  Please generate one and name it office-playground.key")
           return -1
   elif environment == "office":
       user = getpass.getuser()
       host = "10.10.16.105"
       try:# open('office-playground.key', 'r') and open('office-playground.pem', 'r'):     
           password = encrypt.decrypt_login('office-playground.key')
       except Exception as e:
           #print (e)
           print ("\nERROR: Symmetric key and/or password file not found not found.  Please generate one and name it office-playground.key")
           return -1
   else:
       print ("please enter a valid parameter for the environment...")
   

   print("\nAll nodes have been reverted to a previous snapshot.\n")



def main():
   """
   Powers them off, reverts snapshots and powers them back on.
   """
   if len(sys.argv) != 3:
      print ("Incorrect number of parameters, please enter home or office as an option.  The VMs must be comma delimited.")
      sys.exit(1)

   machine_list = sys.argv[2].replace(" ", "").split(',')
   if sys.argv[1] == "office" or sys.argv[1] == "dev":
      environment = sys.argv[1]
      
      refresh_vms(machine_list, environment)
   # elif sys.argv[1] == "home":
   #    print ("Refreshing home nodes...")
   #    refresh_vms()
   else:
      print ("please enter a valid environment as a parameter...")



   return 0

# Start program
if __name__ == "__main__":
   main()
