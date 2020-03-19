import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

songs = [ { 'number': 1, 'title' : "Run This Town", 'artists' : {'Kanye West', 'Jay-Z', 'Rihanna'} },
          { 'number': 2, 'title' : "All Of The Lights", 'artists' : {"Kanye West", "Alicia Keys", "John Legend", "Drake", "Fergie", "Kid Cudi", "Rihanna"} } ]

song_colors = { 1: '#c7424a', 2 : '#42b3c7'}

def getArtists(songs):
    toret = set()
    for song in songs:
        for artist in song['artists']:
            toret.add(artist)
    return toret

def hasSongEdge(artist1, artist2, song_num):
    if not G.has_edge(artist1, artist2):
        return False
    for i in range(len(G[artist1][artist2])):
        if G[artist1][artist2][i]['song_num'] == song_num:
            return True
    return False

def initVertices(artists):
    for artist in artists:
        G.add_node(artist)

def initEdges(songs, artists):
    for artist1 in artists:
        for song in songs:
            if artist1 in song['artists']:
                for artist2 in song['artists']:
                    if (artist1 != artist2
                        and not hasSongEdge(artist1, artist2, song['number'])):
                        G.add_edge(artist1, artist2,
                                    song_num = song['number'])
          
    
#Graph initialization:          
G = nx.MultiGraph()
artists = getArtists(songs)
initVertices(artists)
initEdges(songs, artists)


#Graph Visualization:
layout = nx.spring_layout(G)
nx.draw_networkx_nodes(G, layout, node_size = 100, with_labels = True)
ax = plt.gca()
for e in G.edges:
    song_num = G[e[0]][e[1]][e[2]]['song_num']
    ax.annotate("",
                xy=layout[e[0]], xycoords='data',
                xytext=layout[e[1]], textcoords='data',
                arrowprops=dict(arrowstyle="-", color=song_colors[song_num],
                                alpha = 0.5,
                                shrinkA=5, shrinkB=5,
                                patchA=None, patchB=None,
                                connectionstyle="arc3,rad=rrr".replace('rrr',str(0.3*e[2])
                                ),
                                ),
                )
plt.axis('off')
nx.draw_networkx_labels(G, layout)
song_nums = nx.get_edge_attributes(G, 'song_num')
plt.show()








            
    



