#!/usr/bin/python
__author__ = 'Anne Marie Merritt, anne.marie.merritt@gmail.com'
'''
    License: MIT

    The MIT License

    SPDX short identifier: MIT

    Author:  Anne Marie Merritt, anne.marie.merritt@gmail.com

    Copyright 2018 Stephanie Strickland, www.stephaniestrickland.com
    (who commissioned the code, with assistance from JC Chatelain and Ian Hatcher)

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
    documentation files (the "Software"), to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
    to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of
    the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
    WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
    OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    Program Summary:

    This program is implemented in Python 3.x.

    This program reads a manifest file to map a group number to a file name. Group files contain text delimited
    by a number between 1 and 1024.

    It then reads each file so designated and assigns the entries contained to a logical group with which it is
    associated.

    Finally, it reads the input bell file. Each individual character references a group file from which an entry will
    be selected at random and emitted without replacement.  When all the entries of a group have been emitted, the group
    will refresh anew; all entries are again eligible to be selected at random as subject to the reference in the bell
    file, then emitted without replacement until empty, at which time the group is again refreshed from source.



'''

import os
import sys
import random
import argparse

''' Global Variables '''

_encoding_style= 'utf-8'

# lookup group filename given group ID
_groups_dict = {}
# lookup group ID given group filename
_inv_groups_dict = {}
# Keeps track of what lines have been used per group
_file_contents_dict = {}
# Original contents can be restored when all lines are used to re-use.
_file_contents_orig_dict = {}

# Each line in input is preceded by a numerical delimiter.  This lets us separate input data.
_entry_delimiters = set([str(i) for i in range(0, 1024)])

_default_groupdir = "./groups"
_default_output_name = "output.txt"
_default_manifest_name = "manifest.txt"
_default_input_name = "ringtones.txt"

def _init_manifest_dict(group_dir):
    '''Load the manifest listing the mapping between groupID and filename.

    :param group_dir: Directory containing the manifest file
    :return: None.  Initializes global groups_dict and inv_groups_dict variables.
    '''

    with open(os.path.join(os.path.abspath(group_dir), _default_manifest_name), mode='r',
              encoding=_encoding_style) as thisfile:
        for line in thisfile:
            groupID, groupFileName = line.split()
            # groupentry[0] is groupID, groupentry [1] is filename of corresponding group.
            _groups_dict[groupID] = groupFileName
            # Inverse lookup, given filename, give me the group ID
            _inv_groups_dict[groupFileName] = groupID
            print (("Mapping ID {} to filename {} ".format(groupID, groupFileName)))


def _load_groups(group_dir):
    ''' Load a groups file after the manifest has been loaded which relates
        the group file name with the group identifier referenced by the
        bellring inputs.
    :param group_dir:
    :return: None.  Global group dict is initialized with all groups and their related text entries.
    '''

    files = os.listdir(group_dir)
    files.remove(_default_manifest_name)
    entry_contents = ""
    for name in files:
        # If filename isn't in manifest, move along and don't load it.
        r = _inv_groups_dict.get(name, None)
        if r is None:
            print(("NON_FATAL: File {} is not mapped in manifest file {} .").format(name, _default_manifest_name))
            continue
        print("Loading groupfile {}".format(name))
        all_lines = []
        # Entries can be multiline but are delimited by a number preceding the entry.
        with open(os.path.join(os.path.abspath(group_dir), name), mode='r', encoding=_encoding_style) as thisfile:
            for line in thisfile:
                value = line.strip()
                if value in _entry_delimiters:
                    # New entry!
                    # old entry is done.  Add to all_lines.
                    if len(entry_contents) > 0:
                        all_lines.append(entry_contents)
                        # Get ready for new entry contents.
                        entry_contents = ""
                else:
                    # Entry is not done yet.  Append to the previous entry contents, if any.
                    if len(line.strip()) > 0:
                        entry_contents = entry_contents + line
        if len(entry_contents) > 0:
            all_lines.append(entry_contents)
            entry_contents = ""

        group = _inv_groups_dict[name]
        # Initialize unused lines
        _file_contents_dict[group] = all_lines
        # Keep an original copy around to reinitialize as necessary
        _file_contents_orig_dict[group] = list(all_lines)


def _fetch_random_line(group_index):
    '''
    :param group_index: Group ID from which to remove a line
    :return:  Returns a line from the given group
    '''

    linelist = _file_contents_dict[group_index]
    listsize = len(linelist)
    if listsize == 1:
        listelem = linelist[0]
        # We got the last one.  Refresh the source group with original contents.
        _file_contents_dict[group_index] = list(_file_contents_orig_dict[group_index])
    else:
        random_idx = random.randint(0,listsize - 1)
        listelem = linelist.pop(random_idx)

    return listelem


def _parse_ringtones(ringfile, outfile):
    '''
    :param ringfile:  Name of bells file to parse
    :param outfile:  Output file to emit random lines to
    :return: No return.
    '''

    for thisline in ringfile:
        # get group name from each char in line
        linelist = list(thisline.strip())

        for x in linelist:
            thisline = _fetch_random_line(x)
            # Emit the source file from which the random line originated in an xml-ish styling.
            outfile.write("<ringfile name=\"{}\" id=\"{}\"/>\n".format(_groups_dict[x], x))
            # Emit the selected random line.
            outfile.write(thisline)
            outfile.write("\n")

        # At the end of each bell group emit a page break so it can be replaced later
        # during post-processing.
        outfile.write("<page_break>\n")


def _parse_args():
    '''
        This routine parses the input arguments for later use.
    :return:  returns structure containing all given input args.
    '''

    parser = argparse.ArgumentParser(description='Parse bell file and emit corresponding group\'s random lines.')

    parser.add_argument('--groupdir', help='Directory containing Groups to parse Default is ' + _default_groupdir,
                        required=False, dest='group_dir')

    parser.add_argument('--output',
                        help="Name of output file to write to.  Default is " + _default_output_name,
                        required=False, dest='output_name')

    parser.add_argument('--input',
                        help="Name of bell file.  Default is " + _default_input_name,
                        required=False, dest='input_name')

    # Default values are set in the global variables near the top of the script.
    parser.set_defaults(group_dir=_default_groupdir,
                        output_name=_default_output_name,
                        input_name=_default_input_name)

    return parser.parse_args()


if __name__ == "__main__":
    #This is where all the action is.  Main!

    # Read the command line args, if any.
    args = _parse_args()

    # Read the manifest to setup the group to filename mapping
    _init_manifest_dict(args.group_dir)

    # Read the group files to extract the text for each entry
    _load_groups(args.group_dir)
    with open(args.input_name, mode='r', encoding=_encoding_style) as ringfile, \
            open(args.output_name, mode='a', encoding=_encoding_style) as outfile:
    # Read the bells file to determine what group to read text from, and emit to the output file.
        _parse_ringtones(ringfile, outfile)

    print(("Emited output to {}").format(os.path.abspath(args.output_name)))
    sys.exit(0)
