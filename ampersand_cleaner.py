# uses the "only_collaborators" data set and changes
# FROM: A & B & C & D
# TO: A & B
#     A & C
#     A & D

import csv

formattedRows = []

# counts number of ampersands in string.
def ampersandCounter(content):
    index = 0
    counter = 0
    while index < len(content):
        if "&" == content[index]:
            counter += 1
        index += 1
    return counter


# first artist
def findMainArtist(content):
    index = 0
    counter = 0
    while index < len(content):
        if "&" == content[index]:
            # return start to & - 1 (because it's always ' & ')
            return content[0:index-1]
        index += 1

# from A & B & C to A & B \n A & C
# can only run when there are 2 or more ampers
def chunkify(content):
    if ampersandCounter(content) < 2:
        return
    # prepare list of correct rows
    rows = []
    main = findMainArtist(content)
    sub = ""
    # skip through main artist's name and " & "
    content = content[len(main) + 3:]
    index = 0
    start = 0
    end = 0
    while index < len(content):
        if "&" == content[index]:
            # add previous
            sub = content[start:end]
            rows.append(main + " & " + sub)
            # skip through -> "& "
            index += 2
            # reset start/end
            start = index
            end = index
            # any ampers left? if no, add and finish
            if ampersandCounter(content[index:]) == 0:
                sub = content[index:]
                rows.append(main + " & " + sub)
                return rows
        else:
            end += 1
            index += 1

with open('only_collaborators_raw.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\n', quotechar='|')
    for row in spamreader:
        # fetch row-string to be formatted
        s = row[0]
        # count number of " & " (features)
        numOfAmper = ampersandCounter(s)
        # split if there's more than 1 amper
        if numOfAmper >= 2:
            r = chunkify(s)
            for item in r:
                formattedRows.append(item)
        # append row otherwise
        else:
            formattedRows.append(s)

formattedRows.sort()

with open('only_collaborators_formatted.csv', 'w', newline='\n') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='\n')
    spamwriter.writerow(formattedRows)

# def tester():
    # print(ampersandCounter("112 & The Notorious B.I.G. & Big Dad"))
    # print(findMainArtist("112 & The Notorious B.I.G. & Big Dad"))
    # r = chunkify("MVC & DB FZ & KI & GBVS & UNICLR")
    # for item in r: print(item)


# tester()
