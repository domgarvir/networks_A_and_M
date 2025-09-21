# Set size of each community
community_sizes = [25, 25, 25,25]
community_probs =  np.array([[0.502, 0.005, 0.002,0.0], 
                             [0.005, 0.6, 0.05,0.0], 
                             [0.002, 0.05, 0.5,0.05],
                             [0.0 , 0.0 , 0.05, 0.5]])

net4=nx.stochastic_block_model(community_sizes, community_probs*0.6) #SBM
partition = nx.community.louvain_communities(net4)
best_partition_map = create_partition_map(partition)
node_colors = [best_partition_map[n] for n in net4.nodes()]
nx.draw(net4,with_labels=False, node_color=node_colors)

##########################################

G=net4
group_state_dict={0:'A', 1:'B', 2:'C', 3:'D'}
def initial_state_polarized(G, group_state_dict, best_partition_map):
    state = {}
    for node in G.nodes:
        state[node] = group_state_dict[best_partition_map[node]]
    return state
#########################################
test_state = initial_state_polarized(G,group_state_dict, best_partition_map)
sim = Simulation(G, test_state, state_transition, stop_condition, name='Voter model')
sim.draw()
sim.run(200)