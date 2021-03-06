import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import csv
import random
import itertools

# Note: This program is set to only the first
# 50 entries in the dataset in order
# for the functions to be more
# easily tested

# Plot does not support dollar signs
def removeDollarSigns(s):
    toret = ''
    for i in range(len(s)):
        if s[i] == '$':
            toret += 's'
        else:
            toret += s[i]
    return toret

def formatData(filename):
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

# Assigns each song a unique color
def createColorMap(collabs):
    toret = dict()
    used_colors = set() # Sets have average O(1) "in" lookup
    for i in range(1, len(collabs) + 1):
        # Get an unused hex color
        color = getRandomHexColor()
        while color in used_colors:
            color = getRandomHexColor()
        toret[i] = color
    return toret
        
def initSongs(collabs):
    songs = []
    colors = createColorMap(collabs)
    num = 1
    for row in collabs:
        toadd = dict()
        toadd['artists'] = set(row)
        toadd['color'] = colors[num]
        toadd['song_num'] = num
        songs.append(toadd)
        num += 1
    return songs

def getArtists(songs):
    toret = set()
    for song in songs:
        for artist in song['artists']:
            toret.add(artist)
    toret = list(toret)
    return toret

# Initializes vertices in the graph
def initVertices(artists):
    for artist in artists:
        G.add_node(artist)

#Initialize edges in the graph, given vertices and songs calculated
def initEdges(songs):
    for song in songs:
        # Get each 'pair' of artists in the song's listed artists
        pairs = itertools.combinations(song['artists'], 2)
        # For each pair, add a new edge with unique song color
        for pair in pairs:
            G.add_edge(pair[0], pair[1], song['color'])

# Shortest Path:

def getShortestPathLength(artist1, artist2):
    try:
        return nx.dijkstra_path_length(G, artist1, artist2)
    except nx.NetworkXNoPath:
        return float("inf") # If no paths, return inf

# Degree/Outgoing Edges:

def getOutgoingEdges(artist):
    return len(list(G[artist]))

# Gets most outgoing edges of the graph
def getMostCollaborativeArtist():
    max_edges = 0
    most_collaborative_artist = ''
    for artist in artists:
        if getOutgoingEdges(artist) > max_edges:
            max_edges = getOutgoingEdges(artist)
            most_collaborative_artist = artist
    return (most_collaborative_artist, max_edges)

# Get top n Collaborative Aritsts
def getTopCollaborativeArtists(n):
    d = {}
    for artist in artists:
        d[artist] = getOutgoingEdges(artist)
    keys = sorted(d, key=d.__getitem__)
    keys = keys[-n:]
    toret = {}
    for key in keys:
        toret[key] = d[key]
    return toret

def getNumberOfHits(artist):
    with open('performers.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        hits = 0
        for row in reader:
            tocheck = []
            artists = row[0].split('&')
            for performer in artists:
                tocheck.append(removeDollarSigns(performer.strip()))
            if artist in tocheck:
                hits += 1
        return hits

def getTopNumberOfHits(n):
    d = {}
    for artist in artists:
        d[artist] = getNumberOfHits(artist)
    keys = sorted(d, key=d.__getitem__)
    keys = keys[-n:]
    toret = {}
    for key in keys:
        toret[key] = d[key]
    return toret
            
# Betweenness Centrality:

def getShortestPaths(G, u,v):
    # See if we can get a path first
    try:
        path = nx.dijkstra_path(G, u,v)
    except nx.NetworkXNoPath:
        return [] # If not, return an empty list
    # Otherwise return all paths
    return nx.all_shortest_paths(G, u, v)

# You may test correcteness by using this against the
# nx.betweenness_centrality(G) function already implemented
# by NetworkX (highly recommended to test with <100 nodes)
def getBetweenness(G):
    betweenness = {}
    V = []
    # Initialize to zero
    for v in G:
        betweenness[v] = 0.0
        V.append(v)
    # Choose each node as a source, get betweeness(s):
    for s in G:
        b = 0
        pairs = list(itertools.combinations(list(G.nodes), 2))
        # For all pairs in G which we have not tested:
        for (u,v) in pairs:
                if u != s and  u != v and s != v:
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

# Get n top betweenness artists
def getTopBetweenness(n):
    d = getBetweenness(G)
    keys = sorted(d, key=d.__getitem__)
    keys = keys[-n:]
    toret = {}
    for key in keys:
        toret[key] = d[key]
    return toret

def normalizeValues(betweenness, n):
    # number of pairs is our normalization factor
    factor = (n-1) * (n-2) / 2
    factor = 1/ factor
    for v in betweenness:
        betweenness[v] = betweenness[v] * factor
    return betweenness

# Line graph analysis:

def getBetweennessGraphData(G):
    b = getBetweenness(G)
    x = [] # x-axis (betweenness)
    y = [] # y-axis (# of hits)
    for artist in G:
        x.append(b[artist])
        y.append(getNumberOfHits(artist))
    return x, y

def makeBetweennessGraph(G):
    x, y = getBetweennessGraphData(G)
    plt.plot(x, y, 'ro')
    plt.xlabel("Betweenness Centrality")
    plt.ylabel("Number of Hits")
    plt.show()

def getCollaborationGraphData(G):
    x = [] # x-axis (collaborations)
    y = [] # y-axis (# of hits)
    for artist in G:
        x.append(getOutgoingEdges(artist))
        y.append(getNumberOfHits(artist))
    return x, y

def makeCollaborationGraph(G):
    x, y = getCollaborationGraphData(G)
    plt.plot(x, y, 'ro')
    plt.xlabel("Collaboraitons (degree)")
    plt.ylabel("Number of Hits")
    plt.show()

# Shortest Path Analysis:

# Analyzes "close artists" for the first 50 artists in full graph
# You can adjust this to look at more artist, but the run time
# will increase significantly
def analyzeCloseArtists(G):
    artists = [artists for artists in G]
    artists = artists[:50]
    pairs = itertools.combinations(artists, 2)
    close_artists = []
    for (u,v) in pairs:
        if getShortestPathLength(u,v) <= 3:
            close_artists.append((u,v))
    for pair in close_artists:
        print("Artists: ", pair)
        print("Distance: ", getShortestPathLength(pair[0], pair[1]))
        collabs0 = list(G[pair[0]])
        collabs1 = list(G[pair[0]])
        in_common_collabs = list(set(collabs0) & set(collabs1))
        print("Collaborations in common:", in_common_collabs)
        print()

    
#Graph initialization:

G = nx.MultiGraph()
# To test the code, it is recommended to use only the top 50
# since a greater number of artists leads to very long wait
# times for some of the data:
collabs = formatData('./FINAL_DATA/ONLY_COLLABS_FINAL.csv')[:50]
songs = initSongs(collabs)
artists = getArtists(songs)
initVertices(artists)
initEdges(songs)

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
