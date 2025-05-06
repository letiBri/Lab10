import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self._countries = DAO.getAllCountries()
        self._idMap = {}
        for c in self._countries:
            self._idMap[c.CCode] = c  # faccio la iddMap dove associo al codice dello Stato, l'oggetto Stato
        self._grafo = nx.Graph()  # creo il grafo non orientato e non pesato

    def buildGraph(self, anno):
        listaStatiEsistenti = DAO.getCountriesAnno(anno)  # salvo solo gli i codici degli stati con i collegamenti per quell'anno
        for code in listaStatiEsistenti:
            self._grafo.add_node(self._idMap[code])  # aggiungo i nodi al grafo, accedendo all'oggetto Stato attraverso la idMap
        listaTupleArchi = DAO.getAllEdges(anno)  # salvo i collegamenti terreni, quindi filtro il conttype = 1
        for tupla in listaTupleArchi:
            self._grafo.add_edge(self._idMap[tupla[0]], self._idMap[tupla[1]])
        #print(len(self._grafo.nodes))
        #print(len(self._grafo.edges))
        listaGradiStati = self.getGradoNodes()
        numCompConnesse = self.getCompConnesse()
        return self._grafo, listaGradiStati, numCompConnesse

    def getGradoNodes(self):
        result = {}
        for node in self._grafo.nodes():
            result[node] = self._grafo.degree(node)  # questo è un dizionario che associa a ciascun nodo, il numero di collegamenti con altri nodi

        ordinato = sorted(result.keys(), key=lambda x: x.StateAbb)
        lista = []
        for stato in ordinato:
            lista.append(f"{stato.StateNme} -- {result[stato]} vicini")
        return lista

    def getCompConnesse(self):
        conn = list(nx.connected_components(self._grafo))
        return len(conn)

    def getNodiRaggiungibili(self, source):
        conn = nx.node_connected_component(self._grafo, source) # utilizzo i metodi di networkX per trovare la componente connessa partendo da source
        conn.remove(source)
        return conn, len(conn)


