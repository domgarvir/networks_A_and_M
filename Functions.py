#from IPython.core.magic import register_cell_magic
#from IPython.display import HTML, display
import networkx as nx
import numpy as np
import itertools as it


def draw_colored_multigraph(MDG):
    
    ## Additionally we can also plot it
    pos = nx.spring_layout(MDG)
    nx.draw_networkx_nodes(MDG, pos)
    nx.draw_networkx_labels(MDG, pos)

    rad_dict={"car":0.1,"train":0.2,"plane":0.3}
    color_dict={"train":'#ff6666',"plane":'#ff9900',"car":'#00cc99'}

    for edge in MDG.edges(data=True):
        #print(edge)
        #print(edge[2]["transport"])
        #print(edge[2]["weight"])
        rad=rad_dict[edge[2]["transport"]]
        color=color_dict[edge[2]["transport"]]
        w=np.log(edge[2]["weight"]/50)
        nx.draw_networkx_edges(MDG, pos, edgelist=[(edge[0],edge[1])], connectionstyle=f'arc3, rad = {rad}',edge_color=color,width=w)
        
        
#read databases
def load_crime_network():
    df = pd.read_csv(
        "./data/moreno_crime/out.moreno_crime_crime",
        sep=" ",
        skiprows=2,
        header=None,
    )
    df = df[[0, 1]]
    df.columns = ["personID", "crimeID"]
    df.index += 1

    # Read in the role metadata
    roles = pd.read_csv(
        "./data/moreno_crime/rel.moreno_crime_crime.person.role", header=None
    )
    roles.columns = ["roles"]
    roles.index += 1

    # Add the edge data to the graph.
    G = nx.Graph()
    for r, d in df.join(roles).iterrows():
        pid = "p{0}".format(d["personID"])  # pid stands for "Person I.D."
        cid = "c{0}".format(d["crimeID"])  # cid stands for "Crime I.D."
        G.add_node(pid, bipartite="person")
        G.add_node(cid, bipartite="crime")
        G.add_edge(pid, cid, role=d["roles"])

    # Read in the gender metadata
    gender = pd.read_csv(
       "./data/moreno_crime/ent.moreno_crime_crime.person.sex", header=None
    )
    gender.index += 1
    for n, gender_code in gender.iterrows():
        nodeid = "p{0}".format(n)
        G.nodes[nodeid]["gender"] = gender_code[0]

    return G