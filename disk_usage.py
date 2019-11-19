import sys
import subprocess
import json
import os

try:
   inventory=sys.argv[1]
   operating_system=sys.argv[2]

   if operating_system == "linux":
      directory='facter_linux'
      disk_prefix='sd'
      filesystem_format='ext4'
   if operating_system == "aix":
      directory='facter_aix'
      disk_prefix='hd'
      filesystem_format='jfs2'

   subprocess.check_output('/usr/bin/ansible -b -m setup -a "filter=facter_*" -i '+inventory+' all -t '+directory, shell=True)
   jsons = os.listdir(directory)
   sum=0
   for i in jsons:
      with open(directory+"/"+i) as json_file:
          facter_disks=json.load(json_file)
          for p in facter_disks['ansible_facts']['facter_disks']:
             if disk_prefix in p:
                sum=(facter_disks['ansible_facts']['facter_disks'][p]['size_bytes'])+sum
   print "Total aprovisionado: "
   print sum/1000000000

   sum=0
   for i in jsons:
      with open(directory+"/"+i) as json_file:
          facter_disks=json.load(json_file)
          for x in facter_disks['ansible_facts']['facter_mountpoints']:
             if facter_disks['ansible_facts']['facter_mountpoints'][x]['filesystem'] in filesystem_format:
               sum=(facter_disks['ansible_facts']['facter_mountpoints'][x]['used_bytes'])+sum
   print "Total usado: "
   print sum/1000000000

except:
   print "Uso: "+sys.argv[0]+" inventario tipo de sistema operativo"
