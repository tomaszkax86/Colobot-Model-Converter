#-*- coding: utf-8 -*-
# Contains implementation of COLLADA .dae model format
# Copyright (c) 2015 Tomasz Kapuœciñski

import re
import modelformat
import geometry
from xml.dom import minidom

class COLLADAFormat(modelformat.ModelFormat):
    def __init__(self):
        self.description = 'COLLADA .dae format'
    
    def read(self, filename, model, params):
        xmldoc = minidom.parse(filename)
        
        # parse materials
        materials_xml = xmldoc.getElementsByTagName('library_materials')[0]
        materials = {}
        
        for material_xml in materials_xml.getElementsByTagName('material'):
            material = geometry.Material()
            
            material_name = material_xml.getAttribute('name')
            material_id = material_xml.getElementsByTagName('instance_effect')[0].getAttribute('url')[1:]
            
            # finding proper effects tag
            # effect_xml = None
            
            # for effect in xmldoc.getElementsByTagName('effect'):
                # if effect.getAttribute('id') == material_id:
                    # effect_xml = effect
            
            material.texture = params['texture']
            
            # end of material definition
            materials[material_name] = material

        # parse vertex data
        mesh_xml = xmldoc.getElementsByTagName('mesh')[0]
        
        # vertex arrays
        vertex_arrays = {}
        
        for source_xml in xmldoc.getElementsByTagName('source'):
            source_id = source_xml.getAttribute('id')
            float_array = source_xml.getElementsByTagName('float_array')
            
            if len(float_array) < 1:
                continue
            
            text = ''.join(t.nodeValue for t in float_array[0].childNodes)
            
            print(source_id)
            print(text)
            print(' ')
        
        return model



modelformat.register_format('collada', COLLADAFormat())
modelformat.register_extension('dae', 'collada')
