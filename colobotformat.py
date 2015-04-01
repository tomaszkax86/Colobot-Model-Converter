#-*- coding: utf-8 -*-
# Implements Colobot model formats
# Copyright (c) 2014 Tomasz Kapuściński

import modelformat
import geometry
import struct

class ColobotNewTextFormat(modelformat.ModelFormat):
    def __init__(self):
        self.description = 'Colobot New Text format'
        
    def get_extension(self):
        return 'txt'
    
    def read(self, filename, model, params):
        input_file = open(filename, 'r')
        
        triangle = geometry.Triangle()
        materials = []
        
        while True:
            line = input_file.readline()
            
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
                triangle.material = parse_material(values)
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

                mat_final = None

                for mat in materials:
                    if triangle.material == mat:
                        mat_final = mat

                if mat_final is None:
                    mat_final = triangle.material
                    materials.append(mat_final)

                triangle.material = mat_final
                
                model.triangles.append(triangle)
                triangle = geometry.Triangle()
        
        input_file.close()
        
        return True
    
    def write(self, filename, model, params):
        output_file = open(filename, 'w')
        
        version = 2
        
        if 'version' in params:
            version = int(params['version'])

        # write header
        output_file.write('# Colobot text model\n')
        output_file.write('\n')
        output_file.write('### HEAD\n')
        output_file.write('version ' + str(version) + '\n')
        output_file.write('total_triangles ' + str(len(model.triangles)) + '\n')
        output_file.write('\n')
        output_file.write('### TRIANGLES\n')

        # write triangles
        for triangle in model.triangles:
            # write vertices
            for i in range(3):
                vertex = triangle.vertices[i]
                output_file.write('p{} c {} {} {}'.format(i+1, vertex.x, vertex.y, vertex.z))
                output_file.write(' n {} {} {}'.format(vertex.nx, vertex.ny, vertex.nz))
                output_file.write(' t1 {} {}'.format(vertex.u1, vertex.v1))
                output_file.write(' t2 {} {}\n'.format(vertex.u2, vertex.v2))

            mat = triangle.material
            
            dirt = 'N'
            dirt_texture = ''
            
            if 'dirt' in params:
                dirt = 'Y'
                dirt_texture = params['dirt']

            output_file.write('mat dif {} {} {} {}'.format(mat.diffuse[0], mat.diffuse[1], mat.diffuse[2], mat.diffuse[3]))
            output_file.write(' amb {} {} {} {}'.format(mat.ambient[0], mat.ambient[1], mat.ambient[2], mat.ambient[3]))
            output_file.write(' spc {} {} {} {}\n'.format(mat.specular[0], mat.specular[1], mat.specular[2], mat.specular[3]))
            output_file.write('tex1 {}\n'.format(mat.texture))
            output_file.write('tex2 {}\n'.format(dirt_texture))
            output_file.write('var_tex2 {}\n'.format(dirt))

            if version == 1:
                output_file.write('lod_level 0\n')

            output_file.write('state ' + str(mat.state) + '\n')
            output_file.write('\n')

        output_file.close()
        
        return True


class ColobotOldFormat(modelformat.ModelFormat):
    def __init__(self):
        self.description = 'Colobot Old Binary format'
        
    def get_extension(self):
        return 'mod'
    
    def read(self, filename, model, params):
        input_file = open(filename, 'rb')
        
        # read header
        version_major = struct.unpack('=i', input_file.read(4))[0]
        version_minor = struct.unpack('=i', input_file.read(4))[0]

        triangle_count = struct.unpack('=i', input_file.read(4))[0]

        if version_major != 1 or version_minor != 2:
            print('Unsupported format version: {}.{}'.format(version_major, version_minor))
            return False

        # read and ignore padding
        input_file.read(40)

        materials = []

        for index in range(triangle_count):
            triangle = geometry.Triangle()

            # used, selected, 2 byte padding
            input_file.read(4)

            for vertex in triangle.vertices:
                # position, normal, uvs
                floats = struct.unpack('=ffffffffff', input_file.read(40))

                vertex.x = floats[0]
                vertex.y = floats[1]
                vertex.z = floats[2]

                vertex.nx = floats[3]
                vertex.ny = floats[4]
                vertex.nz = floats[5]

                vertex.u1 = floats[6]
                vertex.v1 = floats[7]

                vertex.u2 = floats[8]
                vertex.v2 = floats[9]

            # material colors
            floats = struct.unpack('=fffffffffffffffff', input_file.read(17 * 4))

            mat = triangle.material

            for i in range(4):
                mat.diffuse[i] = floats[0 + i]
                mat.ambient[i] = floats[4 + i]
                mat.specular[i] = floats[8 + i]

            # texture name
            chars = input_file.read(20)

            for i in range(20):
                if chars[i] == '\0':
                    mat.texture = struct.unpack('={}s'.format(i), chars[:i])[0]
                    break

            values = struct.unpack('=ffiHHHH', input_file.read(20))

            mat.state = values[2]
            dirt = values[3]

            if dirt != 0:
                mat.texture2 = 'dirty{:02d}.png'.format(dirt)

            # optimizing materials
            replaced = False

            for material in materials:
                if mat == material:
                    triangle.material = material
                    replaced = True
                    break

            if not replaced:
                materials.append(mat)

            model.triangles.append(triangle)

            # end of triangle
        
        input_file.close()
        
        return True
    
    
    def write(self, filename, model, params):
        output_file = open(filename, 'wb')
        
        # write header
        output_file.write(struct.pack('i', 1))      # version major
        output_file.write(struct.pack('i', 2))      # version minor
        output_file.write(struct.pack('i', len(model.triangles)))   # total triangles
        
        # padding
        for x in range(10):
            output_file.write(struct.pack('i', 0))
        
        # triangles
        for triangle in model.triangles:
            output_file.write(struct.pack('=B', True))     # used
            output_file.write(struct.pack('=B', False))    # selected ?
            output_file.write(struct.pack('=H', 0))        # padding (2 bytes)
            
            # write vertices
            for vertex in triangle.vertices:
                output_file.write(struct.pack('=fff', vertex.x, vertex.y, vertex.z))       # vertex coord
                output_file.write(struct.pack('=fff', vertex.nx, vertex.ny, vertex.nz))    # normal
                output_file.write(struct.pack('=ff', vertex.u1, vertex.v1))                # tex coord 1
                output_file.write(struct.pack('=ff', vertex.u2, vertex.v2))                # tex coord 2
            
            # material info
            mat = triangle.material
            output_file.write(struct.pack('=ffff', mat.diffuse[0], mat.diffuse[1], mat.diffuse[2], mat.diffuse[3]))        # diffuse color
            output_file.write(struct.pack('=ffff', mat.ambient[0], mat.ambient[1], mat.ambient[2], mat.ambient[3]))        # ambient color
            output_file.write(struct.pack('=ffff', mat.specular[0], mat.specular[1], mat.specular[2], mat.specular[3]))    # specular color
            output_file.write(struct.pack('=ffff', 0.0, 0.0, 0.0, 0.0))                                                    # emissive color
            output_file.write(struct.pack('=f', 0.0))                                                                      # power
            
            # texture name
            output_file.write(mat.texture.encode('utf-8'))
            
            # texture name padding
            for i in range(20 - len(mat.texture)):
                output_file.write(struct.pack('=x'))
            
            dirt = 0
            
            if 'dirt' in params:
                dirt = int(params['dirt'])
            
            output_file.write(struct.pack('=ff', 0.0, 10000.0))            # rendering range
            output_file.write(struct.pack('i', mat.state))                 # state
            output_file.write(struct.pack('=H', dirt))                     # dirt texture
            output_file.write(struct.pack('=HHH', 0, 0, 0))                # reserved
        
        output_file.close()
        
        return True


def parse_vertex(values):
    vertex_coord = geometry.VertexCoord(float(values[2]), float(values[3]), float(values[4]))
    normal = geometry.Normal(float(values[6]), float(values[7]), float(values[8]))
    tex_coord_1 = geometry.TexCoord(float(values[10]), float(values[11]))
    tex_coord_2 = geometry.TexCoord(float(values[13]), float(values[14]))
    
    return geometry.Vertex(vertex_coord, normal, tex_coord_1, tex_coord_2)

def parse_material(values):
    material = geometry.Material()
    
    for i in range(4):
        material.diffuse[i] = float(values[2+i])
        material.ambient[i] = float(values[7+i])
        material.specular[i] = float(values[12+i])
    
    return material


modelformat.register_format('colobot', ColobotOldFormat())
modelformat.register_format('old', ColobotOldFormat())
modelformat.register_format('new_txt', ColobotNewTextFormat())

modelformat.register_extension('mod', 'old')
modelformat.register_extension('txt', 'new_txt')
