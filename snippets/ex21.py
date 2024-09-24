#ensure to get the correct bottom and top nodes
bottom_nodes = {n for n, d in B.nodes(data=True) if d["bipartite"] == "plant"}#get nodes with bipartite==0
top_nodes = set(B) - bottom_nodes

#create the randomized version
B_R3=randomization_constant_Kseq_bipart(B,bottom_nodes,top_nodes)

#we need to specify the bottom nodes to get nestedness
bottom_nodesR = {n for n, d in B_R3.nodes(data=True) if d["bipartite"] == "plant"}#get nodes with bipartite==0
eta_R3=nestedness_bipartite(B_R3,bottom_nodesR)
print(eta_R3)