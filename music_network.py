import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import csv
import random

# Plot does not support dollar signs
def removeDollarSigns(s):
    toret = ''
    for i in range(len(s)):
        if s[i] == '$':
            toret += 's'
        else:
            toret += s[i]
    return toret

def getData(filename):
    toret = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            toadd = []
            artists = row[0].split('&')
            for artist in artists:
                toadd.append(removeDollarSigns(artist.strip()))
            toret.append(toadd)
    return toret
    
def getRandomHexColor():
    color = "%06x" % random.randint(0, 0xFFFFFF)
    color = '#' + color
    return color

def initSongs(artists):
    songs = []
    for row in artists:
        toadd = dict()
        toadd['artists'] = set(row)
        toadd['color'] = getRandomHexColor()
        songs.append(toadd)
    return songs


def getArtists(songs):
    toret = set()
    for song in songs:
        for artist in song['artists']:
            toret.add(artist)
    toret = list(toret)
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
                    if (artist1 != artist2):
                        G.add_edge(artist1, artist2, song['color'])
          
def getShortestPathLength(artist1, artist2):
    path = nx.shortest_path(artist1, artist2)
    return len(path) - 1 # Don't include the source

def getOutgoingEdges(artist):
    return len(list(G[artist]))

# Gets most outgoing edges of 
def getMostCollaborativeArtist():
    max_edges = 0
    most_collaborative_artist = ''
    for artist in artists:
        if getOutgoingEdges(artist) > max_edges:
            max_edges = getOutgoingEdges(artist)
            most_collaborative_artist = artist
    return (most_collaborative_artist, max_edges)

def testedPairs(u,v, tested_pairs):
    return (u,v) in tested_pairs or (v,u) in tested_pairs

def getShortestPaths(G, u,v):
    # See if we can get a path first
    try:
        path = nx.dijkstra_path(G, u,v)
    except nx.NetworkXNoPath:
        return [] # If not, return an empty list
    # Otherwise return all paths
    return nx.all_shortest_paths(G, u, v)

def getBetweenness(G):
    betweenness = {}
    # Initialize to zero
    for v in G:
        betweenness[v] = 0.0
    # Choose each node as a source, get betweeness(s):
    for s in G:
        b = 0
        tested_pairs = []
        # For all pairs in G which we have not tested:
        for u in G:
            for v in G:
                if u != s and  u != v and s != v and not testedPairs(u,v,tested_pairs):
                    # Get all shortest paths
                    shortest_paths = getShortestPaths(G,u,v)
                    sigma_v = 0 # Paths passing through v
                    sigma = 0 # All paths
                    for p in shortest_paths:
                        if s in p:
                            sigma += 1
                            sigma_v += 1
                        else:
                            sigma += 1
                    if sigma != 0:
                        b += sigma_v / sigma
                    tested_pairs.append((u,v))
        betweenness[s] = b # Add to betweenenss
    betweeness = normalizeValues(betweenness, len(artists)) #Normalize
    return betweenness

def getMaxBetweenness():
    betweenness = getBetweenness(G)
    max_betweenness = 0
    max_betweenness_artist = ''
    for artist in betweenness:
        if betweenness[artist] >= max_betweenness:
            max_betweenness = betweenness[artist]
            max_betweenness_artist = artist
    return (max_betweenness_artist, betweenness[max_betweenness_artist])


def normalizeValues(betweenness, n):
    # number of pairs is our normalization factor
    factor = (n-1) * (n-2) / 2
    factor = 1/ factor
    for v in betweenness:
        betweenness[v] = betweenness[v] * factor
    return betweenness
        
#Graph initialization:          
G = nx.MultiGraph()
collabs = getData('ONLY_COLLABS_FINAL.csv')
songs = initSongs(collabs)[:50]
artists = getArtists(songs)
initVertices(artists)
initEdges(songs, artists)


#Graph Visualization:
layout = nx.spring_layout(G)
nx.draw_networkx_nodes(G, layout, node_size = 10, with_labels = True)
ax = plt.gca()
for e in G.edges:
    edge_color = e[2]
    ax.annotate("",
                xy=layout[e[0]], xycoords='data',
                xytext=layout[e[1]], textcoords='data',
                arrowprops=dict(arrowstyle="-", color=edge_color,
                                alpha = 0.5,
                                shrinkA=5, shrinkB=5,
                                patchA=None, patchB=None,
                                connectionstyle="arc3,rad=rrr".replace('rrr',str(0)
                                ),
                                ),
                )
plt.axis('off')
nx.draw_networkx_labels(G, layout, font_size = 8)
song_nums = nx.get_edge_attributes(G, 'song_num')
plt.show()

