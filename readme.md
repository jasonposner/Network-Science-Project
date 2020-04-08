# Music Collaboration Network

Credit to @kcmillersean for his 'Hot Stuff' Billboard dataset. It can be found
here: https://data.world/kcmillersean/billboard-hot-100-1958-2017/workspace/project-summary?agentid=kcmillersean&datasetid=billboard-hot-100-1958-2017.

We hit that database with this SQL query to fetch a column of sorted,
unique performers:

SELECT DISTINCT hot_stuff_2.performer
FROM hot_stuff_2
ORDER BY hot_stuff_2.performer

Performers.csv has the resulting data.

Then, we manually decided whether or not two artists were collaborating or if they were a band by looking at their name and deciding which would be most reasonable. We looked for keywords such as "with", "and", "featuring" and "/". Since many band names use "and" and "," (ex: Earth, Wind and Fire") we had to solve this when later inputting our data into the music network portion of our project.

After that, we wrote "collaborator_writer.py", which looks at performers.csv and fetches only rows with "&". We did a tiny bit more "cmd-F" cleaning, followed by writing "ampersand cleaner.py". That script takes the "only_collaborators_raw" data that collaborator_writer gets, and it changes entries like "A & B & C" to "A & B (line break) A & C".

After a bit more tweaking with cmd-F, the final data set was inserted into "FINAL_DATA".
