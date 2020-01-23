import sys, os, shutil

in_dirs = ['']

find = 'TEXT TO FIND'
replace = 'TEXT TO REPLACE'

def fix_spelling(source):
    dirname = os.path.dirname(source)
    basename = os.path.basename(source)

    cases = [[find, replace],
             [find.upper(), replace.upper()],
             [find.lower(), replace.lower()],
             [find.title(), replace.title()]]

    if find.lower() in basename.lower():
        for case in cases:
            if case[0] in basename:
                dest = os.path.join(dirname, basename.replace(case[0], case[1]))
                os.rename(source, dest)
                print('%s\t%s --> %s' % (basename, source, dest))
                break

for in_dir in in_dirs:
    for root, dirs, files in os.walk(in_dir):
        for d in dirs:
            if find.lower() in d.lower():
                fix_spelling(os.path.join(root, d))
        for f in files:
            if find.lower() in f.lower():
                fix_spelling(os.path.join(root, f))
