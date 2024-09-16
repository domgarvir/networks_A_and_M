# Start by loading the network as we did before
filename="./data/WoL_StMarks/st_marks_Ilist.csv"
Ilist=pd.read_csv(filename, header=None, index_col=None)
Ilist.columns=["source","target","w"]
FW=nx.from_pandas_edgelist(Ilist, edge_attr="w", create_using=nx.DiGraph)

#1 ) - How many species are in the network?
#check and print the number of nodes
S=FW.number_of_nodes()
print("\n1 - The number of species is %s\n" % S)

#2) What is the species that has more predators? (out-degree)
# you can see it as we have seen by writing:
print("Let's see the out_degree of each species")
for sp in FW.nodes():
    print(sp)
    print(FW.out_degree(sp))
    
#However is much better to store all the out-degrees in a series, as we can then work with it
K_out=pd.Series(dict(FW.out_degree()))
K_out.sort_values(ascending=False)
#Let's see how is the series
print("Let's see it store as a series")
print(K_out)
print("\n2 - The species with more predators is %s\n" % (K_out.idxmax()) )

#3) - What is the species that has a more varied diet? (in-degree)
K_in=pd.Series(dict(FW.in_degree()))
print("\n3 - The species with a more varied diet is %s\n" % (K_in.idxmax()))

#4)  - What are the species that prey on the most generalist predator? 
predator=K_in.idxmax()
print("\n4 - The species feeding on the generalist predator are:")
print(list(FW.successors(predator)))