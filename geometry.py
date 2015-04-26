#-*- coding: utf-8 -*-
# Implements Colobot geometry specification
# Copyright (c) 2014 Tomasz Kapuściński

class VertexCoord:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return abs(self.x - other.x) < 1e-3 and abs(self.y - other.y) < 1e-3 and abs(self.z - other.z) < 1e-3

    def __ne__(self, other):
        return not self == other

class TexCoord:
    def __init__(self, u, v):
        self.u = u
        self.v = v
        
    def __eq__(self, other):
        return abs(self.u - other.u) < 1e-3 and abs(self.v - other.v) < 1e-3

    def __ne__(self, other):
        return not self == other

class Normal:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __eq__(self, other):
        return (abs(self.x - other.x) < 1e-3) and (abs(self.y - other.y) < 1e-3) and (abs(self.z - other.z) < 1e-3)

    def __ne__(self, other):
        return not self == other

class Vertex:
    def __init__(self, vertex = VertexCoord(0, 0, 0), normal = Normal(0, 0, 0), tex1 = TexCoord(0.0, 0.0), tex2 = TexCoord(0.0, 0.0)):
        self.x = vertex.x
        self.y = vertex.y
        self.z = vertex.z
        self.nx = normal.x
        self.ny = normal.y
        self.nz = normal.z
        self.u1 = tex1.u
        self.v1 = tex1.v
        self.u2 = tex2.u
        self.v2 = tex2.v

class Triangle:
    def __init__(self):
        self.vertices = [Vertex(), Vertex(), Vertex()]
        self.material = Material()

class Model:
    def __init__(self):
        self.triangles = []

class Material:
    def __init__(self):
        self.texture = ''
        self.texture2 = ''
        self.ambient = [0.0, 0.0, 0.0, 0.0]
        self.diffuse = [0.8, 0.8, 0.8, 0.0]
        self.specular = [0.5, 0.5, 0.5, 0.0]
        self.state = 0
        self.version = 2
        self.lod = 0
        
    def __eq__(self, other):
        if self.texture != other.texture:
            return False
        if self.texture2 != other.texture2:
            return False
        if self.state != other.state:
            return False
        if self.lod != other.lod:
            return False
        
        for i in range(4):
            if abs(self.ambient[i] - other.ambient[i]) > 1e-3:
                return False
            if abs(self.diffuse[i] - other.diffuse[i]) > 1e-3:
                return False
            if abs(self.specular[i] - other.specular[i]) > 1e-3:
                return False
        
        return True

    def __ne__(self, other):
        return not self == other

# triangulates polygon
def triangulate(vertices, flipOrder = False):
    result = []

    first = vertices[0]
    third = vertices[1]

    count = len(vertices)

    for i in range(2, count):
        second = third
        third = vertices[i]

        triangle = Triangle()

        # reverses order
        if flipOrder:
            temp = second
            second = third
            third = temp
        
        triangle.vertices[0] = first
        triangle.vertices[1] = second
        triangle.vertices[2] = third

        result.append(triangle)

    return result

# encodes state to number
def encode_state(state):
    result = 0

    for value in state.split(','):
        if value in state_to_number:
            value = state_to_number[value]
        result |= int(value)

    return result

# decodes state from number
def decode_state(state):
    labels = []
    
    if state != 0:
        for i in range(21):
            mask = 1 << i
            if (state & mask) != 0:
                labels.append(state_to_string[mask])
    else:
        labels.append('normal')
    
    return ','.join(labels)

# state dictionary
state_to_number = {}
state_to_string = {}

def add_state(text, number):
    state_to_number[text] = number
    state_to_string[number] = text

add_state('normal', 0)                      # standard texture
add_state('ttexture_black', 1 << 0)         # black texture is transparent
add_state('ttexture_white', 1 << 1)         # white texture is transparent
add_state('ttexture_diffuse', 1 << 2)       # transparent texture
add_state('wrap', 1 << 3)                   # wrap mode
add_state('clamp', 1 << 4)                  # clamp mode
add_state('light', 1 << 5)                  # completely bright
add_state('dual_black', 1 << 6)             # dual black ?
add_state('dual_white', 1 << 7)             # dual white ?
add_state('part1', 1 << 8)                  # part 1
add_state('part2', 1 << 9)                  # part 2
add_state('part3', 1 << 10)                 # part 3
add_state('part4', 1 << 11)                 # part 4
add_state('2face', 1 << 12)                 # render both faces
add_state('alpha', 1 << 13)                 # alpha channel is transparency
add_state('second', 1 << 14)                # use second texture
add_state('fog', 1 << 15)                   # render fog
add_state('tcolor_black', 1 << 16)          # black color is transparent
add_state('tcolor_white', 1 << 17)          # white color is transparent
add_state('text', 1 << 18)                  # used for rendering text
add_state('opaque_texture', 1 << 19)        # opaque texture
add_state('opaque_color', 1 << 20)          # opaque color
