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
Python program for listing the vms on an ESX / vCenter host
"""

from __future__ import print_function

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

import argparse
import atexit
import getpass
import ssl
import encrypt
import sys
import time




def PrintVmInfo(vm, depth=1):
   """
   Print information for a particular virtual machine or recurse into a folder
   or vApp with depth protection
   """
   maxdepth = 10

   # if this is a group it will have children. if it does, recurse into them
   # and then return
   if hasattr(vm, 'childEntity'):
      if depth > maxdepth:
         return
      vmList = vm.childEntity
      for c in vmList:
         PrintVmInfo(c, depth+1)
      return

   # if this is a vApp, it likely contains child VMs
   # (vApps can nest vApps, but it is hardly a common usecase, so ignore that)
   if isinstance(vm, vim.VirtualApp):
      vmList = vm.vm
      for c in vmList:
         PrintVmInfo(c, depth + 1)
      return
   #We'll check if the VM is in the list.
   if [x for x in vm_cluster if x == vm.name]:
       print("\nPowering off " + vm.name)
       vm.PowerOff()
       time.sleep(10)
       snapshots = vm.snapshot.rootSnapshotList
       for snapshot in snapshots:
           print ("Restoring vm to snapshot:" , snapshot.name)
           snap_obj = snapshot.snapshot
           snap_obj.RevertToSnapshot_Task()
           time.sleep(5)
           print ("Powering on " + vm.name)
           vm.PowerOn()
           #sys.exit(0)
   # summary = vm.summary
   # print("Name       : ", summary.config.name)
   # print("Path       : ", summary.config.vmPathName)
   # print("Guest      : ", summary.config.guestFullName)
   # annotation = summary.config.annotation
   # if annotation != None and annotation != "":
   #    print("Annotation : ", annotation)
   # print("State      : ", summary.runtime.powerState)
   # if summary.guest != None:
   #    ip = summary.guest.ipAddress
   #    if ip != None and ip != "":
   #       print("IP         : ", ip)
   # if summary.runtime.question != None:
   #    print("Question  : ", summary.runtime.question.text)
   # print("")

def main():
   """
   Simple command-line program for listing the virtual machines on a system.
   """
   global vm_cluster

   parser = argparse.ArgumentParser(
       description='Process args for retrieving all the Virtual Machines')

   parser.add_argument('-l', '--login', required=True, action='store',
                   help='login for VCenter access')

   parser.add_argument('-k', '--key', required=True, action='store',
                   help='secured key for authentication')

   parser.add_argument('-vc', '--vcenter', required=True, action='store',
                   help='VCenter host')


   parser.add_argument('-v', '--vm', required=True, action='store',
                   help='Comma delimited list of VMs')
    
   args = parser.parse_args()

   vm_cluster = str(args.vm).split(',')
   
   try:
       password = encrypt.decrypt_login(args.key)

   except Exception as e:
       #print (e)
       print ("\nERROR: Symmetric key and/or password file not found not found.")
       return -1

   context = None
   if hasattr(ssl, '_create_unverified_context'):
      context = ssl._create_unverified_context()
   si = SmartConnect(host=args.vcenter,
                     user=args.login,
                     pwd=password,
                     port=443,
                     sslContext=context)
   if not si:
       print("Could not connect to the specified host using specified "
             "username and password")
       return -1

   atexit.register(Disconnect, si)

   content = si.RetrieveContent()
   for child in content.rootFolder.childEntity:
      if hasattr(child, 'vmFolder'):
         datacenter = child
         vmFolder = datacenter.vmFolder
         vmList = vmFolder.childEntity
         for vm in vmList:
            PrintVmInfo(vm)

   print('\nAll VMs have been refreshed.')
   return 0

# Start program
if __name__ == "__main__":
   main()