import subprocess
import modules
import modules.util

def connect():
    try:
        subprocess.check_output("adb tcpip 5555", shell=True)
    except:
        modules.util.error("adb command failed")
        return
    modules.util.info("restarting in tcpip")

    modules.util.await_device()
    ip_output = [line for line in subprocess.check_output("adb shell ip addr show wlan0", shell=True).decode("utf-8").split("\n") if "inet " in line][0]
    ip = ip_output.lstrip("inet ").split("/")[0]
    modules.util.info(f"device ip: {ip}")
    subprocess.run(f"adb connect {ip}:5555", shell=True)
    modules.util.success("wifi bridge established")

