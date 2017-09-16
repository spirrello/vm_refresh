This script will restore VMs to a previous snapshot.  Currently it has only been tested with VMs with a single snapshot.

Usage:

python vm_refresh.py -l USERNAME -vc VCENTER -k KEY -v vm1,vm2,vm3

Requirements
- symmetric key
- pyvmomi python module
