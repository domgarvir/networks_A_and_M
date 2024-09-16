sp_0='Suspension-feeding molluscs'
sp_1='Catfish and stingrays'
sp_2='Spider crabs'
sp_3='Red drum'

sp1_sp0=nx.has_path(FW,sp_0,sp_1)
print("It is %s that %s eats %s" % (sp1_sp0,sp1,sp0))

sp0_sp1=nx.shortest_path(FW,sp_0,sp_1)

nx.shortest_path(FW,sp_0,sp_3)

list(FW.successors(sp_0))

TL=pd.Series(nx.centrality.trophic_levels(FW)).sort_values(ascending=True)
TL