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
    def __init__(self, vertex, normal, tex1, tex2 = TexCoord(0.0, 0.0)):
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
        self.vertices = [0, 0, 0]
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
def triangulate(vertices):
    result = []

    first = vertices[0]
    third = vertices[1]

    count = len(vertices)

    for i in range(2, count):
        second = third
        third = vertices[i]

        triangle = Triangle()

        # reverses order
        triangle.vertices[0] = first
        triangle.vertices[1] = second
        triangle.vertices[2] = third

        result.append(triangle)

    return result
