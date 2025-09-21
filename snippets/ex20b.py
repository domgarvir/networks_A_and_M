Ka_R2=pd.Series(dict(B_R2.degree(animal_nodes))).sort_values(ascending=False)
#2.B build the histograms - lesson2A.24
bins = np.arange(min(Ka.min(),Ka_R1.min(),Ka_R2.min()), max( Ka.max(),Ka_R1.max(),Ka_R2.min()) + 2, 1)#fix width of bin to 1
hist, bin_edges = np.histogram(Ka, bins=bins)
histr1, bin_edges = np.histogram(Ka_R1, bins=bins)
histr2, bin_edges = np.histogram(Ka_R2, bins=bins)

plt.plot(bin_edges[:-1],histr1,'o-',color="r",alpha=0.3,label="GNL")
plt.plot(bin_edges[:-1],hist,'x-',color="k",alpha=0.3,label="Empirical")
plt.plot(bin_edges[:-1],histr2,'o-',color="b",alpha=0.3,label="Gconf")
plt.title("Degree distribution")
plt.xlabel("Degree of node (K)")
plt.ylabel("Number of nodes with degree K")
plt.legend()
plt.show()

#Compute the cumulative sum, but in reverse order to count values greater than or equal
cumulative_hist = np.cumsum(hist[::-1])[::-1]
cumulative_histr1 = np.cumsum(histr1[::-1])[::-1]
cumulative_histr2 = np.cumsum(histr2[::-1])[::-1]

#plot
plt.plot(bin_edges[:-1], cumulative_hist, 'x',color="k",alpha=0.3,label="Empirical")
plt.plot(bin_edges[:-1], cumulative_histr1, 'o',color="r",alpha=0.3,label="GNL")
plt.plot(bin_edges[:-1], cumulative_histr2, 'o',color="b",alpha=0.3,label="Gconf")
plt.xscale('log')
plt.yscale('log')
plt.title("Cumulative degree distribution of empirical (black) and random (red) network")
plt.xlabel("Degree of node (K)")
plt.ylabel("Number of nodes with degree K or more") #
plt.legend()
plt.show()