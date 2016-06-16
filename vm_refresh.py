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
Python program refreshing the Calico nodes to a previous snapshot.
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

def refresh_playground(machine_list):
   """This method will refresh the VMs in the office."""
   print (machine_list)
   context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
   context.verify_mode = ssl.CERT_NONE
   si = SmartConnect(host='playvcenter6.liaison.tech',
                     user='root',
                     pwd=grab_info(),
                     port=443,
                     sslContext=context)
   if not si:
       print("Could not connect to the specified host using specified "
             "username and password")
       return -1

   atexit.register(Disconnect, si)

   content = si.RetrieveContent()
   for child in content.rootFolder.childEntity:
      if hasattr(child,'hostFolder'):

         datacenter = child
         vmFolder = datacenter.vmFolder
         vmList = vmFolder.childEntity
         #print (hostList)


         for vm in vmList:
             #hostList_name.append(host.name)
             if vm.name in machine_list:
                 print ("Powering off:" , vm.name)
                 vm.PowerOff()
                 time.sleep(5)

                 #Revert the snapshot.....
                 snapshots = vm.snapshot.rootSnapshotList
                 for snapshot in snapshots:
                     print ("Reverting back to " , snapshot.name)
                     snap_obj = snapshot.snapshot
                     snap_obj.RevertToSnapshot_Task()
                     time.sleep(10)
                     print ("Powering on:" , vm.name)
                     vm.PowerOn()

   print("\nAll nodes have been reverted to a previous snapshot.\n")


def refresh_home():
   """This method will refresh the VMs at home."""

def main():
   """
   This preps the Calico vms for testing.  Powers them off, reverts snapshots and powers them back on.
   """

   # args = GetArgs()
   # if args.password:
   #    password = args.password
   # else:
   #    password = getpass.getpass(prompt='Enter password for host %s and '
   #                                      'user %s: ' % (args.host,args.user))

   if len(sys.argv) != 3:
      print ("Incorrect number of parameters, please enter home or office as an option.  The VMs must be comma delimited.")
      sys.exit(1)

   machine_list = sys.argv[2].replace(" ", "").split(',')
   if sys.argv[1] == "office":
      print ("Refreshing office nodes...")
      refresh_playground(machine_list)
   elif sys.argv[1] == "home":
      print ("Refreshing home nodes...")
      refresh_home()
   else:
      print ("please enter office or home as a parameter")



   return 0

# Start program
if __name__ == "__main__":
   main()
