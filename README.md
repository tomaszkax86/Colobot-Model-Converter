Colobot Model Converter
=======================

This program can be used to convert various 3D model formats to and from model formats used by Colobot.


Basic usage
-----------

To convert one format to another you need to run this program in terminal.

```
converter.py [switches]
```

The most basic case is when you just specify files. Actual format will be determined by extension. For example, extension "obj" means Wavefront .OBJ format and "mod" extension means old Colobot binary format.
To specify input file you use "-i" switch and to specify output file you use "-o" switch. For example, to convert .obj file to new Colobot text format, use can use following command:

```
converter.py -i box.obj -o box.txt
```

You can specify formats manually with "-if" and "-of" switches. They mean input and output formats respectively. You can also add parameters using "-ip" and "-op" switches. For example, by default Colobot format version 2 is used for output. If you need version 1, you need to add output parameter like this:

```
converter.py -i box.obj -if obj -o box.txt -of new_txt -op version=1
```


Command line switches
---------------------

Switch             | Description
-------------------|----------------------------------------
-ext               | Lists all available default extensions and exits
-f                 | Lists all available formats and exits
-i *filename*      | Sets input file name to *filename*
-if *format*       | Sets input format to *format*
-ip *name*         | Adds input format parameter *name* with no value
-ip *key*=*value*  | Adds input format parameter *key* with value *value*
-o *filename*      | Sets output file name to *filename*
-of *format*       | Sets output format to *format*
-op *name*         | Adds output format parameter *name* with no value
-op *key*=*value*  | Adds output format parameter *key* with value *value*


Supported formats
-----------------

Below are listed all formats supported by this converter. A given format can have read only, write only and read/write access. Read only means you can convert this format to something else but not into it. Write only means you can convert other format to this format but can't convert from it. Read/write means you can convert to and from this format. Format might have assigned default extension.

Format name      | Extension  | Access     | Description
-----------------|------------|------------|-------------------------------------------------------------------------
default          |            | depends    | Default format that uses filename extension to determine actual format
colobot          |            | write only | Default Colobot format (currently: old binary format)
old              | mod        | write only | Old Colobot binary format (.mod files)
new_txt          | txt        | read/write | New Colobot text format
obj              | obj        | read/write | Wavefront .OBJ format


Format specific options
-----------------------

- old
  - *dirt* - specifies dirt texture number, defaults to 0
- new_txt
  - *dirt* - specifies dirt texture name, defaults to none
  - *version* - specifies format version, defaults to 2
- obj
  - *flipX* - flips axis X during import/export
  - *flipY* - flips axis Y during import/export
  - *flipZ* - flips axis Z during import/export


State specification
-------------------

Colobot meshes specify internal state of each triangle that changes behaviour of rendering engine. You can specify state in material name like this: *Material name [state]*. *state* has to be a list of numbers or state names.

Valid state names are listed in table below. Some states are not properly documented and have unknown effects.

Name                | Code    | Description
--------------------|---------|---------------------------------------
normal              | 0       | Normal texture
ttexture_black      | 1       | Texture with black color transparency
ttexture_white      | 2       | Texture with white color transparency
ttexture_diffuse    | 4       | Texture with transparency
wrap                | 8       | Wrap mode
clamp               | 16      | Clamp mode
light               | 32      | Completely bright
dual_black          | 64      | Dual black ?
dual_white          | 128     | Dual white ?
part1               | 256     | Part 1
part2               | 512     | Part 2
part3               | 1024    | Part 3
part4               | 2048    | Part 4
2face               | 4096    | Render both faces
alpha               | 8192    | Transparency with alpha channel
second              | 16384   | Use second texture
fog                 | 32768   | Render fog
tcolor_black        | 65536   | Black color is transparent
tcolor_white        | 131072  | White color is transparent
text                | 262144  | Used for rendering text
opaque_texture      | 524288  | Opaque texture
opaque_color        | 1048576 | Opaque color


Changelog
---------

- 1.5
  - added support for writing Wavefront OBJ files
  - added switches for *obj* format
  - added base for COLLADA format (not yet useful)
  - added *-ext* switch
- 1.4
  - more refactoring
  - split some code into additional file
  - changed way of registering and accessing formats
  - added registering of filename extensions
  - added *default* format that chooses appropriate format by filename extension
  - added filename extensions: *mod*, *txt* and *obj*
- 1.3.1
  - added support for writing old Colobot model format files
  - added parameter to specify dirt texture
- 1.3
  - code refactored
  - added simple and extensible API for format conversion
  - added command line switches
- 1.2
  - code refactored, split into separate files
- 1.1
  - added alternate state specification
  - default output format version changed to 2
- 1.0
  - state specification in material name ("Material [state]")