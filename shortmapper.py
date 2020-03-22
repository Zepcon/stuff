import sys
import plistlib

if (isinstance(sys.argv[1],str)):
    try:
        with open(sys.argv[1], "rb") as pfile:
            pl = plistlib.load(pfile)
            newfile = open("hotkeyfile.ahk", "w+")
            for short in pl:
                try:
                    newfile.write("::"+short["shortcut"]+"::"+short["phrase"]+"\n")
                except Exception:
                    print("Could not parse one of the shortcuts!")
                    pass
            newfile.close()
            print("Success! Saved file as: hotkeyfile.ahk")
    except:
        print("File not found or wrong file")
        quit()
else:
    print("Fail, enter correct filename of existing file")
    quit()

