#!/usr/bin/env python3
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

def printcolumns(rows):
    
    maxwidth=max(len(word) for row in rows for word in row)+2
    
    for row in rows:
        for word in row:
            print(word.ljust(maxwidth),end='')
        print('')

def item_info(item):
    
    name=item.name.split('/')[-1]
    if isinstance(item,h5py.Group):
        kind='group'
    elif isinstance(item,h5py.Dataset):
        kind='dataset'
    else:
        kind='other'

    if kind=='group' or kind=='other':
        return name,kind

    dtypestr=item.dtype.name
    shapestr=str(item.shape)
    
    return name,kind,shapestr,dtypestr

def listgroup(group):
    
    infos=[]
    for key in group.keys():
        infos.append(list(item_info(group[key])))
    
    printcolumns(infos)

def print_item_info(item):
    
    printcolumns([list(item_info(item))])

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
                print_item_info(item)
                if item.size<=1000:
                    data=numpy.array(item)
                    print('\nData:')
                    print(data)
                else:
                    print('(Will not print data as the dataset has more than 1000 elements)')
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
