#start by determining the two types of nodes
person_nodes = {n for n, d in G.nodes(data=True) if d["bipartite"] == 'person'}
crime_nodes = set(G) - person_nodes

#get the degree of people and of crimes
K_person=pd.Series(dict(G.degree(person_nodes)))
K_crime=pd.Series(dict(G.degree(crime_nodes)))

#Get the person linked to most crimes
most_dangerous_person=K_person.idxmax()
number_of_crimes=G.degree(most_dangerous_person)

print("\n1- the most dangerous person is %s, involved in %s crimes" % (most_dangerous_person,number_of_crimes))

#look the role: We need to go over the EDGES of the person with all the crimes, and for each of retrieve the word inside the attribute "role. We then store them in a list called Roles
Roles=[]
for c, p, r in G.edges(most_dangerous_person, data=True):
    print(c, p, r["role"])
    Role=r["role"]
    Roles.append(Role)

#transform the list of roles in a dictionary containig how many times they appear
from collections import Counter
counts = dict(Counter(Roles))
print(counts)

print("\n2- The person appears:")
for key in counts:
    print("%s times as %s" % (counts[key],key))
    
#look for the crime with more people involved (higer degree)    
print 
most_trending_crime=K_crime.idxmax()
number_of_people_involved=G.degree(most_trending_crime)

print("\n3- The most common crime is %s, that got %s poeple involved" % (most_trending_crime,number_of_people_involved))


# What persons have more shared crimes in common?
# do the unipartite projection on people: weghts give the number of shared crimes!
people_projection = nx.bipartite.weighted_projected_graph(G, person_nodes)
#pass it to edgelist, so we can order by weigth!
shared_df=nx.to_pandas_edgelist(people_projection,source='person1',target='person2')
print("\n4- The persons with more shared crimes are:")
print(shared_df.sort_values(by="weight",ascending=False).head(5))

#To obtain the graph of the network
#pos = nx.spring_layout(G) #assing position to the nodes acoording to their bipartite property
#color_dict={"person":"red","crime":"blue"} #dictionary of node color, each bipartite set is asociated to a different color
#colors = [color_dict[node[1]['bipartite']] for node in G.nodes(data=True)]
#nx.draw(G, pos, node_color=colors, with_labels=False,node_size=20)