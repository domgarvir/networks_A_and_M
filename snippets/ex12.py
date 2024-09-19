print("1. The aiport with more direct flights is %s (%s)" % (d.idxmax(),G.nodes[d.idxmax()]["name"]))

#I would want to be in the city with an airport closer to more other cites: CLOSENESS
print("2. I would like a house close to %s (%s))" % (closenness.idxmax(),G.nodes[closenness.idxmax()]["name"]))

#It should be places in the place that is acting as a bottleneck in the network, as more people should pass by there
print("3. I would put it in %s (%s)" % (betweenness.idxmax(),G.nodes[betweenness.idxmax()]["name"]))