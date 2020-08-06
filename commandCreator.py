'''
I really like to hit Win + R and then just type a command to start a file i am using often.
In oder to do this you need to have a batch file with the commands name in the C:\Windows folder.

This tool just creates this batch file with the command name and the Path to the file/ program you want to open.

Example:
    1) I just want to open my Windows Documents by hitting Win + R -> "d" -> enter
    2) "d" is the name of the command
    3) path is just "Dokumente"
    4) Move the created file to "C:\Windows" (admin rights needed) and it should work
'''
def exitChecker(check):
    if check in ["exit","e"]:
        exit()

print("🌫🌫🌫 Welcome to commandCreator! 🌫🌫🌫")
while True:
    cName = input("Please enter the command you want wo create: ")
    exitChecker(cName)
    cPath = input("Please enter the Path of your file/ program: ")
    exitChecker(cName)
    file = open(cName+".bat","a")
    file.write('start \"\" \"'+cPath+'\"')
    file.close()
    print("File saved as "+cName+".bat")
    print("You can move the file to your C:\Windows Folder and start using the command!")
    print("Type (e)xit to leave, anything else to continue.")