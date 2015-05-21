#-*- coding: utf-8 -*-
# Model format base implementation
# Copyright (c) 2014 Tomasz Kapuściński

import geometry

formats = {}
extensions = {}

# base class for formats
class ModelFormat:
    def get_extension(self):
        return None

    def read(self, filename, model, params):
        print('Reading not implemented')
        return False

    def write(self, filename, model, params):
        print('Writing not implemented')
        return False

# default model format -- chooses format based on filename extension
class DefaultModelFormat(ModelFormat):
    def __init__(self):
        self.description = 'Default model format'

    def read(self, filename, model, params):
        ext = get_extension(filename)
        format = get_format_by_extension(ext)

        if format is None:
            print('Unknown default format. File ' + filename + ' cannot be processed.')
            return False

        return format.read(filename, model, params)

    def write(self, filename, model, params):
        ext = get_extension(filename)
        format = get_format_by_extension(ext)

        if format is None:
            print('Unknown default format. File ' + filename + ' cannot be processed.')
            return False

        return format.write(filename, model, params)

# registers format
def register_format(name, format):
    formats[name] = format

# registers filename extension that translates to given format
def register_extension(ext, name):
    extensions[ext] = name

def get_format(name):
    if name in formats:
        return formats[name]
    else:
        return None

def get_format_by_extension(extension):
    if extension is None: return None

    if extension in extensions:
        return formats[extensions[extension]]

def get_extension(filename):
    if '.' in filename:
        parts = filename.split('.')
        return parts[len(parts)-1]
    else:
        return None

def read(format, filename, model, params):
    modelformat = get_format(format)

    if modelformat is None:
        print('Unknown format: ' + format)
        return False
    else:
        return modelformat.read(filename, model, params)

def write(format, filename, model, params):
    modelformat = get_format(format)

    if modelformat is None:
        print('Unknown format: ' + format)
        return False
    else:
        return modelformat.write(filename, model, params)

def convert(in_format, in_filename, in_params, out_format, out_filename, out_params):
    if in_filename is None:
        print('Input file not specified.')
        return False

    if out_filename is None:
        print('Output file not specified.')
        return False

    if 'directory' in in_params:
        in_filename = in_params['directory'] + '/' + in_filename

    if 'directory' in out_params:
        out_filename = out_params['directory'] + '/' + out_filename

    model = geometry.Model()

    completed = read(in_format, in_filename, model, in_params)
    if not completed: return

    completed = write(out_format, out_filename, model, out_params)
    if not completed: return

    print('{} -> {}'.format(in_filename, out_filename))

def convert_list(file_list, in_format, in_params, out_format, out_params):
    in_filename = ''
    out_filename = ''

    in_modelformat = get_format(in_format)
    out_modelformat = get_format(out_format)

    if in_modelformat is None:
        print('Unknown input format: ' + in_format)
        return

    if out_modelformat is None:
        print('Unknown output format: ' + out_format)
        return

    in_directory = ''
    if 'directory' in in_params:
        in_directory = in_params['directory'] + '/'

    out_directory = ''
    if 'directory' in out_params:
        out_directory = out_params['directory'] + '/'

    for pair in file_list:
        # parse input string
        if ':' in pair:
            parts = pair.split(':')
            in_filename = parts[0]
            out_filename = parts[1]
        else:
            index = pair.rfind('.')

            if index == -1: filename_part = pair
            else: filename_part = pair[:index]

            extension = out_modelformat.get_extension()

            if extension is None:
                print('Cannot convert file {}, unknown output format.'.format(pair))
                continue

            in_filename = pair
            out_filename = filename_part + '.' + extension

        # append directory path
        in_filename = in_directory + in_filename
        out_filename = out_directory + out_filename

        # convert format
        model = geometry.Model()

        in_modelformat.read(in_filename, model, in_params)
        out_modelformat.write(out_filename, model, out_params)

        print('{} -> {}'.format(in_filename, out_filename))

    if len(file_list) == 0:
        print('Batch list empty. No files converted.')

def print_formats():
    for format in formats.keys():
        print('{:<16}{}'.format(format, formats[format].description))

def print_extensions():
    for ext in extensions.keys():
        format = extensions[ext]
        desc = formats[format].description

        print('{:<8}{}'.format(ext, desc))

# returns parameter value
def get_param(params, name, default = None):
    if name in params:
        return params[name]
    else:
        return default


register_format('default', DefaultModelFormat())
