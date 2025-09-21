import pandas as pd
import networkx as nx
import json

# 1- Games of Thrones Dataframe of interactions and networks  ----------------
my_path="./data/Projects/GOT/asoiaf-books/"
book="book1" #book1,book2,book3,book4,book5

# Load CSV files - Information in dataframe format
edges = pd.read_csv(my_path+book+"-edges.csv")   # Source,Target,Type,id,weight
nodes = pd.read_csv(my_path+book+"-nodes.csv")   # Id,Label

# Create an undirected graph
G = nx.Graph()

# Add nodes with labels
for _, row in nodes.iterrows():
    G.add_node(row['Id'], label=row['Label'])

# Add edges with weights and other attributes
for _, row in edges.iterrows():
    G.add_edge(row['Source'], row['Target'], 
               weight=row['weight'], 
               book=row['book'],
               edge_type=row['Type'])

#--------------------------------------------------------------------------------
# 2 - Star wars  Network and Dataframe of interactions --------------------------
my_path="./data/Projects/STAR_WARS/"
movie="1" 
itype="-interactions-allCharacters" # -interactions, -mentions
filename=my_path+"episode-"+movie+itype+".json"
with open(filename, "r") as f:
    data = json.load(f)

nodes = data["nodes"]
links = data["links"]

# --- Build the graph ---
G = nx.Graph()

# Add nodes with attributes
for i, node in enumerate(nodes):
    G.add_node(i, 
               name=node["name"], 
               value=node["value"], 
               colour=node["colour"])

# Add edges with weights
for link in links:
    G.add_edge(link["source"], link["target"], value=link["value"])

# --- Create a dataframe with interactions ---
# Use the names instead of indices for clarity
interactions = []
for link in links:
    source = nodes[link["source"]]["name"]
    target = nodes[link["target"]]["name"]
    value  = link["value"]
    interactions.append([source, target, value])

df_interactions = pd.DataFrame(interactions, columns=["Source", "Target", "Value"])

print(df_interactions.head())

#---------------------------------------------------------------------------------
#3 - Lord of the rings Dataframe of itneractions and network----------------------
my_path="./data/Projects/LOTR/"
book="1" #1,2,3,all
filename=my_path+"network-book"+book+".csv"

# Load edges and information about the node
info = pd.read_csv(my_path+"pre-ontology.csv", sep="\t")  # assuming it's tab-separated

# Keep only useful columns for nodes
nodes = info[['id','normalizedName','type','freq']].drop_duplicates()
id_to_name = dict(zip(nodes['id'], nodes['normalizedName']))

edges = pd.read_csv(filename)         # IdSource,IdTarget,Weight,Type: Dataframe of interactions
# Map Ids to canonical names
edges['SourceName'] = edges['IdSource'].map(id_to_name)
edges['TargetName'] = edges['IdTarget'].map(id_to_name)

G = nx.Graph()

# Add nodes with attributes
for _, row in nodes.iterrows():
    G.add_node(row['id'],
               label=row['normalizedName'],
               type=row['type'],
               freq=row['freq'])

# Add edges with attributes
for _, row in edges.iterrows():
    G.add_edge(row['IdSource'], row['IdTarget'],
               weight=row['Weight'],
               edge_type=row['Type'])
    
#---------------------------------------------------------
# 4 Import/Export world trade network
my_path="./data/Projects/TRADE/"
year='2023'
filename=my_path+"BACI_Y"+year+".csv"

# Trade flows
trade_df = pd.read_csv(filename)   
# t,i,j,k,v,q List of Variables:
#t: year
#i: exporter
#j: importer
#k: product
#v: value
#q: quantity

#To better understand the information one needs to load also the name of countires and products
# Country codes
countries = pd.read_csv(my_path+"country_codes.csv")   # country_code,country_name,country_iso2,country_iso3
# Product codes
products = pd.read_csv(my_path+"product_codes.csv")   # code,description

# Merge exporter
trade_df = trade_df.merge(
    countries.rename(columns={
        "country_code": "i",
        "country_name": "exporter_name",
        "country_iso2": "exporter_iso2",
        "country_iso3": "exporter_iso3"
    }),
    on="i", how="left"
)
# Merge importer
trade_df = trade_df.merge(
    countries.rename(columns={
        "country_code": "j",
        "country_name": "importer_name",
        "country_iso2": "importer_iso2",
        "country_iso3": "importer_iso3"
    }),
    on="j", how="left"
)
trade_df = trade_df.merge(
    products.rename(columns={"code": "k", "description": "product_description"}),
    on="k", how="left"
)

#Now with trade_df one can build the network of trade between countries and products. 
#I recommend aggregating products using only the first 4 numbers of the code, for example all 
#the codes starting with 0101 represent trade of live horses, and those starting with 0103 live pigs.
#This will generat a more simple network that is easier to work with.
# Make sure product codes are strings
trade_df["k"] = trade_df["k"].astype(str)

# Extract first 4 digits
trade_df["hs4"] = trade_df["k"].str[:4]
# Group by year, exporter, importer, and hs4 code
SimpleTrade_df = (trade_df.groupby(["t", "exporter_name", "exporter_iso3", "importer_name", "importer_iso3","hs4"])
         .agg({
             "v": "sum",   # sum of value in thousand USD
             "q": "sum"    # sum of quantity in tons
         })
         .reset_index()
         .rename(columns={
             "t": "year",
             "v": "value_usd_thousands",
             "q": "quantity_tons"
         }))
#-------------------------------------------------------------------------------------------------
#5 AIrport traffic network -----------------------------------------------------------------------
my_path="./data/Projects/FLIGHTS/"
pass_air_data = pd.read_csv(my_path+"passengers.csv", index_col="id")
coordinates=pd.read_csv(my_path+"GlobalAirportDatabase.txt", delimiter=":", header=0)

#-------------------------------------------------------------------------------------------------
#6 Foodwebs --------------------------------------------------------------------------------------
# the 17 available quantitative foodwebs in the web of live database
my_path="./data/Projects/FOODWEBS/"
 
#read information of the available networks
references_df=pd.read_csv(my_path+"references.csv")

webs=["001", "002","003","004","005","006","007","008","009","010", "016_01", "017_01", "017_02", "017_03","017_04","017_05","017_06"]

web=webs[0]#for now I only choose the first one

#To create the dataframe of interactions:
my_df = pd.read_csv(my_path+"FW_"+web+".csv", index_col=0)
# prey = index, predator = columns, values = weight
interactions = my_df.stack().reset_index()
interactions.columns = ["Prey", "Predator", "Weight"]
# keep only nonzero interactions
interactions = interactions[interactions["Weight"] > 0].reset_index(drop=True)

#------------------------------------------------------------------------------------------------
#7 Multilayer network ---------------------------------------------------------------------------
# As the data was complex, I have written the code to obtain a dataframe with the interactions
my_path="./data/Projects/INTERTIDAL/"

def read_adj_matrix(filename, interaction_type):
    """
    Read multiplex adjacency file and return edge list dataframe.
    interaction_type = 'T', 'NTp', or 'NTn'
    """
    df = pd.read_csv(filename, sep="\t", header=0)
    
    # First two cols: id, name
    ids = df.iloc[:,0]
    names = df.iloc[:,1]
    
    # Adjacency values start from col index 2
    adj = df.iloc[:,2:].values
    col_ids = df.columns[2:].astype(int)  # target species IDs
    
    edges = []
    for i, source_id in enumerate(ids):
        for j, target_id in enumerate(col_ids):
            if adj[i,j] == 1:
                edges.append([source_id, target_id, interaction_type])
    
    return pd.DataFrame(edges, columns=["source", "target", "interaction"])

ftype="TI" #TI,NTIpos, NTIneg
filename=my_path+"chilean_"+ftype+".txt"
edges_T   = read_adj_matrix(filename, ftype)
ftype="NTIpos" #TI,NTIpos, NTIneg
filename=my_path+"chilean_"+ftype+".txt"
edges_NTp = read_adj_matrix(filename, "NTp")
ftype="NTIneg" #TI,NTIpos, NTIneg
filename=my_path+"chilean_"+ftype+".txt"
edges_NTn = read_adj_matrix(filename, "NTn")

# Combine all edges
edges_all = pd.concat([edges_T, edges_NTp, edges_NTn], ignore_index=True)

# Load metadata
meta = pd.read_csv(my_path+"chilean_metadata.csv")
# Merge source info
edges_all = edges_all.merge(
    meta[["Spec","Species names"]],
    left_on="source", right_on="Spec", how="left"
).rename(columns={"Species names":"source_name"}).drop(columns="Spec")

# Merge target info
edges_all = edges_all.merge(
    meta[["Spec","Species names"]],
    left_on="target", right_on="Spec", how="left"
).rename(columns={"Species names":"target_name"}).drop(columns="Spec")

# -----------------------------------------------------------------------------------
# 8 Mutualistic networks ------------------------------------------------------------
my_path="./data/Projects/MUTUALISTIC/"
#read information of the available networks
references_df=pd.read_csv(my_path+"references.csv")
webs=["M_PL_004.csv",  "M_PL_041.csv", "M_PL_073.csv", "M_SD_005.csv",  "M_SD_020.csv",
"M_PL_006.csv",  "M_PL_051.csv",     "M_PL_074_01.csv",  "M_SD_006.csv",  "M_SD_031.csv",
"M_PL_017.csv",  "M_PL_058.csv",     "M_SD_002.csv",     "M_SD_010.csv",  "M_SD_034.csv",
"M_PL_019.csv",  "M_PL_060_05.csv",  "M_SD_003.csv",     "M_SD_011.csv",
"M_PL_040.csv",  "M_PL_060_06.csv",  "M_SD_004.csv",     "M_SD_012.csv"]
    


web=webs[0]#for now I only choose the first one

#To create the dataframe of interactions:
my_df = pd.read_csv(my_path+web, index_col=0)
# plant = index, animal = columns, values = weight
interactions = my_df.stack().reset_index()
interactions.columns = ["Plant", "Animal", "Weight"]
interactions = interactions[interactions["Weight"] > 0].reset_index(drop=True)
#--------------------------------------------------------------------------------------