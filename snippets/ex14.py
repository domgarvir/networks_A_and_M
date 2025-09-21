#1) Is it possible to travel from any airport in the US to any other airport in the US, possibly using connecting flights? 
print("it is %s that you can go from any airport to any other!" % nx.is_connected(G))

#2) How many airports are in the component with less nodes?
components = list(nx.connected_components(G))
print("There are %s components" % len(components))
for component in components:
    print("there are %s elements in this component" % len(component))

    #plus: color by component   
# Create a dictionary to map each node to its component index
node_colors = {}
for i, component in enumerate(components):
    for node in component:
        node_colors[node] = i  # Assign component index as color

# Extract color list for each node in the graph
color_map = [node_colors[node] for node in G.nodes()]

# Plot the graph
plt.figure(figsize=(8, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos,node_color=color_map, with_labels=True, cmap=plt.get_cmap('Set3'), node_size=50)
plt.show()