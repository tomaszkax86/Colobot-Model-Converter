#-*- coding: utf-8 -*-
# implements Colobot model format writing
# Copyright (c) 2014 Tomasz Kapuściński

# writes model in new Colobot text format
def write_colobot_model(filename, model, version):
    file = open(filename, 'w')

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
            file.write('p{0} c {1} {2} {3}'.format(i+1, vertex.x, vertex.y, vertex.z))
            file.write(' n {0} {1} {2}'.format(vertex.nz, vertex.ny, vertex.nz))
            file.write(' t1 {0} {1}'.format(vertex.u, vertex.v))
            file.write(' t2 {0} {1}\n'.format(vertex.u, vertex.v))

        material = triangle.material

        file.write('mat dif {0} {1} {2} 0'.format(material.diffuse[0], material.diffuse[1], material.diffuse[2]))
        file.write(' amb {0} {1} {2} 0'.format(material.ambient[0], material.ambient[1], material.ambient[2]))
        file.write(' spc {0} {1} {2} 0\n'.format(material.specular[0], material.specular[1], material.specular[2]))
        file.write('tex1 ' + material.texture + '\n')
        file.write('tex2 \n')
        file.write('var_tex2 Y\n')

        if version == 1:
            file.write('lod_level 0\n')

        file.write('state ' + str(material.state) + '\n')
        file.write('\n')

    file.close()
