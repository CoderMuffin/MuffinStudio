import json
import os

def find_project():
    file_name = ".muffin_studio"
    cur_dir = os.getcwd()
    while True:
        file_list = os.listdir(cur_dir)
        parent_dir = os.path.dirname(cur_dir)
        if file_name in file_list:
            return cur_dir
        else:
            if cur_dir == parent_dir: # (if /)
                return None
            else:
                cur_dir = parent_dir

