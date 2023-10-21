import os, re, zipfile, shutil, subprocess, json
import distutils.dir_util
import urllib.request
import modules.util

PLACEHOLDER = "muffin_studio_app_base"

def download_blueprint(bpt, location):
    if os.path.exists(location) or os.path.exists(location+".zip"):
        modules.util.error(f"Cannot download: location {location} is not empty! Please rename before continuing")
        exit()
    
    modules.util.info("Downloading... 0%", end="\r")
    urllib.request.urlretrieve(f"https://api.github.com/repos/CoderMuffin/MuffinStudio{bpt}AppBase/zipball", location+".zip", reporthook=lambda c, b, s:
        modules.util.info(f"Downloading... {c*b*100//s}%", end="\r"))
    modules.util.success("Downloaded successfully                         ")

    modules.util.info("Unzipping...")
    with zipfile.ZipFile(location+".zip", 'r') as zip_ref:
        zip_ref.extractall(location)
    
    nested = os.listdir(location)[0]
    distutils.dir_util.copy_tree(os.path.join(location, nested), location)
    
    os.remove(location+".zip")
    shutil.rmtree(os.path.join(location, nested))

def new_project():
    name = input("Project name: ")
    if not re.fullmatch("[A-z0-9_]+", name):
        modules.util.error("Project name should only feature letters, numbers and underscores")
        exit()

    bpt = [ "Android", "Compose" ][modules.util.select("Project type:", ["xml", "compose"])]
    
    location = name.lower()

    download_blueprint(bpt, location)

    modules.util.info("Specializing blueprint...")
    modules.util.find_and_replace(os.path.join(location, f"app/src/main/java/com/codermuffin/{PLACEHOLDER}/MainActivity.{'kt' if bpt == 'Compose' else 'java'}"), PLACEHOLDER, name.lower())
    modules.util.find_and_replace(os.path.join(location, "settings.gradle"), PLACEHOLDER, name)
    modules.util.find_and_replace(os.path.join(location, "app/build.gradle"), PLACEHOLDER, name.lower())
    modules.util.find_and_replace(os.path.join(location, "app/src/main/res/values/strings.xml"), PLACEHOLDER, name)
    os.rename(
        os.path.join(location, f"app/src/main/java/com/codermuffin/{PLACEHOLDER}"),
        os.path.join(location, f"app/src/main/java/com/codermuffin", name.lower())
    )

    with open(os.path.join(location, ".muffin_studio"), "x") as f:
        json.dump({ "name": name }, f)
        f.write("\n")

    modules.util.info("Preparing gradle...")
    gradle = modules.util.gradle_script()
    os.chmod(os.path.join(location, gradle), 0o755)
    subprocess.run(gradle + " clean", shell=True, check=True, cwd=location)

    modules.util.success(f"Successfully initialised new project '{name}'")

