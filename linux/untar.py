#!/usr/bin/python
import tarfile
def extractTar(tarname):
	if not tarfile.is_tarfile(tarname):
		return False
	tar = tarfile.open(tarname)
	tar.extractall()
	tar.close()
	return True

if __name__ == '__main__':
    tarname = "/home/nfs/xiaowei/github/ex-python/linux/aa.tar.gz"
    extractTar(tarname)
