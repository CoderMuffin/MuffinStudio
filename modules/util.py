import platform

def find_and_replace(file_path, old_text, new_text):
    with open(file_path, 'r') as file:
        content = file.read()
    modified_content = content.replace(old_text, new_text)
    with open(file_path, 'w') as file:
        file.write(modified_content)

def gradle_script():
    return "./gradlew.bat" if platform.system() == "Windows" else "./gradlew"

def info(msg, *args, **kwargs):
    print("[\033[34minfo\033[0m]", msg, *args, **kwargs)

def success(msg, *args, **kwargs):
    print("[\033[32m ok \033[0m]", msg, *args, **kwargs)

def warn(msg, *args, **kwargs):
    print("[\033[33mwarn\033[0m]", msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    print("[\033[31merr!\033[0m]", msg, *args, **kwargs)
    

