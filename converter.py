#-*- coding: utf-8 -*-
# Colobot Model Converter
# Version 1.6
# Copyright (c) 2014 Tomasz Kapuściński

import sys
import geometry
import modelformat

# put libraries with model format implementations here
import objformat
import colobotformat
#import colladaformat

# parse arguments
i = 1
n = len(sys.argv)

batch_mode = False
file_list = []

in_filename = None
in_format = 'default'
in_params = {}

out_filename = None
out_format = 'default'
out_params = {}

while i < n:
    arg = sys.argv[i]
    
    if arg == '-i':
        in_filename = sys.argv[i+1]
        i = i + 2
    elif arg == '-if':
        in_format = sys.argv[i+1]
        i = i + 2
    elif arg == '-ip':
        text = sys.argv[i+1]
        
        if '=' in text:
            pair = text.split('=')
            in_params[pair[0]] = pair[1]
        else:
            in_params[text] = 'none'
        
        i = i + 2
    elif arg == '-o':
        out_filename = sys.argv[i+1]
        i = i + 2
    elif arg == '-of':
        out_format = sys.argv[i+1]
        i = i + 2
    elif arg == '-op':
        text = sys.argv[i+1]
        
        if '=' in text:
            pair = text.split('=')
            out_params[pair[0]] = pair[1]
        else:
            out_params[text] = 'none'
        
        i = i + 2
    elif arg == '-batch':
        batch_mode = True
        i = i + 1
    elif arg == '-add':
        file_list.append(sys.argv[i+1])
        i = i + 2
    elif arg == '-addlist':
        listfile = open(sys.argv[i+1], 'r')
        
        for line in listfile.readlines():
            if len(line) == 0: continue
            if line[-1] == '\n': line = line[:-1]
            file_list.append(line)
        
        listfile.close();
        i = i + 2
    elif arg == '-f':
        modelformat.print_formats()
        exit()
    elif arg == '-ext':
        modelformat.print_extensions()
        exit()
    else:
        print('Unknown switch: {}'.format(arg))
        exit()

# convert file

if batch_mode:
    modelformat.convert_list(file_list, in_format, in_params, out_format, out_params)
else:
    modelformat.convert(in_format, in_filename, in_params, out_format, out_filename, out_params)
