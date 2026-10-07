import networkx as nx, glob, os, collections, statistics, json
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

D='data/social-networks'
def load_ego(ego):
    G=nx.read_edgelist(f'{D}/{ego}.edges',nodetype=int)
    G.add_edges_from((ego,v) for v in list(G.nodes))
    return G

def dist_counts(G):
    c=collections.Counter()
    for s,dd in nx.all_pairs_shortest_path_length(G):
        for t,l in dd.items():
            if s<t: c[l]+=1
    return c

def stats(c):
    seq=[l for l,n in sorted(c.items()) for _ in range(n)]
    return dict(mode=max(c,key=c.get),median=statistics.median(seq),
                mean=round(sum(seq)/len(seq),3),diameter=max(c),pairs=sum(c.values()))

egos=sorted(int(os.path.basename(f).split('.')[0]) for f in glob.glob(f'{D}/*.edges'))
res={}; union=nx.Graph()
for e in egos:
    G=load_ego(e); union=nx.compose(union,G)
    comps=nx.number_connected_components(G)
    c=dist_counts(G); res[e]=(G,c,comps)
    print(e,G.number_of_nodes(),G.number_of_edges(),'компонент:',comps,stats(c))

cu=dist_counts(union)
print('объедененный граф',union.number_of_nodes(),union.number_of_edges(),
      'компонент:',nx.number_connected_components(union))
print(sorted(cu.items())); print(stats(cu))

# графики
def bar(ax,c,title):
    ks=sorted(c); ax.bar(ks,[c[k] for k in ks],color="#c66eb1")
    st=stats(c); ax.axvline(st['median'],color='r',ls='--',label=f"медиана={st['median']}")
    ax.set_title(f"{title}\nмода={st['mode']}, мед.={st['median']}, ср.={st['mean']}")
    ax.set_xlabel('длина кратчайшего пути'); ax.set_ylabel('число пар'); ax.set_xticks(ks)
fig,ax=plt.subplots(figsize=(7,4.5)); bar(ax,cu,'объединённый граф'); ax.legend(); fig.tight_layout(); fig.savefig('distribution_union.png',dpi=150)
fig,axs=plt.subplots(2,5,figsize=(20,8))
for ax,e in zip(axs.flat,egos): bar(ax,res[e][1],f'эго-сеть {e}')
fig.tight_layout(); fig.savefig('distribution_per_ego.png',dpi=120)
json.dump({'union':dict(sorted(cu.items())),'stats':stats(cu)},open('result.json','w'),ensure_ascii=False,indent=1)