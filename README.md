Colobot-Model-Converter
=======================

This program can be used to convert various 3D model formats to and from model formats used by Colobot.

For now only convertion from Wavefront .OBJ format to Colobot new text format version 1 and 2 is supported.


Basic usage
-----------

To convert .obj file to Colobot format, open terminal and run program like this:

```
converter.py input.obj output.txt
```

By default, program outputs Colobot format version 2. If you need version 1, use following command:

```
converter.py input.obj output.txt 1
```


State specification
-------------------

Colobot meshes specify internal state of each triangle that changes behaviour of rendering engine. You can specify state in material name like this: *Material name [state]*. *state* has to be a list of numbers or state names.
