Hello, world, from Jules Chatelain (@juliannechat on GitHub and elsewhere)

This file contains:

WHAT IS THIS
HOW TO USE THE CODE
COLLABORATORS AND LINKS
PROJECT DESCRIPTION (from the book)


+++ WHAT IS THIS

This repository contains the code that Stephanie Strickland used to create _Ringing the Changes_, a code project for print published in 2020 by Counterpath Press, in the series Using Electricity, edited by Nick Montfort.

Each book in the series has been created by a computer or an algorithm. This is the code used to create the book's structure. It allows you to use your own content to create a similar project.

The Scientific Triples peal is also used in Stephanie Strickland's online  _Liberty Ring!_ written with Ian Hatcher. 

+++ HOW TO USE THE CODE

RUN_HERE contains the operating code.

The .py file acts on: 

- manifest.txt
- ringtones.txt
- files in the "groups" folder (as specified in the manifest file)

to create output.txt. 

OPTIONAL DETAIL

The output file's custom markup has two types of tags; there is a bell number tag for each text chunk and a page break tag after each "change" (set of 7 text chunks). (To create the print book, we wrote MS-Word macros that put this content onto print-friendly pages.)

The files in the "groups" folder contain placeholder text strings, to be filled by your own content. In this version only plain text (UTC-8) is supported.

The ringtones file contains a true peal of Scientific Triples, beginning and ending with the sequence 1234567. 

As a bonus, the contents of the SCIENTIFIC TRIPLES folder show how the true peal was created. If you do not need the full 5040 changes, you can substitute the ringtones_truncated version. 

+++ COLLABORATORS AND LINKS

Stephanie Strickland directed this project
www.stephaniestrickland.com

Specification midwifery by Jules Chatelain
www.juliannechatelain.com

Python code written by Anne Marie Merritt
anne.marie.merritt@gmail.com

Scientific Triples code by Bryn Reinstadler
@BrynMarieR on GitHub

Series Editor Nick Montfort
www.nickm.com

Publisher's page
http://counterpathpress.org/ringing-the-changes-stephanie-strickland

Stephanie Strickland's page about the book
http://www.stephaniestrickland.com/ringing

+++ ABOUT THIS BOOK
The computer-generated order of words in this book is based on the ancient art of tower-bell ringing. For sport, ordinary folk in seventeenth century England created highly structured ringing sequences. We now understand these as group-theory symmetry operations.
Their game, specifically, was to ring all the possible arrangements on seven bells, a daunting task because there are 7! (7 x 6 x 5 x 4 x 3 x 2 x 1), or 5,040, such patterns, each called a change or row. An entire peal would be rung in about three hours, and to do this the ringers had to memorize 5,040 unique seven-digit numbers. There were no cheat sheets, and anyone who messed up bought drinks for all the others! Because the bells weigh up to 9,000 pounds, once they are set in motion there is little ability to affect their sway. As a result, when a new change is sounded, each bell must either stay where it is or change places with its nearest neighbor.
Our code, written in Python, acts on the 5,040 fixed rows of a method called Scientific Triples. Method ringing is a modern simplification of the traditional peal. By memorizing rules for generating new changes--and not every single change itself--method ringers can plot their course ahead of time. Method performances may visit all permutations, or just a subset of them, but only once each. In the ringing world, this constraint is called _truth_; to repeat any row would make the performance _false_.
Method sequences begin and end with rounds, the practice of ringing all the bells in descending order of pitch. Ringing the Changes begins with rounds (1 2 3 4 5 6 7) and ends on a pause, after every bell text has appeared seven times, which occurs after 161 changes (in the book, pages).
Sounding from a bell tower changes are samples of sound, but in the book they are samples of language. Just as metal bells have overtones you can hear, book bells have 23 texts (or overtones, as it were) that you can read. In any run of the code, a text is randomly assigned to its bell and will not repeat until all 23 have made an appearance. Through permutation and realignment, a generated order makes plain how concerns, variously mapped, can be variously understood. By enacting the differences ordering and context make, a generated order refuses the fixed hierarchy of attention print normally enforces, a fixity swiftly seized upon as _true_ or _fake_.