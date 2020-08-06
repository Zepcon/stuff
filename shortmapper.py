import sys
import plistlib

'''
Goal: To use my text replacements from macos under windows with Autohotkey.
Call this program with the plist file to get the according autohotkey file.
'''

tip = '''In order to use your original shortcut, you have to type two space behind your shortcut to get the replacement. Otherwise there would not be any possibility to escape the replacement.\n'''

try:
    if (isinstance(sys.argv[1],str)):
        try:
            with open(sys.argv[1], "rb") as pfile:
                pl = plistlib.load(pfile)
                newfile = open("hotkeyfile.ahk", "w+")
                newfile.write("MsgBox, " + tip)
                for short in pl:
                    try:
                        newfile.write("::"+short["shortcut"]+"::"+short["phrase"]+"\n")
                    except Exception:
                        print("Could not parse shortcut: "+ short["shortcut"])
                        pass
                newfile.close()
                print("Success! Saved file as: hotkeyfile.ahk")
        except:
            print("File not found or wrong file.")
            quit()
except:
        print("Fail, enter filename of .plist file when calling the program.")
        quit()

