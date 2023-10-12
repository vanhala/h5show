import h5py
import sys
import os
import numpy

def parsepath(path):

    scount=path.count('//')
    
    if path.count('//')>1:
        print('Error: the separator // cannot appear more than once in the path')
        sys.exit(1)
    
    filepath,separator,dsetpath=path.partition('//')
    
    return filepath,dsetpath

def printusage():
    
    print('Usage: h5show /path/to/file.h5//group1/group2/dsetname')

def listgroup(group):

    for key in group.keys():
        print(key)

def show(filepath,itempath):
    
    if not os.path.isfile(filepath):
        print('No such file: '+filepath)
        return False
    
    try:
        with h5py.File(filepath,'r') as f:
            
            if itempath!='' and (not itempath in f):
                print('No such group or dataset: '+itempath)
                return False
            
            if itempath=='':
                #the root group
                item=f
            else:
                item=f[itempath]
            
            if isinstance(item,h5py.Dataset):
                if item.size>1000:
                    print(item)
                else:
                    data=numpy.array(item)
                    print(data)
            else:
                listgroup(item)
                
    except FileNotFoundError as err:
        print('Failed opening the file '+filepath)
        print(err)
        

def main():
    
    if len(sys.argv)!=2:
        printusage()
        sys.exit()
    
    filepath,itempath=parsepath(sys.argv[1])

    show(filepath,itempath)

if __name__=='__main__':
    main()
