#!/usr/bin/python

import subprocess
import platform

installdir = '/opt/iprobe/'
ccdkdir = '/opt/ccdk/'

#Linux  Windows
def  check_platform():
    plat = platform.system()
    return plat

def  get_install_dir():
    plat = check_platform()
    if 'Windows' in  plat:
        installdir = 'C:\\iprobe\\'
        ccdkdir = 'C:\\ccdk\\'
    if  'Linux'  in  plat:
        installdir = '/opt/iprobe/'
        ccdkdir = '/opt/ccdk/'

###############################   software  interralte  ###########################################

def get_iprobe_version():
    fiprobe = installdir + 'VERSION'
    print fiprobe
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
    monit_comm = installdir + 'monit -c ' + installdir + 'monitrc status'
    proc = subprocess.Popen(monit_comm, shell=True, stdout=subprocess.PIPE)
    #p = proc.stdout.readlines()
    #print p[0]
    return proc.communicate()[0]

if __name__ == '__main__':
    post_ip=""
    post_port=""
    guid=""
    peerhost=""
    monit_ip=""
    broker_list=""
    get_install_dir()
    print installdir
    print ccdkdir
    iprobe_version = get_iprobe_version()
    print iprobe_version #str
    ccdk_version = get_ccdk_version()
    print ccdk_version  #str

    arr_conf = get_saas_conf()
    for line in arr_conf:
        if 'post_server_ip' in line:
            post_ip = line.split('=')[1].strip()
        if 'post_server_port' in line:
            post_port = line.split('=')[1].strip()
        if 'guid' in line:
            guid = line.split('=')[1].strip()
        if 'peerhost' in line:
            peerhost = line.split('=')[1].strip()
        if 'metadata.broker.list' in line:
            broker_list = line.split('=')[1].strip()
        if 'monit_ip' in line:
            monit_ip = line.split('=')[1].strip()
    print post_ip    
    print post_port
    print guid
    print peerhost
    print broker_list
    print monit_ip
    mt = get_monit_status()
    print type(mt)

