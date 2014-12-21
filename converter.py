#-*- coding: utf-8 -*-
# Colobot Model Converter
# Version 1.2
# Copyright (c) 2014 Tomasz Kapuściński
#
# Usage:
#   converter.py input output [version]
#
#       input           input file, e.g. input.obj
#       output          output file, e.g. output.txt
#       version         (optional) output version (1 - with LOD, 2 - without LOD)
#
# Changelog:
#   1.2 (2014.12.04)
#     code refactored, split into separate files
#
#   1.1 (2014.10.30)
#     added alternate state specification
#     default output format version changed to 2
#
#   1.0 (earlier)
#     state specification in material name ("Material [state]")

import sys
import objformat
import colobotformat

version = 2

if len(sys.argv) > 3:
    version = int(sys.argv[3])

model = objformat.read_obj_model(sys.argv[1])
colobotformat.write_colobot_model(sys.argv[2], model, version)
