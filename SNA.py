import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.colors as mcolors
from itertools import islice
import operator
import pylab

def starMaker(N, Nodes, Edges):
    print("Calculation V* and E*, please wait...")
    for i in range(N):
        try:
            tmp=set(Nodes[i+1]) - set(Nodes[i])
            tmp2=set(Edges[i+1]) - set(Edges[i])
            Vstar.append(set(Nodes[i]) - set(tmp)) #find the common values
            Estar.append(set(Edges[i]) - set(tmp2)) #find the common values
            continue
        except:
            break
    return Vstar, Estar


def graphHistogram(j, G):
    print("Calculating centralities, please wait...")
    if G != set():
        nx.draw(G)
        plt.title("Subgraph")
        plt.savefig('subgraph%d' %j)
        plt.clf()
        plt.hist(list(nx.degree_centrality(G).values()))
        plt.title('Degree Centrality')
        plt.savefig('Degree%d' %j)
        plt.clf()
        plt.hist(list(nx.in_degree_centrality(G).values()))
        plt.title('In Degree Centrality')
        plt.savefig('InDegree%d' %j)
        plt.clf()
        plt.hist(list(nx.out_degree_centrality(G).values()))
        plt.title('Out Degree Centrality')
        plt.savefig('OutDegree%d' %j)
        plt.clf()
        plt.hist(list(nx.closeness_centrality(G).values()))
        plt.title('Closeness Centrality')
        plt.savefig('Closeness%d' %j)
        plt.clf()
        plt.hist(list(nx.betweenness_centrality(G).values()))
        plt.title('Betweeness Centrality')
        plt.savefig('Betweeness%d' %j)
        plt.clf()
        plt.hist(list(nx.eigenvector_centrality_numpy(G).values()))
        plt.title('Eigenvector Centrality')
        plt.savefig('Eigenvector%d' %j)
        plt.clf()
        plt.hist(list(nx.katz_centrality(G).values()))
        plt.title('Katz Centrality')
        plt.savefig('Katz%d' %j)
        plt.clf()
    print("The centralities have been extracted as .png files in the same folder where the program is.")

def similarities(G, Estar):
    temp_nodes = list(G.nodes)
    temp_gd = {}
    temp_cn = {}
    G = G.to_undirected() #the above functions aren't working with directed kind of graphs
    #find common neighbors in graph G.
    for node1 in temp_nodes:
        for node2 in temp_nodes:
            b = []
            temp1 = nx.common_neighbors(G, node1, node2)
            for p in temp1:
                b.append(p)
            temp_cn[node1, node2] = len(b)
            try:
                a = nx.shortest_path_length(G, node1, node2)
                temp_gd[node1, node2] = a
            except:
                continue
    preds = nx.jaccard_coefficient(G)
    preds1 = nx.adamic_adar_index(G)
    preds2 = nx.preferential_attachment(G)

    c,d,e = {},{},{}
    for u, v, p in preds:
        c[u,v] = p
    for u, v, p in preds1:
        d[u,v]=p
    for u, v, p in preds2:
        e[u,v]=p

    a = temp_gd
    b = temp_cn
    p1,p2,p3,p4,p5 = -1, -1, -1, -1, -1
    while(p1<0 or p1>=1 or p2<0 or p2>=1 or p3<0 or p3>=1 or p4<0 or p4>=1 or p5<0 or p5>=1):
        p1=float(input("Give p1.Make sure it is greater than 0 and less or equal to 1.\n"))
        p2=float(input("Give p2.Make sure it is greater than 0 and less or equal to 1.\n"))
        p3=float(input("Give p3.Make sure it is greater than 0 and less or equal to 1.\n"))
        p4=float(input("Give p4.Make sure it is greater than 0 and less or equal to 1.\n"))
        p5=float(input("Give p5.Make sure it is greater than 0 and less or equal to 1.\n"))

    predictions(p1,a,Estar, 'graph distance')
    predictions(p2,b,Estar, 'common neighbors')
    predictions(p3,c,Estar, 'jaccard coefficient')
    predictions(p4,d,Estar, 'adamic adar')
    predictions(p5,e,Estar, 'preferential attachment')

def predictions(p,s,E, name):
    s = {key:val for key, val in s.items() if val != 0}
    s = sorted(s.items(), key=lambda kv: kv[1])
    temp1 = int(round(p * len(s)))
    temp_values, temp_total_elmnts = list(islice(s,temp1,None)), len(s)-temp1
    temp_count = 0
    temp_values  = [x[0] for x in temp_values]
    for i in range(temp_total_elmnts):
        if (temp_values[i]) in (list(E)):
            temp_count += 1
    try:
        temp_success_rate = (temp_count / float(temp_total_elmnts)) * 100
        print ("Success rate for", name, "is: ",temp_success_rate, "%")

    except:
        print ("Cannot divide with 0")



#get the data from the txt file
print("Getting data from txt file, please wait...")
data=pd.read_csv("text2.txt", sep=" ", header= None, low_memory=False)
data.columns = ["source", "target", "timestamp"]
tmax=data['timestamp'].max()
tmin=data['timestamp'].min()
print("Minimum time: ",tmin,"\nMaximum time:", tmax)
N=-1
while(int(N)<2):
    N=input("Give the number of the subsets. Be sure that the number is >= 2.\n")
N=int(N)
print("Calculating D, dt, t, Tau...please wait...")

DeltaT=tmax-tmin
dt=DeltaT/N
t, Tau = [], []

for j in range(N+1):
    t.append(tmin+j*dt)
for j in range(1, N+1):
    Tau.append([t[j-1], t[j]])

Graphs, Estar, Vstar, Nodes, Edges = [], [], [], [] ,[]
print("We will cut the graph G into ", N, "equal subgraphs.")
for j in range (N): #+1 to get the last item from Tau
    print("Time is from: ", Tau[j][0], " seconds, to :", Tau[j][1], "seconds.")
    print("A new subgraph is making...")
    G=nx.DiGraph() #initialize an empty graph
    start=Tau[j][0] #start time
    end=Tau[j][1] #end time
    for index, row in data.iterrows():
        if (row.timestamp>=start and row.timestamp<=int(end)):
            G.add_node(row.source)
            G.add_node(row.target)
            G.add_edge(row.source, row.target)
    G.remove_edges_from(G.selfloop_edges()) #removes selfloops
    graphHistogram(j, G) #calculating centralities
    Nodes.append(G.nodes)#make Nodes array
    Edges.append(G.edges)#make Edges array
    starMaker(j, Nodes, Edges) #make Estar, Vstar

print("Calculating predictions...please wait...")
for i in range (N-1):
    if Estar[i] != set():
        similarities(G, Estar[i])
