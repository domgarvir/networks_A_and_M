D = nx.DiGraph()

D.add_edges_from([("plant","snail"),("plant","caterpillar"),("plant","rabbit"),("snail","lizard"),("caterpillar","lizard")])

nx.draw(D, with_labels=True)