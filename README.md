Colobot-Model-Converter
=======================

This program can be used to convert various 3D model formats to and from model formats used by Colobot.

For now only conversion from Wavefront .OBJ format to Colobot new text format (version 1 and 2) is supported.


Basic usage
-----------

To convert one format to another you need to run this program in terminal.

```
converter.py [switches]
```

For example, to convert .obj file to Colobot format, use can use following command:

```
converter.py -i box.obj -if obj -o box.txt -of colobot
```

List of available switches:

Switch             | Description
-------------------|----------------------------------------
-i *filename*      | Sets input file name to *filename*
-if *format*       | Sets input format to *format*
-ip key=value      | Adds input format parameter *key* with value *value*
-o *filename*      | Sets output file name to *filename*
-of *format*       | Sets output format to *format*
-op key=value      | Adds output format parameter *key* with value *value


State specification
-------------------

Colobot meshes specify internal state of each triangle that changes behaviour of rendering engine. You can specify state in material name like this: *Material name [state]*. *state* has to be a list of numbers or state names.


Changelog
---------

- 1.3
-- code refactored
-- added simple and extensible API for format conversion
-- added command line switches
- 1.2
-- code refactored, split into separate files
- 1.1
-- added alternate state specification
-- default output format version changed to 2
- 1.0
-- state specification in material name ("Material [state]")