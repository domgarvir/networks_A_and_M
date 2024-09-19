a0='Loxigilla portoricensis '

#load first network
filename="./data/WoL_fugivory/1.csv" 
Idf1=pd.read_csv(filename, header=0, index_col=0)
B1 = nx.Graph()
# Add producers (rows) and consumers (columns) as nodes
plants1 = Idf1.index
animals1 = Idf1.columns
B1.add_nodes_from(plants1, bipartite="plant")  # Set for producers
B1.add_nodes_from(animals1, bipartite="animal")  # Set for consumers
    # Add edges for non-zero interactions, we can also use the matrix directly
for plant in plants1:
    for animal in animals1:
        if Idf1.loc[plant, animal] != 0:
            B1.add_edge(plant, animal)

#second network
filename="./data/WoL_fugivory/2.csv" 
Idf2=pd.read_csv(filename, header=0, index_col=0)
B2 = nx.Graph()
# Add producers (rows) and consumers (columns) as nodes
plants2 = Idf2.index
animals2 = Idf2.columns
B2.add_nodes_from(plants2, bipartite="plant")  # Set for producers
B2.add_nodes_from(animals2, bipartite="animal")  # Set for consumers
# Add edges for non-zero interactions, we can also use the matrix directly
for plant in plants2:
    for animal in animals2:
        if Idf2.loc[plant, animal] != 0:
            B2.add_edge(plant, animal)

#get the degree of the bird in both networks
K1=B1.degree(a0)
K2=B2.degree(a0)

#get the degree centrality on both networks
D1=pd.Series(dict(bipartite.degree_centrality(B1,animals1))).loc[a0]
D2=pd.Series(dict(bipartite.degree_centrality(B2,animals2))).loc[a0]

print("The bird has degrees %s and %s in the 1st and 2nd networks" % (K1,K2))

print("The bird has degree centrality %.2f and %.2f in the 1st and 2nd networks" % (D1,D2))

K1=pd.Series(dict(B1.degree()))
K2=pd.Series(dict(B2.degree()))

bins = np.arange(min( K1.min(),K2.min()), max(K1.max(), K2.max()) + 2, 1)#fix width of bin to 1
hist1, bins= np.histogram(K1, bins=bins)
hist2, bins= np.histogram(K2 ,bins=bins)

cumulative_hist1 = np.cumsum(hist1[::-1])[::-1]
cumulative_hist2 = np.cumsum(hist2[::-1])[::-1]

#plot
plt.plot(bins[:-1], cumulative_hist1, 'o',color="k",alpha=0.3)
plt.plot(bins[:-1], cumulative_hist2, 'o',color="r",alpha=0.3)
plt.xscale('log')
plt.yscale('log')
plt.title("Cumulative degree distribution of frugivore birds")
plt.xlabel("Degree of node (K)")
plt.ylabel("Number of nodes with degree K or more") #
plt.show()