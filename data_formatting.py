import csv

performerColumn = []

# only fetch the artists
with open('hot_stuff_complete.csv', newline='\n') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
     for row in spamreader:
         performer = row[4]
         # see if first char is a space
         if performer[0] == ' ':
             index = 0
             # iterate through string to find first char
             while(index < len(performer)):
                if performer[index] != ' ':
                    # redefine performer to not include first space
                    performer = performer[index:]
                    break
                index += 1
         performerColumn.append(performer)

# filter out repeated appearances
performers = []

# for p in performerColumn:
#     if p not in performers and p != 'Performer':
#         performers.append(p)

# sort performers before we put them in the new csv
# performers.sort()
#
# # write a csv that contains only performers
# with open('performers.csv', 'w', newline='\n') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=',')
#     index = 0
#     while index < len(performers):
#         spamwriter.writerow([performers[index]])
#         index += 1

# if performers have collaborated, put them in the same row

# for p in performers:
#     if "Feat." in p or "feat." in p or "Featuring" in p:
#         print(p)
