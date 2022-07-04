import vdf
import sys
from pathlib import Path
import subprocess

folders = []
libraryfolders = vdf.load(open(sys.argv[1] + 'steam/steamapps/libraryfolders.vdf'))
for value, key in libraryfolders["libraryfolders"].items():
    folders.append(Path(key["path"]))

appNames = []
appIds = []
for appFolder in folders:
    manifests = appFolder.glob("steamapps/appmanifest_*.acf")
    for manifest in manifests:
        manifest = vdf.load(open(manifest))
        appNames.append(manifest["AppState"]["name"])
        appIds.append(manifest["AppState"]["appid"])

args = ["yad", "--list", "--no-headers", "--center",
            "--window-icon", "wine",
            "--no-markup",
            "--search-column", "2",
            "--print-column", "2",
            "--width", "600", "--height", "400",
            "--text", "Select a game",
            "--title", "Cheat engine helper",
            "--column", "Steam app"]

cmd_input = [
    "{}: {}".format(appNames[i], appIds[i])
    for i, value in enumerate(appNames)
]
result = subprocess.run (args, input="\n".join(cmd_input).encode("utf-8"), stdout=subprocess.PIPE)
choice = result.stdout
if choice in (b"", b" \n"):
    sys.exit(-1)

id = str(choice).rsplit(": ")[-1]
id = "".join(x for x in id if x.isdigit())
print (id)
sys.exit(0)
