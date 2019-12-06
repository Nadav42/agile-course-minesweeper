import platform
import os

# replace all back slashes with normal slashes
def clean_slashes(fileStr):
    fileStr = str(fileStr)
    fileStr = fileStr.replace("\\\\", "\\")
    fileStr = fileStr.replace("\\", "/")

    return fileStr

# bind to 0.0.0.0 on linux
SHOULD_BIND_ADRESS = False

# if linux then --> SHOULD_BIND_ADRESS = True
if SHOULD_BIND_ADRESS != "Windows" and os.name != "nt":
    SHOULD_BIND_ADRESS = True

SCRIPT_PATH = clean_slashes(os.path.dirname(os.path.realpath(__file__)))
print("SCRIPT_PATH={}".format(SCRIPT_PATH))