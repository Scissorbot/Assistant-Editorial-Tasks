import sys, os, re, shutil
import setup as setup
from Include import _willett as w


# WHICH CAMERA WOULD YOU LIKE TO MAKE A TEST STRUCTURE FOR?
# 1: Halo
your_answer = 1


root_dir = setup.dir_in
formats_available = {1: 'Halo'}
number_of_cameras = 7

for camera in range(number_of_cameras):
    if formats_available[your_answer] == 'Halo':
        # N = Normal, T = Timelapse
        # Numbers indicate number of Spans
        shots = ['N1', 'N1', 'T5', 'T1', 'N3']
        camera = camera + 1
        number_of_lenses = 17
        lens_switch = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9,
                       10:'A', 11:'B', 12:'C', 13:'D', 14:'E', 15:'F', 16:'G', 17:'H'}

        dest_root = os.path.join(root_dir, 'Willett%s' % camera)
        if os.path.isdir(dest_root):
            print('\nRemoving existing directory: %s' % dest_root)
            shutil.rmtree(dest_root, ignore_errors=True)

        for i in range(len(shots)):
            for lens in range(number_of_lenses):
                dest_dir = os.path.join(dest_root, 'Card%s' % (lens + 1), 'DCIM', '100MEDIA')
                for n in range(int(shots[i][-1])):
                    filename = '%s%s%s%s%s' % (shots[i][0], lens_switch[lens+1], w.format_length(n, 2, 0), w.format_length(i + 1, 4, 0), '.mp4')
                    full_path = os.path.join(dest_dir, filename)
                    if not os.path.isdir(dest_dir):
                        os.makedirs(dest_dir)
                    file = open(full_path, 'w')
                    print('.', end='')
