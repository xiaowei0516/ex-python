#!/usr/bin/env python
import sys
import sys as system
import time
import os
import re
import subprocess
#import psutil
import socket
import platform
import urllib2

installdir = ''
ccdkdir = ''
SNMP_GET_IPADDR = '192.168.10.188'
#SNMP_GET_IPADDR = '192.168.10.21'
post_url = 'http://192.168.10.22:8888/post_receive.php'

port_string = '192.168.10.10:22,192.168.10.87:80'

OS_INFO = '1.3.6.1.2.1.1.1'
MEM_SIZE = '1.3.6.1.2.1.25.2.2.0'
MEM_FREE = '1.3.6.1.4.1.2021.4.6.0'
SWAP_SIZE = '1.3.6.1.4.1.2021.4.3.0'
SWAP_FREE = '1.3.6.1.4.1.2021.4.4.0'

#DISK_MOUNT_PATH = '1.3.6.1.4.1.2021.9.1.2' "Path where the disk is mounted" dskPath WALK

#SPACE_DISK_PERCENT = '1.3.6.1.4.1.2021.9.1.9' "Percentage of space used on disk" dskPercent WALK

#1.3.6.1.4.1.2021.9.1.10 "Percentage of inodes used on disk" dskPercentNode WALK

#Linux  Windows
def  check_platform():
    plat = platform.system()
    return plat

def check_os():
    osname = platform.dist()  #tuple
    return osname[0] + osname[1]

def  get_install_dir():
    global installdir
    global ccdkdir
    plat = check_platform()
    if 'Windows' in  plat:
        installdir = 'C:\\iprobe\\'
        ccdkdir = 'C:\\ccdk\\'
    if  'Linux'  in  plat:
        installdir = '/opt/iprobe/'
        ccdkdir = '/opt/ccdk/'


def get_time():
    return int(time.time())


def Execute(cmd):
    #Log("cmd=[%s]"%(cmd))
    try:
        proc = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
        return proc.communicate()[0]
    except Exception, e:
        print ("Execute failed, command: %s, error: %s" %(cmd, str(e)))
        return None

def walk_snmp_info(ipaddr, mib):
    cmd = 'snmpwalk -v 2c -c public ' + ipaddr + ' ' + mib
    info = Execute(cmd)
    if '' == info:
        print "connect %s Timeout" %ipaddr
        return None

    if 'Unknown Object' in info or 'No Such' in info  or 'No more variables' in info:
        print "mib Unknown %s" %mib
        return None
    return info
    
    
def get_snmp_info(ipaddr, mib):
    cmd = 'snmpget -v 2c -c public ' + ipaddr + ' ' + mib
    info = Execute(cmd)
    if "Timeout" in info:
        print "connect %s Timeout" %ipaddr
    if "Unknown Object" in info:
        print "mib Unknown" %mib
        return None
    return info
    
def PostData(url, data, timeout=60):
    try:
        time_start = int(time.time())
        request = urllib2.Request(url, data, {'Content-Type': 'application/octet-stream'})
        response = urllib2.urlopen(request,timeout=timeout)
        time_end = int(time.time())
        #print "HTTP post response: ", response.read()
        if response.getcode() != 200:
            print "Post json failed"
        if time_end - time_start > 25: 
            print "timeout on posting"
        return response.getcode() == 200 
    except Exception, e:
        return False


def post(url, post_data):
    PostData(url, post_data)


#********************************* HARDWARE ***********************************

# return arr: capacity (M) 
# [total_mem, free_mem, used_percent,  swap_total, swap_free]
def get_memory(ip=SNMP_GET_IPADDR):
    mem_arr = [] # total,free,percent,swapfree  # K
    total_mem_info = walk_snmp_info(ip,MEM_SIZE)
    if total_mem_info is not None:
        total_mem_k = total_mem_info.split('=')[1].split(':')[1].strip().split()[0].strip()
        total_mem = str(int(total_mem_k)/1024)
    else:
        total_mem = ''
    mem_arr.append(total_mem)

    free_mem_info = walk_snmp_info(ip,MEM_FREE)
    print free_mem_info
    if free_mem_info is not None:
        free_mem_k = free_mem_info.split('=')[1].split(':')[1].strip().split()[0].strip()
        free_mem = str(int(free_mem_k)/1024)    
    else:
        free_mem = ''
    mem_arr.append(free_mem)

    if total_mem is not ''  and free_mem is not '':
        mem_percent = str(round(float(free_mem)/float(total_mem)*100,2))+'%'
        mem_arr.append(mem_percent)
    else:
        mem_arr.append('')
    
    total_swap_info = walk_snmp_info(ip,SWAP_SIZE)
    if total_swap_info is not None:
        total_swap_k = total_swap_info.split('=')[1].split(':')[1].strip().split()[0].strip()
        total_swap = str(int(total_swap_k)/1024)
    else:
        total_swap = ''
    mem_arr.append(total_swap)

    free_swap_info = walk_snmp_info(ip,SWAP_FREE)
    if free_swap_info is not None:
        free_swap_k = free_swap_info.split('=')[1].split(':')[1].strip().split()[0].strip()
        free_swap = str(int(free_swap_k)/1024)
    else:
        free_swap = ''
    mem_arr.append(free_swap)

    return mem_arr
    
    

###get disk
DISK_MOUNT = '1.3.6.1.4.1.2021.9.1.2'
DISK_DEVICE = '1.3.6.1.4.1.2021.9.1.3'
DISK_PERCENT='1.3.6.1.4.1.2021.9.1.9'
DISK_TOTAL_SIZE = '1.3.6.1.4.1.2021.9.1.6'
def win_func_disk_base_info(ip=SNMP_GET_IPADDR, mib=DISK_MOUNT,  arr=[]):
    info_disk_mount = walk_snmp_info(ip, mib)
    if info_disk_mount is not None:
        arr_disk_mount = info_disk_mount.strip().split('\n')
        for ele in arr_disk_mount:
            arr.append(ele.split('=')[1].strip().split()[1].strip())
    return arr

def func_disk_base_info(ip=SNMP_GET_IPADDR, mib=DISK_MOUNT,  arr=[]):
    info_disk_mount = walk_snmp_info(ip, mib)
    if info_disk_mount is not None:
        arr_disk_mount = info_disk_mount.strip().split('\n')
        for ele in arr_disk_mount:
            arr.append(ele.split('=')[1].split(':')[1].strip())
    return arr

def get_disk(ip=SNMP_GET_IPADDR):
    arr_mount=[]
    arr_device=[]
    arr_total_size=[]
    arr_used_percent=[]
    arr_mount = func_disk_base_info(ip, DISK_MOUNT, arr_mount)
    arr_device = func_disk_base_info(ip, DISK_DEVICE, arr_device)
    arr_total_size = func_disk_base_info(ip, DISK_TOTAL_SIZE, arr_total_size)
    arr_used_percent  = func_disk_base_info(ip, DISK_PERCENT, arr_used_percent)
    return arr_mount,arr_device,arr_total_size,arr_used_percent

WIN_DISK_INDEX = '1.3.6.1.2.1.25.2.3.1.1'
WIN_DISK_MOUNT = '1.3.6.1.2.1.25.2.3.1.3'
WIN_DISK_UNIT = '1.3.6.1.2.1.25.2.3.1.4'
WIN_DISK_MANY_UNIT = '1.3.6.1.2.1.25.2.3.1.5'
WIN_DISK_USED_UNIT = '1.3.6.1.2.1.25.2.3.1.6'
def win_get_disk(ip=SNMP_GET_IPADDR):
    disk_inflags=[]
    arr_mount=[]
    arr_disk_unit=[]
    arr_disk_many_unit=[]
    arr_disk_used_unit=[]
    arr_total_size=[]
    arr_used_percent=[]
    arr_device=[]

    win_arr_mount = []
    win_arr_unit = []
    win_arr_many_unit = []
    win_arr_used_unit = []
    win_arr_index = []
    win_arr_index = win_func_disk_base_info(ip, WIN_DISK_INDEX, win_arr_index)
    win_arr_mount = win_func_disk_base_info(ip, WIN_DISK_MOUNT, win_arr_mount)
    for index in range(len(win_arr_index)):
        if r":\\" in win_arr_mount[index]:
            disk_inflags.append(index)
            arr_mount.append(win_arr_mount[index])
    for line in arr_mount:
        print line

    win_arr_unit = func_disk_base_info(ip, WIN_DISK_UNIT, win_arr_unit)
    for ind in disk_inflags:
        arr_disk_unit.append(win_arr_unit[int(ind)].split()[0])
    for line in arr_disk_unit:
        print line

    win_arr_many_unit = func_disk_base_info(ip, WIN_DISK_MANY_UNIT, win_arr_many_unit)
    for ind in disk_inflags:
        arr_disk_many_unit.append(win_arr_many_unit[int(ind)])
    for line in arr_disk_many_unit:
        print line

    win_arr_used_unit = func_disk_base_info(ip, WIN_DISK_USED_UNIT, win_arr_used_unit)
    for ind in disk_inflags:
        arr_disk_used_unit.append(win_arr_used_unit[int(ind)])
    for line in arr_disk_used_unit:
        print line


    for ind in disk_inflags:
        arr_total_size.append(str(int(arr_disk_unit[ind]) * int(arr_disk_many_unit[ind]) / 1024 / 1024))
    for line in arr_total_size:
        print line

    for ind in disk_inflags:
        if int(arr_disk_many_unit[ind]) != 0:
            arr_used_percent.append(str(int(arr_disk_used_unit[ind]) / int(arr_disk_many_unit[ind])*100))
    else:
        arr_used_percent.append('0')


    for ind in disk_inflags:
        arr_device.append('')
    return arr_mount,arr_device,arr_total_size,arr_used_percent

    



USER_CPU_PERCENT =  '1.3.6.1.4.1.2021.11.9.0'
SYS_CPU_PERCENT = '1.3.6.1.4.1.2021.11.10.0'
CPU_LOAD = '1.3.6.1.2.1.25.3.3.1.2'
CPU_DESC = '1.3.6.1.2.1.25.3.2.1.3'
def cpu_cores():
    cpu_load_info = walk_snmp_info(SNMP_GET_IPADDR, CPU_LOAD)
    if cpu_load_info is not None:
        cpu_cores = str(len(cpu_load_info.strip().split('\n')))
    else:
        cpu_cores = '0'
    return cpu_cores

def get_cpu_desc():
    cpu_desc_info = walk_snmp_info(SNMP_GET_IPADDR, CPU_DESC)
    print "cpu %s" % cpu_desc_info
    if cpu_desc_info is not None:
        cpu_desc = cpu_desc_info.split('\n')[0].split('=')[1].split(':')[2]
    else:
        cpu_desc = ""
    return cpu_desc

def func_cpu_info(ip=SNMP_GET_IPADDR, mib=USER_CPU_PERCENT):
    user_cpu_info = walk_snmp_info(ip, mib)
    if user_cpu_info is not None:
        user_cpu_percent  = user_cpu_info.split('=')[1].split(':')[1].strip() + '%'
    else:
        user_cpu_percent = ''
    return user_cpu_percent

#return array:
#cpu_arr [user_cpu_percent, ]
def get_cpu(ip=SNMP_GET_IPADDR):
    cpu_arr=[]
    user_cpu_percent = func_cpu_info(ip, USER_CPU_PERCENT)
    cpu_arr.append(user_cpu_percent)
    sys_cpu_percent = func_cpu_info(ip, SYS_CPU_PERCENT)
    cpu_arr.append(sys_cpu_percent)
    cpu_desc = get_cpu_desc()
    if cpu_desc is not '':
        cpu_base = cpu_desc + " with " + cpu_cores() + " cores"
        cpu_arr.append(cpu_base)
    else:
        cpu_arr.append('')
    return cpu_arr


   
#******************************************SYSTEM***********************************************
NIC_DESC = '1.3.6.1.2.1.2.2.1.2'
OUT_BKTS = '1.3.6.1.2.1.2.2.1.16'
OUT_PKTS = '1.3.6.1.2.1.2.2.1.17'
IN_BKTS = '1.3.6.1.2.1.2.2.1.10'
IN_PKTS = '1.3.6.1.2.1.2.2.1.11'

def get_ip_address(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR   
            struct.pack('256s', ifname[:15])
            )[20:24])
    except IOError,e:
        pass

def get_nic_to_ip():
#    nic_arr=[]
    ipaddr_arr=[]
    nic_info = walk_snmp_info(SNMP_GET_IPADDR, NIC_DESC)
    if nic_info is not None:
        all_nic = nic_info.strip().split('\n')
        for line in all_nic:
            one_nic = line.split('=')[1].split(':')[1].strip()
#            if one_nic == 'lo':
#                continue
#       nic_arr.append(one_nic)
            one_ip = get_ip_address(one_nic)
            ipaddr_arr.append(one_ip)
    return ipaddr_arr

def get_packet_info(mib=IN_BKTS, arr=[]):
    pack_info = walk_snmp_info(SNMP_GET_IPADDR, mib)
    if pack_info is not None:
        pack_list = pack_info.strip().split('\n')
        for line in pack_list:
            number = line.split('=')[1].split(':')[1].strip()
            arr.append(number)
    return arr

def get_in_out_flows():
    bkts_in_arr = []
    bkts_out_arr = []
    pkts_in_arr = []
    pkts_out_arr = []
    bkts_in_arr = get_packet_info(IN_BKTS, bkts_in_arr)
    bkts_out_arr = get_packet_info(OUT_BKTS, bkts_out_arr)
    pkts_in_arr = get_packet_info(IN_PKTS, pkts_in_arr)
    pkts_out_arr = get_packet_info(OUT_PKTS, pkts_out_arr)
    return bkts_in_arr,bkts_out_arr,pkts_in_arr,pkts_out_arr

def  get_os_release():
    osname = platform.dist()  #tuple
    return osname[0] + osname[1]

def get_kernel_release(ip=SNMP_GET_IPADDR, mib=OS_INFO):
    return platform.release()


def check_port(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception:
        return "False"
    s.settimeout(10)
    try:
        s.connect((host, port))
    except Exception,e:
        print e
        s.close()
        return "False"
    s.close()
    return "Ok"


#************************************SOFTWARE*********************************
def get_iprobe_version():
    fiprobe = installdir + 'VERSION'
    #print fiprobe
    with open(fiprobe, 'r') as f:
        for line in f.readlines():
            if 'Revision' in line:
                return line.strip().split(':')[1].strip()

def get_ccdk_version():
    fccdk = ccdkdir + 'VERSION'
    with open(fccdk, 'r') as f:
        for line in f.readlines():
            if 'Revision' in line:
                return line.strip().split(':')[1].strip()


#return list
def get_saas_conf():
    fconf = installdir + 'kafka.conf'
    with open(fconf, 'r') as f:
        return f.readlines()

def get_monit_status():
    proc = subprocess.Popen(monit_comm, shell=True, stdout=subprocess.PIPE)
    #print proc.communicate()
    return proc.communicate()[0]

if __name__ == '__main__':
    arr_mem = get_memory()
    for line in arr_mem:
        print line
    #arr_cpu = get_cpu()
    #for line in arr_cpu:
    #    print line

    arr_mount,arr_device,arr_total_size,arr_used_percent = win_get_disk()

	    
