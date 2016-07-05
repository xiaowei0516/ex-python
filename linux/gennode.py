#!/usr/bin/python
import os
import subprocess

def get_cfg():
	path_prefix=os.getenv('IPROBE_DATA')
	fullpath=path_prefix+'/etc/pprobe.cfg'
	return fullpath

def get_nic_list():
	fullpath = get_cfg()
	with open(fullpath, 'r') as f:
		txts = f.readlines()
		for line in txts:
			if "bus_list" in line:
			    arrlist = line.strip().split()
			    if len(arrlist) == 0:
			        print "bus list not config!"
			        os.exit()
			    listone = arrlist[1].split(',')[0].strip('[').strip('"')
                return listone

def Execute(cmd,close_fds=True):
    try:
        proc = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
        return proc.communicate()[0]
    except Exception, e:
        print "Execute failed, command: %s, error: %s" %(cmd, str(e))
        return None

def get_nic_distance(buslist=''):
    comm='cat  /sys/bus/pci/devices/' + buslist + '/numa_node'
    return Execute(comm)

def get_node_num():
	comm='lscpu | grep -E "NUMA\snode\(s\)" | awk -F":" \'{print $2}\' | xargs'
	return Execute(comm).strip()

def get_all_cores():
	comm = 'numactl --hardware | grep -E "cpus" | awk -F ":" \'{print $2}\' | xargs'
	outstr = Execute(comm).strip()
	return outstr

if __name__ == '__main__':
    buslist0 = get_nic_list() # 0000:83:00.0
    distance = get_nic_distance(buslist0) #distance
    print distance
    node_nums = get_node_num()   #numa_num
    allcores = get_all_cores()
    arr_cores = allcores.split()

    core_nums = len(arr_cores)
    per_node_core = core_nums/int(node_nums)
    print per_node_core
   
    arr_numa_cores=[]
    arr_numa_key=[]
    for i in range(int(node_nums)):
        start = i*per_node_core
        arr_numa_key.append('\"numa'+str(i)+'\"')
        arr_numa_cores.append(arr_cores[start:per_node_core*(i+1)])

    arr_str=[]
    for i in range(len(arr_numa_key)):
        print i
        arr_str.append(arr_numa_key[i] + ':['  + ','.join(arr_numa_cores[i]) + ']')
    node_string=',\n'.join(arr_str)
    print node_string
    data='{\n "distance":'+ distance +',\n"per_node_core":' + str(per_node_core) +',\n "nodename": ['+ ','.join(arr_numa_key) + '],\n' + node_string  + '\n}'
    with open("node.cfg", 'w') as f:
        f.write(data)
    print data
