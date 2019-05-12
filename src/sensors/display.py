import subprocess

def readControllerDisplay():
    readout = subprocess.check_output('./display.sh', cwd='./display', stderr=subprocess.STDOUT).decode("utf-8")
    readout = readout.replace("-", "0")
    lines = readout.splitlines()

    lines[0] = float(lines[0]) / 10
    lines[1] = float(lines[1]) / 10

    return lines
