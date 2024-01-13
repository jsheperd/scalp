#!/usr/bin/env python3

import argparse, os, re, string, subprocess, sys

def FileBytes(files):
        return [(fname, os.path.getsize(fname)) for fname in files ]

def Scalp(fname, slicesize='4k'):
        ret = subprocess.run(['fallocate', '-c', '-o', '0', '-l', slicesize,  fname])

def Numerize(human):
        """ convert human readable size to bytes """
        # based on https://stackoverflow.com/a/42865957/2002471
        size = human.upper()
        units = {"B": 1, "K": 2**10, "M": 2**20, "G": 2**30, "T": 2**40}
        if not re.match(r' ', size):
                size = re.sub(r'([KMGT])', r' \1', size)
        number, unit = [string.strip() for string in size.split()]
        return int(float(number)*units[unit])

if __name__ == "__main__":
        description='Cut the head of a file without rewriting it on the supported filesystems (currently xfs and ext4).'
        epilog='usage:  scalp.py 1g 4g 4k file1 file2 file.... '

        parser = argparse.ArgumentParser(description=description, epilog=epilog)
        parser.add_argument('fsmin', help='minimal size of the scalped file. The scalped slice size can be only multiply of the blocksize of the filesystem.')
        parser.add_argument('fsmax', help='make the scalp only if the file is bigger than this size.')
        parser.add_argument('blocksize', help='blocksize of the filesystem')
        parser.add_argument('files', nargs='+', help='files to scalp')
        args = parser.parse_args()
        bytesmin = Numerize(args.fsmin)
        bytesmax = Numerize(args.fsmax)
        bytesblocksize = Numerize(args.blocksize)

        for fname, bytesact in FileBytes(args.files):
                print('processing ', fname, bytesact)
                if bytesact > bytesmax:
                        print(fname, 'needs scalp')
                        cut = bytesact - bytesmin
                        if cut > bytesblocksize:
                                cut -= cut%bytesblocksize # cut%bytesblocksize = 0
                                Scalp(fname, str(cut))
