""""
Just a little tool to create a longer excel command, personal usage

command is like:
=SUMME('Januar 2019'!M35;'Februar 2019'!M35;'März 2019'!M35;'April 2019'!M35;'Mai 2019'!M35)
"""


def exitCheck(checker):
    if checker in ["e", "exit"]:
        exit()


def getCommand(startMonth, endMonth, startYear, endYear, Field, Command):
    builder = ""
    months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

    if startMonth not in months or endMonth not in months or endYear < 1 or startYear < 1:
        return "Error"

    builder += "=" + Command.upper() + "("
    monthIndex = months.index(startMonth)
    # count months in a year and startyear to endyear
    while startYear != endYear or monthIndex != months.index(endMonth)+1:
        builder += "\'" + months[monthIndex] + " " + str(startYear) + "\'!" + Field + ";"
        monthIndex = monthIndex + 1
        if monthIndex > 12:
            startYear = startYear + 1
            monthIndex = 0
    builder = builder[:-1]  # cut off last semikolon
    builder += ")"
    return builder


while True:
    print("Welcome to ExcelUtils")
    command = input("Enter command: ")
    exitCheck(command)
    field = input("Enter field: ")
    exitCheck(field)
    endYear = int(input("Enter EndYear: "))
    exitCheck(endYear)
    startYear = int(input("Enter StartYear: "))
    exitCheck(startYear)
    endMonth = input("Enter endMonth: ")
    exitCheck(endMonth)
    startMonth = input("Enter startMonth: ")
    exitCheck(startMonth)

    print("Your command is: ")
    print(getCommand(startMonth, endMonth, startYear, endYear, field, command))
