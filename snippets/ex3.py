MDG = nx.MultiDiGraph()

train_edges=[("Sevilla", "Madrid", 1500), 
             ("Sevilla", "Barcelona", 100),
             ("Madrid", "Sevilla", 200),
             ("Barcelona", "Sevilla", 600),
             ("Madrid", "Barcelona",5000),
             ("Barcelona","Madrid",4000)]

plane_edges=[("Sevilla", "Madrid", 500), 
             ("Sevilla", "Barcelona", 100),
             ("Madrid", "Sevilla", 500),
             ("Barcelona", "Sevilla", 1000),
             ("Madrid", "Barcelona",3000),
             ("Barcelona","Madrid",3000)]

car_edges=[("Sevilla", "Madrid", 3000), 
             ("Sevilla", "Barcelona", 150),
             ("Madrid", "Sevilla", 1500),
             ("Barcelona", "Sevilla", 20),
             ("Madrid", "Barcelona",200),
             ("Barcelona","Madrid",1000)]


MDG.add_weighted_edges_from(train_edges, transport="train")
MDG.add_weighted_edges_from(plane_edges, transport="plane")
MDG.add_weighted_edges_from(car_edges, transport="car")

## Additionally we can also plot it
#pos = nx.spring_layout(MDG)
#nx.draw_networkx_nodes(MDG, pos)
#nx.draw_networkx_labels(MDG, pos)

#rad_dict={"car":0.1,"train":0.2,"plane":0.3}
#color_dict={"train":'#ff6666',"plane":'#ff9900',"car":'#00cc99'}

#for edge in MDG.edges(data=True):
 #   #print(edge)
  #  #print(edge[2]["transport"])
   # #print(edge[2]["weight"])
    #rad=rad_dict[edge[2]["transport"]]
    #color=color_dict[edge[2]["transport"]]
    #w=np.log(edge[2]["weight"]/50)
    #nx.draw_networkx_edges(G, pos, edgelist=[(edge[0],edge[1])], connectionstyle=f'arc3, rad = {rad}',edge_color=color,width=w)