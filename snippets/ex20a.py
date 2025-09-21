Ka=pd.Series(dict(B.degree(animals))).sort_values(ascending=False)
Kp=pd.Series(dict(B.degree(plants))).sort_values(ascending=False)
B_R2=bipartite.configuration_model(Kp,Ka)
# to force that the graph uses bipartite="plant" or bipartite="animal" instead of the o and 1 by default we can do:
for n in range(Nplants):
    B_R2.nodes[n]["bipartite"]="plant"
for n in range(Nplants,Nplants+Nanimals):
    B_R2.nodes[n]["bipartite"]="animal"