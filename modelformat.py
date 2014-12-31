#-*- coding: utf-8 -*-
# Model format base implementation
# Copyright (c) 2014 Tomasz Kapuściński

import geometry

formats = {}
extensions = {}

# base class for formats
class ModelFormat:
    def read(self, filename, model, params):
        raise ModelFormatException('Reading not implemented')
    
    def write(self, filename, model, params):
        raise ModelFormatException('Writing not implemented')

# exception class
class ModelFormatException(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return 'Model format error: {}'.format(message)

# default model format -- chooses format based on filename extension
class DefaultModelFormat(ModelFormat):
    def read(self, filename, model, params):
        ext = get_extension(filename)
        format_name = extensions[ext]
        format = formats[format_name]
        
        return format.read(filename, model, params)
    
    def write(self, filename, model, params):
        ext = get_extension(filename)
        format_name = extensions[ext]
        format = formats[format_name]
        
        return format.write(filename, model, params)

# registers format
def register_format(name, format):
    formats[name] = format

# registers filename extension that translates to given format
def register_extension(ext, name):
    extensions[ext] = name

def get_format(name):
    return formats[name]

def get_extension(filename):
    if '.' in filename:
        parts = filename.split('.')
        return parts[len(parts)-1]
    else:
        raise ModelFormatException('No file name extension found')

def read(format, filename, model, params):
    return formats[format].read(filename, model, params)

def write(format, filename, model, params):
    return formats[format].write(filename, model, params)

def convert(in_format, in_filename, in_params, out_format, out_filename, out_params):
    model = geometry.Model()
    
    read(in_format, in_filename, model, in_params)
    write(out_format, out_filename, model, out_params)

register_format('default', DefaultModelFormat())
