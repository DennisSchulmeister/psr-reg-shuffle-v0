:Title:   Planed developments for PSR Registration Shuffler 0.4
:Author:  Dennis Schulmeister
:E-Mail:  dennis -at- ncc-1701a.homelinux.net
:Web:     http://www.psrregshuffle.de
:License: GNU Free Documentation License

.. contents ::


New Start-Up Procedure
======================

At the moment there are two Python scripts responsible for starting the program.
One for starting the system-wide installed version and one for starting the
program directly from trunk. The reason for that is that different directories
need to be used for the program data and the translation strings depending upon
which version of the program shall be executed. Thus both scripts find out where
translation strings and program data lie, set up localozation and start the
program by getting an instance of the main class. The installed script also
modifies the environment so that a local instance of GTK+ can be used if it is
available (this is for the Windows distribution).

Although they are very small both scripts share a fair amount of similar code.
Another disadvantage is that they need to modify the __builtin__ dictionary in
order to pass the path of the data directory to the program.

So in order to get rid of this all start-up related logic shall be moved into
the main module and its main class. It should thus be possible to start the
program without external scripts whatsoever. However trunk shall still contain a
small shell script in order to run the program directly from trunk. The script
shall set two environment variables with the names of the data and the
translation directories and then start the program simply by invoking the Python
interpreter. The main module then needs to read those variables or fall back to
the system directories in case the variables aren't set.


Correct Usage of Decorators
===========================

Some methods are defined as static classmethods but don't make use of the
proper decorator syntax. Although technicaly correct those sources shall be
modified in order to use decorators instead of variable assignment.

Wrong syntax::

  class SomeClass:
     def someMethod:
        pass

     someMethod = classmethod(someMethod)

Decorator Syntax::

  class SomeClass:
      @classmethod
      def someMethod:
          pass


User Interface Redesign
=======================

blabla blabla blabla
blabla blabla blabla
blabla blabla blabla


Support for Yamaha PSR-9000 / 9000pro
=====================================

General Memoray and Backup Layout
---------------------------------

Unlike newer keyboard models such as the Yamaha PSR-2000 or the Yamaha Tyros
descendants the Yamaha PSR-9000 doesn't map registration banks to individual
files. Instead the PSR-9000 and the 9000pro have a fixed capacity of 64
registration banks which remain in Flash ROM and cannot be treated like files
at all. This means they cannot be organized in directories and are ordered
independendly from their names. Also they cannot be copied from or to disk
individually. Only a backup can be done which also includes registrations.

Every backup consistas of the following files from which only BACKUP.INI is
really needed. All other files are optional.

 * BACKUP.INI
 * MDB.bup
 * MPD.bup
 * OTS.bup
 * REG.bup
 * STY.bup
 * SUP.bup

BACKUP.INI contains information about the backup's content and REG.bup contains
exactly 64 registration banks. The contents of the other files can be guessed
from their names but is largely unknown.

BACKUP.INI is a latin1 encoded text file with Windows style line-endings (CRLF).
It's layout is somewhat borrowed from INI files:

  [TITLE]
  PSR-9000 BACKUP.INI
  YAMAHA Corporation
  [DISK NO]
  DISK001
  [INSTRUMENT]
  PSR-9000
  [VERSION]
  Ver1.12
  [TOTAL USER DATA SIZE]
  2770276KB
  [BACKUP SETUP]
  TOTAL FILE NUM:0
  7 = SUP.bup
  [BACKUP STYLE]
  TOTAL FILE NUM:0
  2 = STY.b01
  [BACKUP OTS]
  TOTAL FILE NUM:0
  [BACKUP MUSIC DB]
  TOTAL FILE NUM:0
  [BACKUP REGIST]
  TOTAL FILE NUM:0
  [BACKUP MULTI PAD]
  TOTAL FILE NUM:0
  [DATAEND]

It is noteworthy that a backup can span several floppy disks. In that case each
disk contains its own BACKUP.INI file and disks are numbered adjacently. The
first disk is always named DISK001 and the last one DISKFFF. User data size
then refers to the whole backup and needs to be the same value on all disks.

The sub-field TOTAL FILE NUM seems to be ignored as it always seems to be 0
no mater how many files there are. If a data section cannot be backed up to a
single disk it needs to be split and several disks need to be used with each
disk containing only one file per Flash ROM data section. File extensions are
then numberd in accordance to the disks. It is assumed however that only styles
can grow large enough to span several disks. It's not known how the instruments
reacts to the other files being split.

The above backup consists of sevarl disks because the disk name is not DISKFFF.
If it were to span two disks the second disk's BACKUP.INI could look like this:

  [TITLE]
  PSR-9000 BACKUP.INI
  YAMAHA Corporation
  [DISK NO]
  DISKFFF
  [INSTRUMENT]
  PSR-9000
  [VERSION]
  Ver1.12
  [TOTAL USER DATA SIZE]
  2770276KB
  [BACKUP STYLE]
  TOTAL FILE NUM:0
  2 = STY.bFF
  [BACKUP OTS]
  TOTAL FILE NUM:0
  5 = OTS.bup
  [BACKUP MUSIC DB]
  TOTAL FILE NUM:0
  3 = MDB.bup
  [BACKUP REGIST]
  TOTAL FILE NUM:0
  4 = REG.bup
  [BACKUP MULTI PAD]
  TOTAL FILE NUM:0
  6 = MPD.bup
  [DATAEND]

Note that the style section doesn't fit to a single disks and thus can be found
on both disks. In both cases the file number in BACKUP.INI is number 2. Besides
that file numbers are always unique.

The Binary Registration Backup File
-----------------------------------

The registrations are stored as raw byte streams in REG.bup. This file starts
with a fixed-length 24 byte header followed by exactly 64 registration banks
with a fixed length of 3776 bytes each. Each bank contains a 16 byte long name
and exactly 8 registrations. Each registration also starts with a 16 byte long
name followed by a variable length data section. If a name is smaller than 16
bytes it's usually paded with spaces (0x20). But zero-padded strings can also
be found. All strings are latin1 encoded.

  GENERAL LAYOUT

  REG.bup
   |--- 24 bytes file header
   |--+ 64 registration banks
   |  |--+ 16 byte name
   |  |  | 8 registrations
   |  |  |--+ 16 byte name
   |  |  |  | Registration data
   |--- 4 bytes file trailer


  WITH BANKS SHOWN

  REG.bup
   |--- 24 bytes file header
   |--+ REG BANK 001
   |--+ REG BANK 002
   |--+ ...
   |--+ REG BANK 064
   |--- 4 bytes file trailer


  WITH BANKS AND REGISTRAIONS SHOWN

  REG.bup
   |--- 24 bytes file header
   |--+ REG BANK 001
   |  |--+ 16 bytes name
   |  |  | REGISTRATION 001
   |  |  | REGISTRATION 002
   |  |  | REGISTRATION 003
   |  |  | REGISTRATION 004
   |  |  | REGISTRATION 005
   |  |  | REGISTRATION 006
   |  |  | REGISTRATION 007
   |  |  | REGISTRATION 008
   |--+ REG BANK 002
   |  |  | REGISTRATION 001
   |  |  | REGISTRATION 002
   |  |  | REGISTRATION 003
   |  |  | REGISTRATION 004
   |  |  | REGISTRATION 005
   |  |  | REGISTRATION 006
   |  |  | REGISTRATION 007
   |  |  | REGISTRATION 008
   |--+ ...
   |--+ REG BANK 064
   |  |  | REGISTRATION 001
   |  |  | REGISTRATION 002
   |  |  | REGISTRATION 003
   |  |  | REGISTRATION 004
   |  |  | REGISTRATION 005
   |  |  | REGISTRATION 006
   |  |  | REGISTRATION 007
   |  |  | REGISTRATION 008
   |--- 4 bytes file trailer


  WITHREGISTRATION DATA SHOWN

  REG.bup
   |--- 24 bytes file header
   |--+ REG BANK 001
   |  |--+ 16 bytes name
   |  |  | REGISTRATION 001
   |  |  |--+ 16 bytes name
   |  |  |  | Registration data
   |  |  | REGISTRATION 002
   |  |  |--+ 16 bytes name
   |  |  |  | Registration data
   |  |  | REGISTRATION 003
   |  |  |--+ 16 bytes name
   |  |  |  | Registration data
   |  |  | REGISTRATION 004
   |  |  |--+ 16 bytes name
   |  |  |  | Registration data
   |  |  | REGISTRATION 005
   |  |  |--+ 16 bytes name
   |  |  |  | Registration data
   |  |  | REGISTRATION 006
   |  |  |--+ 16 bytes name
   |  |  |  | Registration data
   |  |  | REGISTRATION 007
   |  |  |--+ 16 bytes name
   |  |  |  | Registration data
   |  |  | REGISTRATION 008
   |  |  |--+ 16 bytes name
   |  |  |  | Registration data
   |--+ REG BANK 002
   |--+ ...
   |--- 4 bytes file trailer

The file header consists of the following bytes (given in hexadecimal notation
just like a hex editor might show it):

  0x00000000: 00 46 8e 94 00 03 b0 0c - 00 00 00 00 00 00 00 00 .F..............
  0x00000010: 52 45 47 39 5f 31 30 32                           REG9_102

The file trailer consists of the following four bytes: 0xE7 0x97 0xDD 0xAD

Even if a backup doesn't encompass all of the keyboards 64 registration banks it
still holds exactly 64 banks with the last ones being empty containing just
empty registrations. Those empty banks are then named BANKxx with xx being the
bank number (starting with 01). Empty registrations are simply called 001 ~ 008.

Registration data
-----------------

Little is known about the structure of the registration settings themselves.
It is asumed though that they follow a fixed layout of a C structure because it
has been observed that they're always 470 bytes long including the 16 byte name
at the very beginning. Also there are no section headers like with the later
models and if a registration is empty it just contains zero-bytes except for
its name.

Registrations seem to employ a simple check-sum algorithm which allows for
checking a registration bank's integrity. Usually the last byte of a non-empty
registration contains the first letter of the following registration. This is
not true for empty registrations where the last byte is always zero. The last
byte of the last non-empty registration is always an ascii R (0x52). But at
least one exception to this rule has been found and so it remains unknown
whether this condition is really checked by the instruments.

  EXAMPLE OF AN EMPTY REGISTRATION

  0x0003a8c0: 30 30 35 20 20 20 20 20 - 20 20 20 20 20 20 20 20 005
  0x0003a8d0: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a8e0: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a8f0: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a900: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a910: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a920: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a930: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a940: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a950: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a960: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a970: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a980: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a990: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a9a0: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a9b0: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a9c0: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a9d0: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a9e0: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003a9f0: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003aa00: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003aa10: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003aa20: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003aa30: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003aa40: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003aa50: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003aa60: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003aa70: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003aa80: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 @@@@@@@@@@@@@@@@
  0x0003aa90: 00 00 00 00 00 00                                 @@@@@@


  EXAMPLE OF A NON-EMPTY REGISTRATION

  0x00000780: 53 69 6c 76 65 72 79 20 - 53 61 78 65 73 20 20 20 Silvery Saxes
  0x00000790: 01 00 00 05 7f 03 36 0b - 2a 5a 52 40 40 40 40 40 ......6.*ZR@@@@@
  0x000007a0: 40 4f 82 5c 47 4d 3c 4f - 3d 40 28 00 40 2d 40 4e @O.\GM<O=@(.@-@N
  0x000007b0: 3a 3a 40 2b 00 16 2c 00 - 22 2c 50 1e 28 00 00 00 ::@+..,.",P.(...
  0x000007c0: 14 34 2e 00 00 00 00 00 - 00 00 00 00 00 00 00 00 .4..............
  0x000007d0: 7f 00 7b 7f 00 00 00 00 - 21 00 76 1b 00 74 1b 00 ..{.....!.v..t..
  0x000007e0: 70 30 00 70 00 00 71 19 - 00 40 40 40 34 3a 40 40 p0.p..q..@@@4:@@
  0x000007f0: 40 00 40 40 40 43 3c 3c - 40 40 00 40 40 40 40 40 @.@@@C<<@@.@@@@@
  0x00000800: 40 40 40 00 40 40 40 40 - 40 40 40 40 7f 00 73 12 @@@.@@@@@@@@..s.
  0x00000810: 00 36 40 2d 00 00 00 00 - 02 00 40 30 40 40 00 01 .6@-......@0@@..
  0x00000820: 01 11 40 42 08 40 00 00 - 00 00 00 7f 63 01 7f 7f ..@B.@......c...
  0x00000830: 00 01 00 00 20 20 20 20 - 20 20 00 00 00 00 00 00 ....      ......
  0x00000840: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 ................
  0x00000850: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 ................
  0x00000860: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 ................
  0x00000870: 00 00 00 00 00 00 00 00 - 00 00 00 00 00 00 00 00 ................
  0x00000880: 00 00 00 00 00 00 00 00 - 00 7f 7f 00 75 42 ff 5e ............uB.^
  0x00000890: 40 00 00 00 00 00 02 20 - 40 40 40 46 7f 00 72 41 @...... @@@F..rA
  0x000008a0: ff 46 40 00 00 00 00 00 - 02 1e 40 40 46 48 7f 00 .F@.......@@FH..
  0x000008b0: 74 34 00 50 40 00 00 00 - 00 00 02 24 40 40 40 40 t4.P@......$@@@@
  0x000008c0: 01 01 01 7f 01 11 00 26 - 7f 01 11 00 26 7f 01 11 .......&....&...
  0x000008d0: 00 28 00 00 15 00 1e 40 - 26 00 00 02 40 00 01 7f .(.....@&...@...
  0x000008e0: 5a 17 7f 04 7f 03 00 00 - 40 40 40 40 40 40 40 40 Z.......@@@@@@@@
  0x000008f0: 40 40 40 40 01 00 00 00 - 00 52 30 ff 00 0f 00 24 @@@@.....R0....$
  0x00000900: 64 05 0f 00 24 64 0f 0f - 02 46 00 01 07 01 52 40 d...$d...F....R@
  0x00000910: 40 40 40 40 8f 00 00 00 - 8f 00 00 00 00 00 00 00 @@@@............
  0x00000920: ff 00 00 00 ff 00 00 00 - ff 00 00 00 ff 00 00 00 ................
  0x00000930: 03 00 00 00 00 00 4e 00 - 00 00 00 00 00 00 00 00 ......N.........
  0x00000940: 00 00 00 00 00 00 00 4f - 54 53 20 42 41 4e 4b 30 .......OTS BANK0
  0x00000950: 30 34 20 20 20 53                                 04   S


New Data Model
==============

blabla blabla blabla
blabla blabla blabla
blabla blabla blabla

(Single Data Provider for Available Registrations)

blabla blabla blabla
blabla blabla blabla
blabla blabla blabla
