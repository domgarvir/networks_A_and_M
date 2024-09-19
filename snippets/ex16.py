Clus=pd.Series(dict(nx.clustering(G)))
Betw=pd.Series(dict(nx.betweenness_centrality(G)))
Clos=pd.Series(dict(nx.closeness_centrality(G)))
Deg=pd.Series(dict(nx.degree_centrality(G)))

Centrality_df=pd.concat([Clus,Betw,Clos,Deg], axis=1)
Centrality_df.columns=["T","B","C","D"]