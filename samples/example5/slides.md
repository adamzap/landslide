Macros to Include Files
=======================

---

Syntax
------

- The basic argline syntax is simple: 1, 2, or 3 space-separated arguments.  The
  first argument is always the file names.

- The remainder are (optionally `/`-delimited patterns) or integer line numbers,
  or "`$`" to represent the end of the file.

        .{ code | coden | include }:   <file>   [ <pattern>   [<pattern>] ]

    + `code`: include as a highlighted code block without linenos.

    + `coden`: include as a highlighted code block with linenos.

    + `include`: include the file as is.

---

Syntax
------

- Negative line numbers are allowed and works as expected, i.e. `-1` means the
  last line and so on.

- Patterns may optionally be succeeded with a signed offset spesification:
  "`/pattern/+n`" for `n` lines downward after matched line, and "`/pattern/-n`"
  for `n` lines upward before matched line.

- Shortcut: In an offset specification, use "`+`" for "`+1`", and "`-`" for
  "`-1`".

---

Gotchas
-------

- In patterns, no quotes and remember the args are blank-separated; so **you
  might want to use "`.`" to represent a blank.**

- Language is detected from the extension of the included file; so **make sure
  to use the proper extension.**

---


Including as Code
=================

---

Whole File
----------

Whole file with line numbers:

        .coden: day.c

.coden: day.c

---

One Line
--------

- 8th line

        .code: day.c 8

.code: day.c 8


- Matched line

        .code: day.c /.+wednesday/

.code: day.c /.+wednesday/

---

One Line
--------

- Last line (two alternatives)

        .code: day.c -1
        .code: day.c $

.code: day.c $

- Third line from end

        .code: day.c -3

.code: day.c -3

---

Multi Lines
-----------

- Between numbered lines (inclusive)

        .code: day.c 8 10

.code: day.c 8 10


- Between matched lines (inclusive)

        .code: day.c /.+wednesday/ /.+friday/

.code: day.c /.+wednesday/ /.+friday/

---

Multi Lines
-----------

- Matched line to end

        .code: day.c /int/ $

.code: day.c /int/ $

---

Multi Lines
-----------


- Last 5 lines

        .code: day.c -5 $

.code: day.c -5 $

---

Line Offsets
------------

- Matched lines with offsets

        .code: day.c /main\(.+\)/- /}/

.code: day.c /main\(.+\)/- /}/

---

Line Offsets
------------


- Matched lines with offsets

        .code: day.c /static.const.char.+day/+2 /}/-

.code: day.c /static.const.char.+day/+2 /}/-

- Between matched lines (exclusive)

        .code: day.c /.+wednesday/+ /.+friday/-

.code: day.c /.+wednesday/+ /.+friday/-

---

Including as Raw
================

---

Include Raw HTML
----------------

Include file as is:

        .include: body.html

.include: body.html

---

Options
=======

---

Include Path
------------

- Include files are searched through each of the colon-separated directories in
  "`includepath`" option.

- The default value of "`includepath`" is as follows:

        includepath=.:./src:./code:..:../src:../code

- That means, you can put the file, e.g. "`day.c`", into the "`src`" or "`code`"
  subdirectory, and later include it as "`.code: day.c`" (instead of "`.code:
  src/day.c`").

---

Expanding Tabs
--------------

- Tabs in the include files are expanded to spaces (default is 8 spaces), which
  work better in HTML.

- You can change the default value for tabs expansion through the "`expandtabs`"
  option.  For example:

        expandtabs=4

- Use 0 or a negative value for "`expandtabs`" to keep tabs.
