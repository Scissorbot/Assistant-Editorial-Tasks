#Hey there. I would be most appreciative if you closed this window and didn't muck about in here.
#Much appreciated,
#Love, Willett






import os, csv
import sys
import datetime
import time
import shutil


started = datetime.datetime.now()
indent = 0
errors = []
PROCESS_TITLE = ''
log = ''
log_folder = 'Z:/02_AUTOMATION/logs'


def start(input):
    global log
    log = make_log(input, log_folder)
    printWrite(time.ctime() + '\n\n' + input + '\n\n')
    return log


def print_section_head(title):
    if len(title) <= 100:
        stars = '*' * round(.5 * (100 - len(title)))
        printWrite('\n\n    %s %s %s\n\n' % (stars, title.upper(), stars))
    else:
        printWrite(title.upper())


def print_section_subhead(title):
    if len(title) <= 100:
        space = ' ' * round(.25 * (100 - len(title)))
        stars = '*' * round(.25 * (100 - len(title)))
        printWrite('\n\n    %s%s %s %s%s\n\n' % (space, stars, title.upper(), stars, space))
    else:
        printWrite(title.lower())


def gap(len):
    return '    ' * len



def printWrite(output):
    with open(log, 'a') as write_file:
        write_file.write(output + '\n')
    print(output)


def err(message, done=False):
    printWrite(message)
    errors.append(message)

    if done:
        SECTION_HEADER = "error summary"
        print_section_head(SECTION_HEADER)
        printWrite('    Error Count: %s\n' % len(errors))

        for error in errors:
            printWrite(error)


def close():
    err('', done=True)
    printWrite('\n\nSTARTED\t%s\nENDED\t%s' % (started, datetime.datetime.now()))



def format_length(input, length, filler):
    input = str(input)
    if len(input) <= length:
        return '%s%s' % (str(filler) * (length - len(input)), input)
    else:
        printWrite('!!! Input out of range:\t%s (Max length: %s)' % (input, length))
        return ''


def make_log(title, path):      #REQUIRES PRINTWRITE
    file_name = title + ' (' + str(datetime.date.today()) + ').txt'
    exists = os.path.isfile(os.path.join(path, file_name))
    try:
        os.mkdir(path)
    except FileExistsError:
        print('Directory found at ' + path)
    version = 2
    while exists:
        file_name = title + ' (' + str(datetime.date.today()) + ')_' + str(version) + '.txt'
        exists = os.path.isfile(os.path.join(path, file_name))
        version += 1
    full_path = os.path.join(path, file_name)
    with open(full_path, 'w+'):
        print('File created at %s\n\n' % full_path)
    #print(time.ctime() + '\n\n' + title + '\n\n')
    return full_path
