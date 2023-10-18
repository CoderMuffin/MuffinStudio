import json
import os

def find_nearest():
    file_name = ".muffin_studio"
    cur_dir = os.getcwd()
    while True:
        file_list = os.listdir(cur_dir)
        parent_dir = os.path.dirname(cur_dir)
        if file_name in file_list:
            return os.path.join(cur_dir, file_name)
        else:
            if cur_dir == parent_dir: # (if /)
                return None
            else:
                cur_dir = parent_dir

