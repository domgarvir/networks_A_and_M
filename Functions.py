#from IPython.core.magic import register_cell_magic
#from IPython.display import HTML, display
#import itertools as it
import networkx as nx
import numpy as np
import pandas as pd
import json

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
        dtype="str"
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
       "./data/moreno_crime/ent.moreno_crime_crime.person.sex", 
        header=None,
        dtype="str"
    )
    gender.index += 1
    for n, gender_code in gender.iterrows():
        nodeid = "p{0}".format(n)
        G.nodes[nodeid]["gender"] = gender_code[0]

    return G

def load_LotR_network(book="all"):
    
    #load edges
    if (book=="all"):
        filename="./data/LotR_tables/networks-id-3books.csv"
    elif (book==1):
        filename="./data/LotR_tables/networks-id-volume1.csv"
    elif (book==2):
        filename="./data/LotR_tables/networks-id-volume2.csv"
    elif (book==3):
        filename="./data/LotR_tables/networks-id-volume3.csv"
        
    I_df=pd.read_csv(filename)
    I_df["Weight"]=I_df["Weight"].astype("str")

    #load inforation about the nodes
    filename="./data/LotR_tables/ontologies/ontology.csv"
    People_df=pd.read_csv(filename, sep="\t")

    #Create the network with just the nodes
    characters=People_df.loc[:,"id"] #get the characters, the id of the nodes

    G=nx.Graph() #create network
    G.add_nodes_from(characters) #add nodes
    node_attr = People_df.set_index('id').to_dict('index') #get node_attributes
    nx.set_node_attributes(G, node_attr)#set node attributes

    #get the list oof weighted interactions
    Ilist=list(I_df[["IdSource","IdTarget","Weight"]].to_records(index=False))
    G.add_weighted_edges_from(Ilist)
    
    return G

def load_congress_twitter_network():
    
    filename="data/congress_network/congress_network_data.json"
    f = open(filename)
    data = json.load(f)
    usernameList = data[0]['usernameList']
    node_name_mapping = {str(i): name for i, name in enumerate(usernameList)}
    filename="data/congress_network/congress.edgelist"
    DG=nx.read_edgelist(filename, create_using=nx.DiGraph)
    nx.set_node_attributes(DG, node_name_mapping, 'name')
    
    return DG