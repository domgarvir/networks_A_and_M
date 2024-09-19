#from IPython.core.magic import register_cell_magic
#from IPython.display import HTML, display
#import itertools as it
import networkx as nx
import numpy as np
import pandas as pd
import json
from itertools import combinations
import itertools
import random as rnd

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
    
    filename="./data/congress_network/congress_network_data.json"
    f = open(filename)
    data = json.load(f)
    usernameList = data[0]['usernameList']
    node_name_mapping = {str(i): name for i, name in enumerate(usernameList)}
    filename="data/congress_network/congress.edgelist"
    DG=nx.read_edgelist(filename, create_using=nx.DiGraph)
    nx.set_node_attributes(DG, node_name_mapping, 'name')
    
    return DG

def load_physicians_network():
    # Read the edge list

    df = pd.read_csv(
        "./data/moreno_innovation/out.moreno_innovation_innovation",
        sep=" ",
        skiprows=2,
        header=None,
    )
    df = df[[0, 1]]
    df.columns = ["doctor1", "doctor2"]

    G = nx.Graph()
    for row in df.iterrows():
        G.add_edge(row[1]["doctor1"], row[1]["doctor2"])

    return G

def load_physicians_network_D():
    # Read the edge list

    df = pd.read_csv(
        "./data/moreno_innovation/out.moreno_innovation_innovation",
        sep=" ",
        skiprows=2,
        header=None,
    )
    df = df[[0, 1]]
    df.columns = ["doctor1", "doctor2"]

    G = nx.DiGraph()
    for row in df.iterrows():
        G.add_edge(row[1]["doctor1"], row[1]["doctor2"])

    return G

def modularity(G, partition):
    W = sum(G.edges[v, w].get('weight', 1) for v, w in G.edges)
    summation = 0
    for cluster_nodes in partition:
        s_c = sum(G.degree(n, weight='weight') for n in cluster_nodes)
        # Use subgraph to count only internal links
        C = G.subgraph(cluster_nodes)
        W_c = sum(C.edges[v, w].get('weight', 1) for v, w in C.edges)
        summation += W_c - s_c ** 2 / (4 * W)
    
    return summation / W

def girvan_newman_partition(graph, num_partitions=2):
    comp = nx.algorithms.community.girvan_newman(graph)
    
    # Continue splitting until we reach the desired number of partitions
    limited = next(comp)
    while len(limited) < num_partitions:
        limited = next(comp)
    
    # Convert the tuple of lists into a list of sets
    partition = [set(group) for group in limited]
    
    return partition

def invert_dictionary(ini_dict):
    inv_dict = {v: k for k, v in ini_dict.items()}
    return inv_dict

def create_partition_map(partition):
    partition_map = {}
    for idx, cluster_nodes in enumerate(partition):
        for node in cluster_nodes:
            partition_map[node] = idx
    return partition_map

def nestedness2(web):
    # Get the number of rows (SA) and columns (SP)
    SA, SP = web.shape

    # Step 1: Column calculations
    N = web.T@web  # Equivalent of t(web) %*% web
    num = np.copy(N)
    num[np.tril_indices(SP, k=0)] = 0  # Set lower triangle (including diagonal) to 0

    # Calculate denominator
    diag_N = np.diag(N)[:, None]  # Convert diagonal to column vector
    den = np.ones((SP, 1))* diag_N
    den = den @ np.ones((1, SP))
    den=np.minimum(den, den.T)
    den[np.tril_indices(SP, k=0)] = 0  # Set lower triangle (including diagonal) to 0
    
    n1 = np.sum(num)
    n2 = np.sum(den)
    nP = n1 / n2

    # Step 2: Row calculations
    N = web@web.T  # Equivalent of t(web) %*% web
    num = np.copy(N)
    num[np.tril_indices(SA, k=0)] = 0  # Set lower triangle (including diagonal) to 0

    # Calculate denominator
    diag_N = np.diag(N)[:, None]  # Convert diagonal to column vector
    den = np.ones((SA, 1))* diag_N
    den = den @ np.ones((1, SA))
    den=np.minimum(den, den.T)
    den[np.tril_indices(SA, k=0)] = 0  # Set lower triangle (including diagonal) to 0

    n1b=np.sum(num)
    n2b=np.sum(den)
    # Step 3: Final nestedness calculation
    out = (n1 + n1b) / (n2 + n2b)

    return out


def get_nestedness_bipartite(Imat):
#this function takes a incidence matrix I, generates the biadjacency A, and cuantifies nestedness
#tenemos que eliminar las plantas aisladas antes de trabajar con esto
    a=list(Imat.columns)
    p=list(Imat.index)
    n=a + p
    Na=len(a)
    Np=len(p)
    N=Na+Np
    #get overlap (common pathways between nodes)
    
    Oaa=np.matmul(Imat.T,Imat)
    Oaa.columns=a
    Opp=np.matmul(Imat,Imat.T)
    Opp.columns=p
    #A11=0
    #A22=0
    #A12 
    Ka=(Imat/Imat).fillna(0).sum()#degree of Traits
    Kp=(Imat/Imat).fillna(0).sum(axis=1)# degree of language

    k_med=[Ka.mean(),Kp.mean()]
    k2_med=[(pow(Ka,2)).mean(),(pow(Kp,2)).mean()]
    k3_med=[(pow(Ka,3)).mean(),(pow(Kp,3)).mean()]

    #build nestedness matrix
    Overlap=pd.DataFrame(0.,index=n, columns=n).astype(float)
    for a1 in Oaa:
        Overlap.loc[a1,a1]=0
        for a2 in Oaa:
            Overlap.loc[a1,a2]=max(0,Oaa.loc[a1,a2]/(Ka.loc[a1]*Ka.loc[a2]))

    for p1 in Opp:
        Overlap.loc[p1,p1]=0
        for p2 in Opp:
            Overlap.loc[p1,p2]=max(0,Opp.loc[p1,p2]/(Kp.loc[p1]*Kp.loc[p2]))
    
    #average nestedness uncorrected
    nest=Overlap.mean().mean()

    OverlapAA=Overlap.loc[a,a].sum().sum()
    OverlapPP=Overlap.loc[p,p].sum().sum()
    Overlapf=( (OverlapAA/(Na*Na)) + (OverlapPP/(Np*Np)) )/2

    #nestedness configurational
    norm_k=k_med[0]*k_med[1]*(Na+Np)
    nest_conf=( (Na*k2_med[1]) + (Np*k2_med[0])  )/norm_k

    nest=nest/nest_conf
    return nest



def calc_degree_degree_correlations_bipart(Imat):

    a=list(Imat.columns)
    p=list(Imat.index)
    n=a + p
    Na=len(a)
    Np=len(p)
    N=len(N)
    
    N={"A":0,"B":0}
    k_med={"A":0,"B":0}
    k2_med={"A":0,"B":0}
    k3_med={"A":0,"B":0}

    Ka=(Imat/Imat).fillna(0).sum()#degree of Traits
    Kp=(Imat/Imat).fillna(0).sum(axis=1)# degree of language

    N["A"]=Na
    N["B"]=Np
    k_med["A"]=Ka.mean()
    k_med["B"]=Kp.mean()
    k2_med["A"]=(pow(Ka,2)).mean()
    k2_med["B"]=(pow(Kp,2)).mean()
    k3_med["A"]=(pow(Ka,3)).mean()
    k3_med["B"]=(pow(Kp,3)).mean()
    
    # print("-------")
    # print(k_med,k2_med,k3_med,N,node_sets)
    # print("-------")

    L=0
    kikj_med=0
    for nodei in list(Imat.index): #for language
        ki=Kp.loc[nodei]
        for nodej in list(Imat.columns):
            kj=Ka.loc[nodej]
            kikj_med = kikj_med + ki*kj

            L = L + 1

    kikj_med = kikj_med / L
    #print(kikj_med)

    kmed2=(k2_med["A"]*N["A"])/(k_med["A"]*N["B"])
    kmed1=(k2_med["B"]*N["B"])/(k_med["B"]*N["A"])
    k2med2=(k3_med["A"]*N["A"])/(k_med["A"]*N["B"])
    k2med1=(k3_med["B"]*N["B"])/(k_med["B"]*N["A"])


    #r_pearson= ( kikj_med - (pow(k2_med,2)/pow(k_med,2)) )/( (k3_med/k_med) - (pow(k2_med,2)/pow(k_med,2)))

    sigma1 = (((k3_med["A"] * N["A"]) / (k_med["A"] * N["B"])) - (((k2_med["A"] * N["A"]) / (k_med["A"] * N["B"])) * ((k2_med["A"] * N["A"]) / (k_med["A"] * N["B"])))); # Teoria 1

    sigma2 = (((k3_med["B"] * N["B"]) / (k_med["B"] * N["A"])) - (((k2_med["B"] * N["B"]) / (k_med["B"] * N["A"])) * ((k2_med["B"] * N["B"]) / (k_med["B"] * N["A"]))));

    #print(kmed2,kmed1,sigma1,sigma2)

    r_pearson = (kikj_med - (kmed1 * kmed2)) / (np.sqrt(np.fabs(sigma1 * sigma2)));


    return r_pearson, k_med, k2_med, k3_med

# randomization functions fro PK model
def find_presences(input_matrix):
    num_rows, num_cols = input_matrix.shape
    hp = []
    iters = num_rows if num_cols >= num_rows else num_cols
    input_matrix_b = input_matrix if num_cols >= num_rows else np.transpose(input_matrix)
    for r in range(iters):
        hp.append(list(np.where(input_matrix_b[r] == 1)[0]))

    return hp 
def curve_ball(input_matrix, r_hp, num_iterations=-1):
    num_rows, num_cols = input_matrix.shape
    l = range(len(r_hp))
    num_iters = 5*min(num_rows, num_cols) if num_iterations == -1 else num_iterations
    for rep in range(num_iters):
        AB = rnd.sample(l, 2)
        a = AB[0]
        b = AB[1]
        ab = set(r_hp[a])&set(r_hp[b]) # common elements
        l_ab=len(ab)
        l_a=len(r_hp[a])
        l_b=len(r_hp[b])
        if l_ab not in [l_a,l_b]:
            tot=list(set(r_hp[a]+r_hp[b])-ab)
            ab=list(ab)
            rnd.shuffle(tot)
            L=l_a-l_ab
            r_hp[a] = ab+tot[:L]
            r_hp[b] = ab+tot[L:]
    out_mat = np.zeros(input_matrix.shape, dtype='int8') if num_cols >= num_rows else  np.zeros(input_matrix.T.shape, dtype='int8')
    for r in range(min(num_rows, num_cols)):
        out_mat[r, r_hp[r]] = 1
    result = out_mat if num_cols >= num_rows else out_mat.T
    return result

def randomization_constant_PK(web):
    
    r_hp=find_presences(web.values)
    RM=curve_ball(web.values,r_hp) #randomized by curveball
    rnd_web=pd.DataFrame(RM,index=web.index, columns=web.columns)

    return rnd_web

def get_triangle_neighbors(G, node) -> set:
    """
    Return neighbors involved in triangle relationship with node.
    """
    neighbors1 = set(G.neighbors(node))
    triangle_nodes = set()
    for nbr1, nbr2 in combinations(neighbors1, 2):
        if G.has_edge(nbr1, nbr2):
            triangle_nodes.add(nbr1)
            triangle_nodes.add(nbr2)
    return triangle_nodes

def plot_triangle_relations(G, node):
    """
    Plot all triangle relationships for a given node.
    """
    triangle_nbrs = get_triangle_neighbors(G, node)
    triangle_nbrs.add(node)
    nx.draw(G.subgraph(triangle_nbrs), with_labels=True)

def get_open_triangles_neighbors(G, node) -> set:
    """
    Return neighbors involved in open triangle relationships with a node.
    """
    open_triangle_nodes = set()
    neighbors = list(G.neighbors(node))

    for n1, n2 in combinations(neighbors, 2):
        if not G.has_edge(n1, n2):
            open_triangle_nodes.add(n1)
            open_triangle_nodes.add(n2)

    return open_triangle_nodes


def plot_open_triangle_relations(G, node):
    """
    Plot open triangle relationships for a given node.
    """
    open_triangle_nbrs = get_open_triangles_neighbors(G, node)
    open_triangle_nbrs.add(node)
    nx.draw(G.subgraph(open_triangle_nbrs), with_labels=True)
    
def get_MusRank(web, mode="ranking"):
    #beware, it only owkrs with unweighted networks, so all webs go to binary
    bweb=web.loc[(web!=0).any(axis=1)]
    bweb=(bweb/bweb).fillna(0)
    Ilist=bweb.unstack().replace(0, np.nan).dropna(how='all', axis=0)

    animals=bweb.columns
    Na=len(animals)
    plants=bweb.index
    Np=len(plants)

    niterations=1000 #iterations until fixed point

    #initial fitness and complexities to start iteration
    fitness={}
    complexity={}
    f1={}
    f2={}
    c1={}
    c2={}

    #active species:pollinator-fitness    pasive species:plant-complexity
    for a in animals:
        fitness[a]=random.uniform(0, 1)*5
        #complexity[a]=-1.
        f1[a]=1.
        f2[a]=0.

    for p in plants:
        complexity[p]=random.uniform(0, 1)*5
        #fitness[p]=-1.
        c1[p]=1.
        c2[p]=0.

    for i in range(niterations):
        #print(i)
        #get fitness of animals
        fmed=0.
        for a in animals: #calculo el fitness
            p_pals=list(Ilist.xs(a, level='Pollinator_gen_sp').index)
            for p in p_pals:
                f2[a] += complexity[p]
        
            fmed += f2[a]   

        fmed=fmed/Na    

        #get complexity of plants:
        cmed=0.
        for p in plants:
            #print(p)
            a_pals=list(Ilist.xs(p, level='Plant_gen_sp').index)
            for a in a_pals:
                c2[p] += (1./fitness[a])
            c2[p]=(1./c2[p])
            cmed += c2[p]
        cmed=cmed/Np

        for a in animals:
            f1[a]= f2[a]/fmed
            fitness[a]=f1[a]  

        for p in plants: 
            c1[p]=c2[p]/cmed
            complexity[p]=c1[p]    

    #here we should have a meaningfull fitness of animals and complexity of plants.
    #Lets use these values to order animals and plants: pol from more fit to less, plants from les complex to more
    f_dict=pd.Series(fitness)
    c_dict=pd.Series(complexity)

    sorted_animals=f_dict.sort_values(ascending=False).index
    sorted_plants=c_dict.sort_values().index
    #Pweb_sorted=Pweb.reindex(index=plants.index, columns=animals.index)
    if (mode=="ranking"):
        return f_dict,c_dict
    else:
        return web.reindex(index=sorted_plants,columns=sorted_animals)
    return
   
# We define each S* motif as a directed graph in networkx
motifs = {
    'S1': nx.DiGraph([(1,2),(2,3)]),
    'S2': nx.DiGraph([(1,2),(1,3),(2,3)]),
    'S3': nx.DiGraph([(1,2),(2,3),(3,1)]),
    'S4': nx.DiGraph([(1,2),(3,2)]),
    'S5': nx.DiGraph([(1,2),(1,3)])
 }

def mcounter(gr, mo):

    """Counts motifs in a directed graph
    :param gr: A ``DiGraph`` object
    :param mo: A ``dict`` of motifs to count
    :returns: A ``dict`` with the number of each motifs, with the same keys as ``mo``
    This function is actually rather simple. It will extract all 3-grams from
    the original graph, and look for isomorphisms in the motifs contained
    in a dictionary. The returned object is a ``dict`` with the number of
    times each motif was found.::
        >>> print mcounter(gr, mo)
        {'S1': 4, 'S3': 0, 'S2': 1, 'S5': 0, 'S4': 3}
    """
    #This function will take each possible subgraphs of gr of size 3, then
    #compare them to the mo dict using .subgraph() and is_isomorphic
    
    #This line simply creates a dictionary with 0 for all values, and the
    #motif names as keys

    mcount = dict(zip(mo.keys(), list(map(int, np.zeros(len(mo))))))
    nodes = gr.nodes()

    #We use iterools.product to have all combinations of three nodes in the
    #original graph. Then we filter combinations with non-unique nodes, because
    #the motifs do not account for self-consumption.

    triplets = list(itertools.product(*[nodes, nodes, nodes]))
    triplets = [trip for trip in triplets if len(list(set(trip))) == 3]
    triplets = map(list, map(np.sort, triplets))
    u_triplets = []
    [u_triplets.append(trip) for trip in triplets if not u_triplets.count(trip)]

    #The for each each of the triplets, we (i) take its subgraph, and compare
    #it to all fo the possible motifs

    for trip in u_triplets:
        sub_gr = gr.subgraph(trip)
        mot_match = map(lambda mot_id: nx.is_isomorphic(sub_gr, mo[mot_id]), motifs.keys())
        match_keys = [mo.keys()[i] for i in xrange(len(mo)) if mot_match[i]]
        if len(match_keys) == 1:
            mcount[match_keys[0]] += 1

    return mcount