#!/usr/bin/python
import os
import statistics
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('-v', '--verbose', action='store_true', 
	help="Verbose output")
args = parser.parse_args()

def getSize(filename):
    st = os.stat(filename)
    return st.st_size

def human_readable_size(size, decimal_places=3):
	if size == 'NaN':
		return 'NaN'
	for unit in ['byte','KiB','MiB','GiB','TiB','PiB','EiB']:
		if size < 1024.0:
			break
		size /= 1024.0
	return f"{size:.{decimal_places}f} {unit}"

def avg(lst):
	try:
		return sum(lst) / len(lst)
	except:
		return 'NaN'



while True:
	if len(args.input) > 1:
		folder = args.input
		print('Folder', folder)
		if os.path.isdir(folder):
			break
		else:
			print('Folder not found, please enter a valid path:')
	else:
		print('Please input a folder to calculate size:')

	folder = input()
	if os.path.isdir(folder):
		break
	else:
		print('Folder not found, please enter a valid path:')
			

file_sizes = []

for root, dirs, files in os.walk(folder, topdown=True):
	for name in files:
		file_absolute = os.path.join(root, name)
		size = getSize(file_absolute)
		file_sizes.append(size)




min_file_size = 41943040
disk_size = 0
sia_size = 0
small_file_list = []
large_file_list = []




for size in file_sizes:
	disk_size += size

	num_chunks = int(size / min_file_size)

	if size % min_file_size != 0:
		num_chunks += 1

	sia_size += num_chunks * min_file_size




print('Size on')
print('    Disk:', human_readable_size(disk_size))
print('    Sia: ', human_readable_size(sia_size))
print()
print('Lost space: ', human_readable_size(sia_size-disk_size))
print('    +' + str(int(sia_size/disk_size*100)-100) + '% empty space used for scaling files up to 40MiB chunks')
if args.verbose:
	print()
	print('Files:', len(file_sizes))
	print('    Average:', human_readable_size(avg(file_sizes)))
	print('    Median:', human_readable_size(statistics.median(file_sizes)))
