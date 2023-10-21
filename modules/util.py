import platform
import subprocess
import os

def find_and_replace(file_path, old_text, new_text):
    with open(file_path, 'r') as file:
        content = file.read()
    modified_content = content.replace(old_text, new_text)
    with open(file_path, 'w') as file:
        file.write(modified_content)

def gradle_script():
    return "gradlew.bat" if platform.system() == "Windows" else "./gradlew"

def app_id(project):
    with open(os.path.join(project, "app", "build.gradle")) as f:
        line = [line for line in f.readlines() if "applicationId" in line][0]
        return line.split('"')[1]

def gradle_version(project):
    gradle = gradle_script()
    process = subprocess.Popen(gradle + " -v", shell=True, cwd=project, stdout=subprocess.PIPE, text=True)
    process.stdout.readline()
    process.stdout.readline()
    return process.stdout.readline().split("Gradle ")[1]

def info(msg, *args, **kwargs):
    print("[\033[34minfo\033[0m]", msg, *args, **kwargs)

def success(msg, *args, **kwargs):
    print("[\033[32m ok \033[0m]", msg, *args, **kwargs)

def warn(msg, *args, **kwargs):
    print("[\033[33mwarn\033[0m]", msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    print("[\033[31merr!\033[0m]", msg, *args, **kwargs)

def select(prompt, opts):
    while True:
        choice = input(prompt + " (" + ", ".join(opts) + ") ")
        if choice in opts:
            return opts.index(choice)

