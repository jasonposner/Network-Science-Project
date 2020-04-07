import csv

performerColumn = []

# only fetch the artists
with open('hot_stuff_25.csv', newline='\n') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in spamreader:
         performerColumn.append(row[4])


# filter out repeated appearances
performers = []

for p in performerColumn:
    if p not in performers and p != 'Performer':
        performers.append(p)

# sort performers before we put them in the new csv
performers.sort()
print(performers)
print(performers[1])

# write a csv that contains only performers
with open('performers.csv', 'w', newline='\n') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    index = 0
    while index < len(performers):
        spamwriter.writerow([performers[index]])
        index += 1

# if performers have collaborated, put them in the same row
