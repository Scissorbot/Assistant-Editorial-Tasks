import sys, os, re, shutil
import setup as setup
from Include import _willett as w
import tkinter






TESTING_MODE = False






process_title = "Move Card Media"
w.start(process_title)

if True:
    dir_in = setup.dir_in
    dir_out = dir_in
    trash = os.path.join(dir_in, '_trash')
    w.printWrite("Folder in:\t%s" % dir_in)
    w.printWrite("Folder out:\t%s\n\n" % dir_out)

    files_out = []
    all_cameras = []
    accepted_ext = ['.mp4', '.mov', '.jpg', '.thm', '.png']

    if TESTING_MODE:
        w.print_section_head('Running in testing mode')

class media_file:

    def __init__(self, path):
        # The following object attributes are instantiated here so you can see the data we'll want filled
        self.model = ''         # This is an automatically-detected value based on filename conventions
        self.camera = ''        # This is the unique designation for an individual rig
        self.lens_ID = ''       # This is the label of an individual eye of the camera rig
        self.part = ''          # This value increments when shots are spanned
        self.shot = ''          # This value increments when the camera starts and stops
        self.ext = ''           # This is the extension of the file (mp4, mov, jpg, png, thm)
        self.card = ''          # This is the name of the folder that contains "DCIM"
        self.special = ''       # This allows tags to append the final filename, like "_timelapse"
        self.partstring = ''    # This is the placeholder for the filename component when spans exist
        self.filename_out = ''
        self.dest = ''

        # This function actually assigns the values for the attributes
        self.data_from_filename(path)

    def data_from_filename(self, path):

        # Regex resource of choice: https://rubular.com/
        if re.search(r'[NTP][\dA-H]\d{6}(.MP4|.mp4|.jpg|.thm)', path) is not None:
            # [NTP] -- Begins with N, T, or P
            # [\dA-H] -- Next character is a digit OR the letters A-H (all capital)
            # \d{6} -- Followed by exactly six digits
            # (.MP4|.mp4|.jpg|.thm) -- Accepted extensions

            self.model = 'Halo'
            self.cam_model_halo(path)

        if re.search(r'(HS)\d+_[LR]T_\d+_\d+(.mov|.MOV)', path) is not None:
            # (HS) -- Begins with exactly 'HS'
            # \d{#} -- has # number of consecutive digits

            self.model = 'Hyperstereo'
            self.cam_model_hyperstereo(path)


    # Each camera model should be tested for above,
    # but the object attributes will be assigned in
    # a dedicated subfunction
    def cam_model_halo(self, filepath):
        filename = os.path.basename(filepath)
        self.lens_ID = filename[1].upper()
        self.part = int(filename[2:4])      #making this an int will truncate leading zeroes
        self.shot = int(filename[4:8])      #making this an int will truncate leading zeroes
        shot_string = str(filename[4:8])    #this preserves leading zeroes for span-checking
        self.ext = filename.split('.')[-1].lower()

        media_directory = os.path.dirname(filepath)
        dcim = os.path.dirname(media_directory)
        self.card = os.path.basename(os.path.dirname(dcim))

        self.video_type = filename[0].upper()
        if self.video_type == 'N':
            self.special = ''
        elif self.video_type == 'T':
            self.special = '_timelapse'
        elif self.video_type == 'P':
            self.special = '_image'
            self.part = None
            self.shot = int(filepath[2:8])  # Images have six digits available for shot number

        if self.part != 0:
            self.partstring = '_pt%s' % (self.part + 1)
        elif '%s%s01%s.%s' % (self.video_type, self.lens_ID, shot_string, self.ext) in os.listdir(media_directory) \
                and self.video_type is not 'P':
            self.partstring = '_pt1'

        # This dictionary allows for letter camera IDs to be converted to integers
        if not self.lens_ID.isdigit():
            lens_ID_switch = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17}
            self.lens_ID = lens_ID_switch[self.lens_ID]

        camera_count = len(list(filter(lambda x: (x == 'Halo'), all_cameras))) + 1
        self.camera = os.path.basename(os.path.dirname(os.path.dirname(dcim)))
        self.lens_ID = w.format_length(self.lens_ID, 2, 0)

        self.filename_out = "%s_shot%s%s_lens%s%s.%s" % (self.camera, self.shot, self.partstring,
                                                         self.lens_ID, self.special, self.ext)
        self.dest = os.path.join(dir_out, 'Takes', '%s_Shot%s' % (self.camera, self.shot), self.filename_out)

    def cam_model_hyperstereo(self, filepath):
        filename = os.path.basename(filepath)
        file_split = filename.split('_')
        self.lens_ID = file_split[1]
        self.part = file_split[-1].split('.')[0]
        self.shot = file_split[0].strip('HS')
        self.ext = file_split[-1].split('.')[1]
        self.camera = os.path.basename(os.path.dirname(filepath))

        self.filename_out = 'HS%s_%s_%s.%s' % (self.shot, self.lens_ID, self.part, self.ext)
        self.dest = os.path.join(dir_out, 'HS%s' % self.shot, self.lens_ID, self.filename_out)

w.print_section_head('Moving Media Files')

for root, dirs, files in os.walk(dir_in):
    for f in files:
        source = os.path.join(root, f)
        this_object = media_file(source)
        dest = this_object.dest

        if this_object.model is not '':
            if not os.path.isdir(os.path.dirname(dest)) and not TESTING_MODE:
                os.makedirs(os.path.dirname(dest))

            #print('    %s' % vars(this_object))
            w.printWrite('    From:   %s\n    To:     %s\n' % (source.replace('\\','/'), dest.replace('\\','/')))

            if not TESTING_MODE:
                os.rename(source, dest)
            files_out.append(this_object.filename_out)


if not TESTING_MODE:
    w.print_section_head('Moving Empty Card Folders to _trash')
    for i in range(4):
        for root, dirs, files in os.walk(dir_in):
            if len(files) == 0 and len(dirs) == 0:
                try:
                    shutil.rmtree(root)
                    print('    DELETED: %s' % root)
                except:
                    pass
else:
    w.print_section_head('Testing mode has finished')

w.close()
