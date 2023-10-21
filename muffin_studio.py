#!/usr/bin/env python3
import sys
import subprocess
import modules.new
import modules.util
import modules.project
import modules.run

def usage():
    print("usage: muffin_studio <command>")
    print("Commands:")
    for key in cmds:
        print("\t" + key + ": " + cmds[key]["desc"])

def debug():
    subprocess.run(modules.util.gradle_script() + " installDebug")
    subprocess.run("adb") 

def find_project():
    dir = modules.project.find_project()
    if dir is not None:
        modules.util.success(f"Found project in directory '{dir}'")
    else:
        modules.util.error("Could not find any projects nearby")

def attach():
    modules.run.attach_debug(modules.util.app_id(modules.project.find_project()))

cmds = {
    "new": { 
        "desc": "Opens the interface to create a new project",
        "cmd": modules.new.new_project
    },
    "project": {
        "desc": "Finds the nearest project",
        "cmd": find_project
    },
    "run": {
        "desc": "Install and run the project on any connected devices. Run with `--no-build` to start debugging on the remote device",
        "cmd": modules.run.run_project
    },
    "attach": {
        "desc": "Read from logcat on the remote device",
        "cmd": attach
    }
}

if len(sys.argv) < 2:
    usage()
    exit()

if not sys.argv[1] in cmds:
    print("Unknown command '" + sys.argv[1] + "'")
    usage()
    exit()

cmds[sys.argv[1]]["cmd"]()

