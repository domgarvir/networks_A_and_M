C = G.copy()
N = G.number_of_nodes()

#lets start with betweeness
ordered_nodes=list(betweenness.index)

B_attack_core_proportions = []
i=0
for nodes_removed in num_nodes_removed:
    # Measure the relative size of the network core
    core = max(nx.connected_components(C), key=len)
    core_proportion = len(core) / N
    B_attack_core_proportions.append(core_proportion)

    # If there are more than M nodes, select top M nodes and remove them
    if C.number_of_nodes() > M:
        nodes_to_remove = ordered_nodes[i:i+M]
        C.remove_nodes_from(nodes_to_remove)
        i += M
        
################3
C = G.copy()
ordered_nodes=list(closenness.index)

C_attack_core_proportions = []
i=0
for nodes_removed in num_nodes_removed:
    # Measure the relative size of the network core
    core = max(nx.connected_components(C), key=len)
    core_proportion = len(core) / N
    C_attack_core_proportions.append(core_proportion)

    # If there are more than M nodes, select top M nodes and remove them
    if C.number_of_nodes() > M:
        nodes_to_remove = ordered_nodes[i:i+M]
        C.remove_nodes_from(nodes_to_remove)
        i += M

################3
C = G.copy()
ordered_nodes=list(d.index)

D_attack_core_proportions = []
i=0
for nodes_removed in num_nodes_removed:
    # Measure the relative size of the network core
    core = max(nx.connected_components(C), key=len)
    core_proportion = len(core) / N
    D_attack_core_proportions.append(core_proportion)

    # If there are more than M nodes, select top M nodes and remove them
    if C.number_of_nodes() > M:
        nodes_to_remove = ordered_nodes[i:i+M]
        C.remove_nodes_from(nodes_to_remove)
        i += M

plt.title('Random failure vs. targeted attack')
plt.xlabel('Number of nodes removed')
plt.ylabel('Proportion of nodes in core')
plt.plot(num_nodes_removed, random_attack_core_proportions, marker='o', label='Failures')
plt.plot(num_nodes_removed, B_attack_core_proportions, marker='^', label='B Attacks')
plt.plot(num_nodes_removed, C_attack_core_proportions, marker='^', label='C Attacks')
plt.plot(num_nodes_removed, D_attack_core_proportions, marker='^', label='D Attacks')
plt.legend()