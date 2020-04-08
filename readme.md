# Music Collaboration Network

## Credit
Thanks @kcmillersean for the 'Hot Stuff' Billboard dataset. It can be found
here: https://data.world/kcmillersean/billboard-hot-100-1958-2017/workspace/project-summary?agentid=kcmillersean&datasetid=billboard-hot-100-1958-2017.

## Process

### SQL
We hit the above database with:

```SQL
SELECT DISTINCT hot_stuff_2.performer
FROM hot_stuff_2
ORDER BY hot_stuff_2.performer
```

And we downloaded the resulting data as "performers.csv"

### Manual Checks
Unfortunately, lots of bands have collaborative keywords in them.

- Earth, Wind & Fire
- The Wing And A Prayer Fife & Drum Corps

And sometimes, groups like these collaborate with others...
- Earth, Wind & Fire & The Emotions

Should be...

- (Earth, Wind & Fire) & The Emotions

This made it hard to have python do absolutely all the work when we decided to split the artists into main and sub. We manually sorted through many bands, deciding which were names and which were collaborations.

### Python Scripting

#### Collaborator_Writer.py
Removes all artists who did not have "&" in their row. Before running this, we also replaced popular collaborative keywords like "with" and "feat." with the keyletter "&". This narrowed our data set from 9,675 rows to 3,102. The output can be found in "only_collaborators_raw"

#### Ampersand_Cleaner.py
Transforms a row with many features into many rows with one feature per row. This scripting step was done to make the __music_network.py__ implementation easier. After one last run through of the keyword "and", we saved this data in the "FINAL_DATA" folder. The results can be seen in the "FINAL_DATA" folder. This step expanded our rows from 3,102 to 3,967.

#### Duplicate_Remover.py
We noticed that even though we created a list of unique artists, some were still repeating. This is due to the trailing whitespace and tabs that were entered in the "ampersand cleaner" step. We used the regular expression
```
[ \t]+$
```
in the text editor Atom to remove that white space. Then we ran duplicate_remover on the formatted set. This step reduced our rows from 3,967 to 3,727.
