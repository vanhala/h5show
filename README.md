# Synopsis

This is a simple python utility for inspecting hdf5 files on the
command line. I wrote it to replace h5ls and h5dump in my use case,
which is to simply quickly check what groups and datasets are
contained in the file, and to print selected elements of those
datasets.

# Syntax

## List the root of the file:

h5show.py file.h5

## List contents of a subgroup:

h5show.py /path/to/file.h5//group1/group2

Note the double slash separator between the file name and the group
names. This is to separate the filesystem paths from the paths within
the hdf5 file.

## Print information about a dataset:

h5show.py file.h5//group/dataset

## Print elements from a dataset:

The datasets can be indexed within square brackets much like numpy
arrays. One can also use semicolons for slicing.

h5show.py file.h5//group/dataset[0,:,1:3]

Using just [ or [] will print the full dataset in the way numpy arrays
are printed, i.e. abbreviating with ellipses if the dataset is very
large.

h5show.py file.h5//group/dataset[
