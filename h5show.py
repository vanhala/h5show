#!/usr/bin/env python3
import h5py
import sys
import os
import numpy
import glob

def parsepath(path):

    scount=path.count('//')
    
    if path.count('//')>1:
        print('Error: the separator // cannot appear more than once in the path')
        sys.exit(1)
    
    filepath,separator,dsetpath=path.partition('//')
    
    return filepath,dsetpath

def printusage():

    print('Usage: h5show /path/to/file.h5//group1/group2/dsetname [more paths...]')

def printcolumns(rows):
    
    maxcols=max(len(row) for row in rows)
    
    #the justified width of each column
    maxwidths=[]
    for colind in range(maxcols):    
        maxwidths.append(max(len(row[colind]) if len(row)>colind else 0 for row in rows)+4)
    
    for row in rows:
        for colind in range(len(row)):
            print(row[colind].ljust(maxwidths[colind]),end='')
        print('')

def item_info(item):
    
    name=item.name.split('/')[-1]
    if isinstance(item,h5py.Group):
        kind='group'
    elif isinstance(item,h5py.Dataset):
        kind='dataset'
    else:
        kind='other'
    
    if kind=='group' or kind=='dataset':
        attrnames=list(item.attrs.keys())
        if len(attrnames)!=0:
            attrstr='('
            for i in range(len(attrnames)):
                attrstr+=attrnames[i]+'='+str(item.attrs[attrnames[i]])
                if i!=len(attrnames)-1:
                    attrstr+=', '
            attrstr+=')'
        else:
            attrstr=None
    
    if kind=='group' or kind=='other':
        if attrstr is not None:
            return name,kind,attrstr
        else:
            return name,kind
    
    dtypestr=item.dtype.name
    shapestr=str(item.shape)

    if attrstr is not None:
        return name,kind,shapestr,dtypestr,attrstr
    else:
        return name,kind,shapestr,dtypestr

def listgroup(group):
    
    infos=[]
    for key in group.keys():
        infos.append(list(item_info(group[key])))
    
    printcolumns(infos)

def print_item_info(item):
    
    printcolumns([list(item_info(item))])

def show(filepath,itempath):

    #check the common typo-type mistakes to give a nice error message
    if not os.path.isfile(filepath):
        print('No such file: '+filepath)
        return False
    
    if not h5py.is_hdf5(filepath):
        print('Not an hdf5 file: '+filepath)
        return False
    
    try:
        with h5py.File(filepath,'r') as f:
            
            if itempath!='' and (not itempath in f):
                print('No such item: '+filepath+'//'+itempath)
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
                    print('Data:')
                    print(data)
                else:
                    print('(Will not print data as the dataset has more than 1000 elements)')
            else:
                listgroup(item)
                
    except FileNotFoundError as err:
        print('Failed opening the file '+filepath)
        print(err)

def make_file_paths(filepath):
    
    filenames=glob.glob(filepath)
    
    if len(filenames)==0:
        print('No such file: '+filepath)
    
    return filenames

def main():
    
    if len(sys.argv)<2:
        printusage()
        sys.exit()
    
    paths=sys.argv[1:]
    
    for path in paths:
        filepattern,itempath=parsepath(path)
        filepaths=make_file_paths(filepattern)
        
        for filepath in filepaths:
            if len(paths)>1 or len(filepaths)>1:
                print(filepath)
            show(filepath,itempath)
            if len(paths)>1 or len(filepaths)>1:
                print()

if __name__=='__main__':
    main()
