#-*- coding: utf-8 -*-
# Implements Colobot model format writing
# Copyright (c) 2014 Tomasz Kapuściński

import geometry
import struct

class ColobotNewTextFormat(geometry.ModelFormat):
    def read(self, filename, model, params):
        file = open(filename, 'r')
        
        triangle = geometry.Triangle()
        
        while True:
            line = file.readline()
            
            # eof
            if len(line) == 0:
                break
            
            # comments are ignored
            if line[0] == '#':
                continue
            
            # remove eol
            if line[len(line)-1] == '\n':
                line = line[:len(line)-1]
        
            values = line.split(' ');
            cmd = values[0]
            
            if cmd == 'version':
                model.version = int(values[1])
            elif cmd == 'triangles':
                continue
            elif cmd == 'p1':
                triangle.vertices[0] = parse_vertex(values)
            elif cmd == 'p2':
                triangle.vertices[1] = parse_vertex(values)
            elif cmd == 'p3':
                triangle.vertices[2] = parse_vertex(values)
            elif cmd == 'mat':
                parse_material(triangle.material, values)
            elif cmd == 'tex1':
                triangle.material.texture = values[1]
            elif cmd == 'tex2':
                triangle.material.texture2 = values[1]
            elif cmd == 'var_tex2':
                continue
            elif cmd == 'lod_level':
                triangle.material.lod = int(values[1])
            elif cmd == 'state':
                triangle.material.state = int(values[1])
                model.triangles.append(triangle)
                triangle = geometry.Triangle()
        
        file.close()
    
    def write(self, filename, model, params):
        file = open(filename, 'w')
        
        version = 2
        
        if 'version' in params:
            version = int(params['version'])

        # write header
        file.write('# Colobot text model\n')
        file.write('\n')
        file.write('### HEAD\n')
        file.write('version ' + str(version) + '\n')
        file.write('total_triangles ' + str(len(model.triangles)) + '\n')
        file.write('\n')
        file.write('### TRIANGLES\n')

        # write triangles
        for triangle in model.triangles:
            # write vertices
            for i in range(3):
                vertex = triangle.vertices[i]
                file.write('p{} c {} {} {}'.format(i+1, vertex.x, vertex.y, vertex.z))
                file.write(' n {} {} {}'.format(vertex.nz, vertex.ny, vertex.nz))
                file.write(' t1 {} {}'.format(vertex.u1, vertex.v1))
                file.write(' t2 {} {}\n'.format(vertex.u2, vertex.v2))

            mat = triangle.material
            
            dirt = 'N'
            dirt_texture = ''
            
            if 'dirt' in params:
                dirt = 'Y'
                dirt_texture = params['dirt']

            file.write('mat dif {} {} {} {}'.format(mat.diffuse[0], mat.diffuse[1], mat.diffuse[2], mat.diffuse[3]))
            file.write(' amb {} {} {} {}'.format(mat.ambient[0], mat.ambient[1], mat.ambient[2], mat.ambient[3]))
            file.write(' spc {} {} {} {}\n'.format(mat.specular[0], mat.specular[1], mat.specular[2], mat.specular[3]))
            file.write('tex1 {}\n'.format(mat.texture))
            file.write('tex2 {}\n'.format(dirt_texture))
            file.write('var_tex2 {}\n'.format(dirt))

            if version == 1:
                file.write('lod_level 0\n')

            file.write('state ' + str(mat.state) + '\n')
            file.write('\n')

        file.close()

class ColobotOldFormat(geometry.ModelFormat):
    def write(self, filename, model, params):
        file = open(filename, 'wb')
        
        # write header
        file.write(struct.pack('i', 1))      # version major
        file.write(struct.pack('i', 2))      # version minor
        file.write(struct.pack('i', len(model.triangles)))   # total triangles
        
        # padding
        for x in range(10):
            file.write(struct.pack('i', 0))
        
        # triangles
        for triangle in model.triangles:
            file.write(struct.pack('=B', True))     # used
            file.write(struct.pack('=B', False))    # selected ?
            file.write(struct.pack('=H', 0))        # padding (2 bytes)
            
            # write vertices
            for vertex in triangle.vertices:
                file.write(struct.pack('=fff', vertex.x, vertex.y, vertex.z))       # vertex coord
                file.write(struct.pack('=fff', vertex.nx, vertex.ny, vertex.nz))    # normal
                file.write(struct.pack('=ff', vertex.u1, vertex.v1))                # tex coord 1
                file.write(struct.pack('=ff', vertex.u2, vertex.v2))                # tex coord 2
            
            # material info
            mat = triangle.material
            file.write(struct.pack('=ffff', mat.diffuse[0], mat.diffuse[1], mat.diffuse[2], mat.diffuse[3]))        # diffuse color
            file.write(struct.pack('=ffff', mat.ambient[0], mat.ambient[1], mat.ambient[2], mat.ambient[3]))        # ambient color
            file.write(struct.pack('=ffff', mat.specular[0], mat.specular[1], mat.specular[2], mat.specular[3]))    # specular color
            file.write(struct.pack('=ffff', 0.0, 0.0, 0.0, 0.0))                                                    # emissive color
            file.write(struct.pack('=f', 0.0))                                                                      # power
            
            # texture name
            file.write(mat.texture)
            
            # texture name padding
            for i in range(20 - len(mat.texture)):
                file.write(struct.pack('=x'))
            
            dirt = 0
            
            if 'dirt' in params:
                dirt = int(params['dirt'])
            
            file.write(struct.pack('=ff', 0.0, 10000.0))            # rendering range
            file.write(struct.pack('i', mat.state))                 # state
            file.write(struct.pack('=H', dirt))                     # dirt texture
            file.write(struct.pack('=HHH', 0, 0, 0))                # reserved
        
        file.close()


def register(formats):
    formats['colobot'] = ColobotOldFormat()
    formats['new_txt'] = ColobotNewTextFormat()
    formats['old'] = ColobotOldFormat();

def parse_vertex(values):
    vertex_coord = geometry.VertexCoord(float(values[2]), float(values[3]), float(values[4]))
    normal = geometry.Normal(float(values[6]), float(values[7]), float(values[8]))
    tex_coord_1 = geometry.TexCoord(float(values[10]), float(values[11]))
    tex_coord_2 = geometry.TexCoord(float(values[13]), float(values[14]))
    
    return geometry.Vertex(vertex_coord, normal, tex_coord_1, tex_coord_2)

def parse_material(material, values):
    for i in range(4):
        material.diffuse[i] = float(values[2+i])
        material.ambient[i] = float(values[7+i])
        material.specular[i] = float(values[12+i])
