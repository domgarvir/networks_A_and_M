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
from scipy.optimize import curve_fit,  fsolve
from scipy.stats import mvn

# Suppress FutureWarning messages
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

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

def nestedness(G):
    
    web=nx.to_pandas_adjacency(G)
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

def nestedness_bipartite(B,bottom_nodes):
    #get matrix representation (incidence)
    top_nodes = set(B) - bottom_nodes
    web=nx.to_pandas_adjacency(B).loc[list(top_nodes), list(bottom_nodes)]
    
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


def mcounter_py3(gr, mo):
    """
    Counts motifs in a directed graph
    :param gr: A ``DiGraph`` object
    :param mo: A ``dict`` of motifs to count
    :returns: A ``dict`` with the number of each motifs, with the same keys as ``mo``
    This function is actually rather simple. It will extract all 3-grams from
    the original graph, and look for isomorphisms in the motifs contained
    in a dictionary. The returned object is a ``dict`` with the number of
    times each motif was found.::
        >>> print(mcounter(gr, mo))
        {'S1': 4, 'S3': 0, 'S2': 1, 'S5': 0, 'S4': 3}
    """
    # This function will take each possible subgraph of gr of size 3, then
    # compare them to the mo dict using .subgraph() and is_isomorphic

    # This line simply creates a dictionary with 0 for all values, and the
    # motif names as keys
    mcount = dict(zip(mo.keys(), list(map(int, np.zeros(len(mo))))))
    nodes = list(gr.nodes())

    # We use itertools.product to have all combinations of three nodes in the
    # original graph. Then we filter combinations with non-unique nodes, because
    # the motifs do not account for self-consumption.
    triplets = list(itertools.product(nodes, repeat=3))
    triplets = [trip for trip in triplets if len(set(trip)) == 3]
    triplets = list(map(list, map(np.sort, triplets)))

    # Removing duplicates by converting list of lists to list of tuples for faster uniqueness check
    u_triplets = list(map(list, set(tuple(trip) for trip in triplets)))

    # The for each each of the triplets, we (i) take its subgraph, and compare
    # it to all of the possible motifs
    for trip in u_triplets:
        sub_gr = gr.subgraph(trip)
        mot_match = [nx.is_isomorphic(sub_gr, mo[mot_id]) for mot_id in mo.keys()]
        match_keys = [list(mo.keys())[i] for i in range(len(mo)) if mot_match[i]]
        
        if len(match_keys) == 1:
            mcount[match_keys[0]] += 1

    return mcount

## rewiring 
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

def randomization_constant_Kseq(G, directed=False):
    
    Amat=nx.to_pandas_adjacency(G)
    
    r_hp=find_presences(Amat.values)
    RM=curve_ball(Amat.values,r_hp) #randomized by curveball
    rnd_Amat=pd.DataFrame(RM,index=Amat.index, columns=Amat.columns)
    
    Idf=rnd_Amat.unstack() #I es P(row)XA(col), y el unstack pone a los pollinator como 1ª columna, lo que implica que son el source
    Idf=Idf[Idf>0]
    
    if (directed):
        G_rnd=nx.DiGraph()
    else:
        G_rnd=nx.Graph()
    species=G.nodes()
    G_rnd.add_nodes_from(species)
    edge_list = list(Idf.to_frame().to_records())
    G_rnd.add_weighted_edges_from(edge_list) #parece que lo entiende justo al reves
    
    
    return G_rnd.reverse()

def randomization_constant_Kseq_bipart(B,bottom_nodes,top_nodes):
    
    web=nx.to_pandas_adjacency(B).loc[list(bottom_nodes), list(top_nodes)]
    
    r_hp=find_presences(web.values)
    RM=curve_ball(web.values,r_hp) #randomized by curveball
    rnd_web=pd.DataFrame(RM,index=web.index, columns=web.columns)

    Idf=rnd_web.unstack() #I es P(row)XA(col), y el unstack pone a los pollinator como 1ª columna, lo que implica que son el source
    Idf=Idf[Idf>0]
    
    #create bipartite graph
    B_rnd = nx.Graph()
    B_rnd.add_nodes_from(bottom_nodes, bipartite="plant")
    B_rnd.add_nodes_from(top_nodes, bipartite="pollinator")
    edge_list = list(Idf.to_frame().to_records())
    B_rnd.add_weighted_edges_from(edge_list) #parece que lo entiende justo al reves
    
    return B_rnd

def from_Imat_to_nxBipart(I):

    Idf=I.unstack() #I es P(row)XA(col), y el unstack pone a los pollinator como 1ª columna, lo que implica que son el source
    #remove zeros
    Idf=Idf[Idf>0]

    #create bipartite graph
    B = nx.Graph()
    B.add_nodes_from(list(Idf.index.unique(level='Plant_gen_sp')), bipartite="Plant")
    B.add_nodes_from(list(Idf.index.unique(level='Pollinator_gen_sp')), bipartite="Pollinator")
    edge_list = list(Idf.to_frame().to_records())
    B.add_weighted_edges_from(edge_list) #parece que lo entiende justo al reves

    return B


def rewire_constantNL(Imat):
    
    net=from_Imat_to_nxBipart(Imat)

    rnd_net = nx.Graph()
    #first copy all original nodes so they remain there:
    rnd_net.add_nodes_from(net.nodes(data=True))
    #in this rewrirign we will create as many links in the new networks as where in the original, irrespective of the degree:
    change=0
    nodes_a=[]
    nodes_b=[]
    #get different sets of nodes, since network may be not completely connected we sort like this, based in the label
    for node in net.nodes():
        if (net.nodes[node]['bipartite']=="Plant"):
            nodes_b.append(node)#plants
        else:
            nodes_a.append(node)#animals

    edges=list(rnd_net.edges())

    #copy lists because we are going to force that each node has at least 1 connection
    unconnected_nodes_a = nodes_a.copy()
    unconnected_nodes_b = nodes_b.copy()

    #print("comenzamos con %s edges" % len(list(net.edges())))
    L=len(list(net.edges()))
    while (change < L):
        #print("change %s of %s" %(change,len(list(net.edges()))))
        from_unconnected_a=False
        if (len(unconnected_nodes_a)>0): #while there are unconnected nodes
            node_a=unconnected_nodes_a[random.randint(0,len(unconnected_nodes_a)-1)]
            from_unconnected_a = True
        else:
            node_a = nodes_a[random.randint(0, len(nodes_a) - 1)]

        from_unconnected_b=False
        if (len(unconnected_nodes_b)>0):
            node_b = unconnected_nodes_b[random.randint(0, len(unconnected_nodes_b) - 1)]
            from_unconnected_b=True
        else:
            node_b=nodes_b[random.randint(0,len(nodes_b)-1)]

        while ( ((node_a,node_b) in edges) or ((node_b,node_a) in edges) ):
            #in principle it is not possible to have repeated edges if taken from unconnected nodes
            node_b=nodes_b[random.randint(0,len(nodes_b)-1)]
            node_a = nodes_a[random.randint(0,len(nodes_a) - 1)]

        if (from_unconnected_a):
            unconnected_nodes_a.remove(node_a)
        if (from_unconnected_b):
            unconnected_nodes_b.remove(node_b)

        rnd_net.add_edge(node_a,node_b,weight=1)#unweighted
        edges = list(rnd_net.edges())
        #print(edges)
        change = change +1
    rnd_Imat=from_nxBipart_to_Imat(rnd_net)    

    return rnd_Imat

def rewire_constantNL_fom_net(net):

    rnd_net = nx.Graph()
    #first copy all original nodes so they remain there:
    rnd_net.add_nodes_from(net.nodes(data=True))
    #in this rewrirign we will create as many links in the new networks as where in the original, irrespective of the degree:
    change=0
    nodes_a=[]
    nodes_b=[]
    #get different sets of nodes, since network may be not completely connected we sort like this, based in the label
    for node in net.nodes():
        if (net.nodes[node]['bipartite']=="Plant"):
            nodes_b.append(node)#plants
        else:
            nodes_a.append(node)#animals

    edges=list(rnd_net.edges())

    #copy lists because we are going to force that each node has at least 1 connection
    unconnected_nodes_a = nodes_a.copy()
    unconnected_nodes_b = nodes_b.copy()

    #print("comenzamos con %s edges" % len(list(net.edges())))
    L=len(list(net.edges()))
    while (change < L):
        #print("change %s of %s" %(change,len(list(net.edges()))))
        from_unconnected_a=False
        if (len(unconnected_nodes_a)>0): #while there are unconnected nodes
            node_a=unconnected_nodes_a[random.randint(0,len(unconnected_nodes_a)-1)]
            from_unconnected_a = True
        else:
            node_a = nodes_a[random.randint(0, len(nodes_a) - 1)]

        from_unconnected_b=False
        if (len(unconnected_nodes_b)>0):
            node_b = unconnected_nodes_b[random.randint(0, len(unconnected_nodes_b) - 1)]
            from_unconnected_b=True
        else:
            node_b=nodes_b[random.randint(0,len(nodes_b)-1)]

        while ( ((node_a,node_b) in edges) or ((node_b,node_a) in edges) ):
            #in principle it is not possible to have repeated edges if taken from unconnected nodes
            node_b=nodes_b[random.randint(0,len(nodes_b)-1)]
            node_a = nodes_a[random.randint(0,len(nodes_a) - 1)]

        if (from_unconnected_a):
            unconnected_nodes_a.remove(node_a)
        if (from_unconnected_b):
            unconnected_nodes_b.remove(node_b)

        rnd_net.add_edge(node_a,node_b,weight=1)#unweighted
        edges = list(rnd_net.edges())
        #print(edges)
        change = change +1
    #rnd_Imat=from_nxBipart_to_Imat(rnd_net)    

    return rnd_net

def sample_path_lengths(G, nodes=None, trials=1000):
    if nodes is None:
        nodes = list(G)
    else:
        nodes = list(nodes)

    pairs = np.random.choice(nodes, (trials, 2))
    lengths = [nx.shortest_path_length(G, *pair)
               for pair in pairs]
    return lengths

def estimate_path_length(G, nodes=None, trials=1000):
    return np.mean(sample_path_lengths(G, nodes, trials))

def read_graph_facebook():
    facebook = pd.read_csv(
    "./data/facebook_combined.txt.gz",
    compression="gzip",
    sep=" ",
    names=["start_node", "end_node"],
    )
    G = nx.from_pandas_edgelist(facebook, "start_node", "end_node")

    return G

def load_airports_data():
    pass_air_data = pd.read_csv("./data/passengers.csv", index_col="id")
    return pass_air_data

#define functions to fit: Truncated power law and normal power law
def EF(k, b,cinv):
    return b*np.exp( -cinv*k)

def TPL(k, b, gamma,ko_inv):
    return b * pow(k,-1*gamma)*np.exp( -ko_inv*k)  #ko_inv=1/maxk

def PL(k, b, gamma):
    return b * pow(k,-1*gamma)

def TPL_equation(k, b, gamma, ko_inv):
    return b * pow(k, -gamma) * np.exp(-ko_inv * k) - 0.9

def PL_equation(k, b, gamma):
    return b * pow(k,-1*gamma) - 0.9

def load_game_of_thrones_data():
    books = pd.read_csv("./data/game_of_thrones_network/asoiaf.csv", index_col="id")
    return books

def interaction_matrix(web, gamma_avg=0.01, rho=0.005, delta=0):
    SA, SP = web.shape

    plant_names=list(web.columns)
    pol_names=list(web.index)

    alphaA = rho * np.ones((SA, SA)) + (1 - rho) * np.eye(SA)
    alphaP = rho * np.ones((SP, SP)) + (1 - rho) * np.eye(SP)

    alphaA_df = pd.DataFrame(alphaA, index=pol_names, columns=pol_names)
    alphaP_df = pd.DataFrame(alphaP, index=plant_names, columns=plant_names)

    gammaA = (np.diag(np.power(np.sum(web, axis=1), -delta)) @ web).values
    gammaP = (np.diag(np.power(np.sum(web, axis=0), -delta)) @ web.T).values

    f = np.sum(gammaA[web == 1] + gammaP[web.T == 1]) / (2 * sum(np.sum(web == 1)))
    
    gammaA = (gamma_avg / f) * (np.diag(np.power(np.sum(web, axis=1), -delta)) @ web)
    gammaP = (gamma_avg / f) * np.diag(np.power(np.sum(web, axis=0), -delta)) @ web.T

    gammaA_df=pd.DataFrame(gammaA.values, index=pol_names, columns=plant_names)
    gammaP_df=pd.DataFrame(gammaP.values, index=plant_names, columns=pol_names)


    gammaA[np.isnan(gammaA)] = 0
    gammaP[np.isnan(gammaP)] = 0

    alpha = np.block([
        [alphaA, -gammaA],
        [-gammaP, alphaP]
    ])

    row_names = pol_names + plant_names
    col_names = pol_names + plant_names

    alpha_df = pd.DataFrame(alpha, index=row_names, columns=col_names)

    out = {'alpha': alpha_df,
        'alphaA': alphaA_df,
        'alphaP': alphaP_df,
        'gammaA': gammaA_df,
        'gammaP': gammaP_df
    }

    return out

def simplex_sampling(m, n):
    result = []
    for _ in range(m):
        # Generate n-1 sorted uniform random values between 0 and 1
        dist = np.sort(np.random.uniform(0, 1, n - 1))
        dist = np.append(dist, 1)  # Add 1 to the end
        # Compute the differences to create the simplex sample
        result.append(np.diff(np.insert(dist, 0, 0)))  # Equivalent to c(dist[1], diff(dist)) in R
    return result

def calc_Omegas_py(myweb,size_norm=True, no_log=True,rho=0.005,gamma_avg=0.1, delta=0):
    N=myweb.shape[0]+myweb.shape[1]
    Na=myweb.shape[0]
    Np=myweb.shape[1]

    m=interaction_matrix(myweb, gamma_avg = gamma_avg, rho = rho, delta = delta)

    adj=m["alpha"]

    try:
        O = Omega_function(adj)
    except:
        O = np.nan  

    Beta_a=m['alphaA']
    Beta_p=m[ 'alphaP']
    Gamma_a=m['gammaA']
    Gamma_p=m['gammaP']

    Beta_p_mod= np.matrix(Gamma_p)*np.linalg.inv(np.matrix(Beta_a))*np.matrix(Gamma_a)
    Beta_a_mod= np.matrix(Gamma_a)*np.linalg.inv(np.matrix(Beta_p))*np.matrix(Gamma_p)
        
    Beta_p_eff = np.matrix(Beta_p) - Beta_p_mod
    Beta_a_eff = np.matrix(Beta_a) - Beta_a_mod

    try:
        O_P_eff = Omega_function(Beta_p_eff)
    except:
        O_P_eff = np.nan

    try:        
        O_A_eff = Omega_function(Beta_a_eff)
    except:
        O_A_eff = np.nan    

    if (size_norm):
        if (no_log):
            om= pow(pow(10,O),1./N)
            OP_eff= pow(pow(10,O_P_eff),1./Np)
            OA_eff=pow(pow(10,O_A_eff),1./Na)
        else:    
            om= np.log10(pow(pow(10,O[0]),1./N))
            OP_eff= np.log10(pow(pow(10,O_P_eff),1./Np))
            OA_eff=np.log10(pow(pow(10,O_A_eff),1./Na))
    else:
        if (no_log):
            om=pow(10,O)
            OP_eff=pow(10,O_P_eff)
            OA_eff=pow(10,O_A_eff)
        else:    
            om=O
            OP_eff=O_P_eff
            OA_eff=O_A_eff

    return(om,OP_eff,OA_eff)

def Omega_function(alpha):
    S = alpha.shape[0]
    Sigma = np.linalg.inv(alpha.T @ alpha)
    m = np.zeros((S, 1))
    a = np.zeros((S, 1))
    b = np.full((S, 1), np.inf)
    lower = np.zeros(S)
    upper = np.full(S, np.inf)
    mean = np.zeros(S)
    
    d, _ = mvn.mvnun(lower, upper, mean, Sigma)
    
    out = np.log10(d)
    return out