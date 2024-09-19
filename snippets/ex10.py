sp0='Suspension-feeding molluscs'
sp1='Tonguefish'
sp2='Fish and crustacean-eating birds'
sp3='Herbivorous ducks' 

sp1_sp0=nx.has_path(FW,sp0,sp1)
print("1. It is %s that %s eats %s" % (sp1_sp0,sp1,sp0))

sp2_sp0=nx.has_path(FW,sp0,sp2)
print("2. It is %s that %s eats %s" % (sp2_sp0,sp2,sp0))

L1=nx.shortest_path_length(FW,sp0,sp2)
L2=nx.shortest_path_length(FW,sp0,sp3)

if(L1<L2):
    print("3. %s are in more danger since they are only %s steps away and %s are %s steps away" %(sp2,L1,sp3,L2))
else:
    print("3. %s are in more danger since they are only %s steps away and %s are %s steps away" %(sp3,L2,sp2,L1))
