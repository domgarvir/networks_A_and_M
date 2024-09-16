city1="IND"
city2="FAI"

f=G.has_edge(city1,city2)
print("It is %s that there is a direct flight between these cities" % f)


short_path=nx.shortest_path(G, city1, city2)

print("The shortest route to go from %s to %s is %s" % (city1,city2,short_path))