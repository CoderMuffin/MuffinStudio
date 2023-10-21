import subprocess
import modules.project
import modules.util
import sys
import re
import time

def run_project():
    project = modules.project.find_project()
    if project is None:
        modules.util.error("Could not find any projects in parent directories")
        exit()

    id = modules.util.app_id(project)
    
    if not "--no-build" in sys.argv:
        modules.util.info(f"Compiling app id {id}")
        gradle = subprocess.run(modules.util.gradle_script() + " installDebug", shell=True)
        if gradle.returncode != 0:
            modules.util.error(f"Could not start, gradle build failed")
            exit()
    
    subprocess.run(f"adb shell am start {id}/.MainActivity", shell=True)
    attach_debug(id)

def get_pid(id):
    return subprocess.Popen(f"adb shell pidof -s {id}", shell=True, stdout=subprocess.PIPE, text=True).stdout.readline()

def attach_debug(id):
    modules.util.info(f"Debugging app id {id}")
    pid = get_pid(id)
    while pid == "":
        modules.util.warn("Bad pid, retrying (maybe app didn't start?)")
        time.sleep(1)
        pid = get_pid(id)

    modules.util.info(f"App pid={pid}")
    log_process = subprocess.Popen("adb logcat", shell=True, stdout=subprocess.PIPE)
    for line in log_process.stdout:
        line = line.decode("cp1252", errors="replace")
        if pid.strip() in line:
            line = line.replace(" D ", "\033[0;1;34m DEBUG \033[0m") \
                .replace(" W ", "\033[0;1;33m WARN  \033[0m") \
                .replace(" I ", "\033[0;1;32m INFO  \033[0m") \
                .replace(" V ", "\033[0;1;35m VERB  \033[0m") \
                .replace(" E ", "\033[0;1;31m ERROR \033[0m")
            line = re.sub(
                r"\d+-\d+\s+(\d+):(\d+):(\d+).\d+",
                r"\1:\2:\3\033[0;2m",
                line
            )
            print(line, end="")

