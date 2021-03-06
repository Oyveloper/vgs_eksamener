#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fjerner ubrukte figurer, dvs. figurer i 'figs' 
mapper som ikke er i bruk i .tex dokumenter.

Created on Sat Jan 27 12:04:48 2018

@author: tommy
"""

import os

FIG_FOLDER_NAMES = {'figs', 'figures', 'figurer'}
FIG_FILETYPES = {'.pdf', '.jpeg', '.jpg', '.png', '.tif'}

def clean(dirpath, dirnames, filenames):
    """
    Delete unused figure files. A file is unused if it's not found
    in the tex source code.
    """
    
    # Retrieve all the TeX code written in this directory
    tex_code = ''
    for filename in filenames:
        _, ext = os.path.splitext(filename)
        if ext != '.tex':
            continue
        tex_file_full = os.path.join(dirpath, filename)
        tex_code += ''.join(line for line in open(tex_file_full, 'r'))
    
    # Go through every directory name
    for dirname in dirnames:
        
        # Skip if it's not a figure directory
        if dirname.lower() not in FIG_FOLDER_NAMES:
            continue
        
        # Get all the files: ..., oppgave1.pdf, v17_2c_del2.jpg, ...
        full_path = os.path.join(dirpath, dirname)
        files_in_figdir = (f for f in os.listdir(full_path) if 
                     os.path.isfile(os.path.join(full_path, f)))
        
        # If it's a figure file that's not used, delete it
        for file in files_in_figdir:
            filename_no_ext, ext = os.path.splitext(file)
            if (ext in FIG_FILETYPES) and (filename_no_ext not in tex_code):
                os.remove(os.path.join(full_path, file))
                print('Deleted file:', os.path.join(full_path, file))


if __name__ == '__main__':
    # Path of this script
    path_here, _ = os.path.split(os.path.realpath(__file__))
    
    # One directory up from the location of this script
    path_start, _ = os.path.split(path_here)
    
    for dirpath, dirnames, filenames in os.walk(path_start):
        
        # Skip the .git folder
        if '.git' in dirpath:
            continue
        
        # If there's a figure directory, send the main folder to cleanup
        if any(dirname.lower() in FIG_FOLDER_NAMES for dirname in dirnames):
            clean(dirpath, dirnames, filenames)