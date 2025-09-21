#2.A Retrieve the degree sequences of polinators
#in te original network I know the animal nodes
Ka=pd.Series(dict(B.degree(animals))).sort_values(ascending=False)
#retrieve animal nodes only #LEsson01A, 24 #LEsson01A, 24
animal_nodes = {n for n, d in B_R1.nodes(data=True) if d["bipartite"] == "animal"}
Ka_R1=pd.Series(dict(B_R1.degree(animal_nodes))).sort_values(ascending=False)
#2.B build the histograms - lesson2A.24
bins = np.arange(min(Ka.min(),Ka_R1.min()), max( Ka.max(),Ka_R1.max()) + 2, 1)#fix width of bin to 1
hist, bin_edges = np.histogram(Ka, bins=bins)
histr, bin_edges = np.histogram(Ka_R1, bins=bins)

plt.plot(bin_edges[:-1],histr,'o-',color="r",alpha=0.3,label="GNL")
plt.plot(bin_edges[:-1],hist,'o-',color="k",alpha=0.3,label="Empirical")
plt.title("Degree distribution")
plt.xlabel("Degree of node (K)")
plt.ylabel("Number of nodes with degree K")
plt.legend()
plt.show()

#Compute the cumulative sum, but in reverse order to count values greater than or equal
cumulative_hist = np.cumsum(hist[::-1])[::-1]
cumulative_histr = np.cumsum(histr[::-1])[::-1]
#plot
plt.plot(bin_edges[:-1], cumulative_hist, 'o',color="k",alpha=0.3,label="Empirical")
plt.plot(bin_edges[:-1], cumulative_histr, 'o',color="r",alpha=0.3,label="GNL")
plt.xscale('log')
plt.yscale('log')
plt.title("Cumulative degree distribution of empirical (black) and random (red) network")
plt.xlabel("Degree of node (K)")
plt.ylabel("Number of nodes with degree K or more") #
plt.legend()
plt.show()