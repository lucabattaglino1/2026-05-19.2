from networkx import DiGraph

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = DiGraph()
        self._nodes = []
        self._idMapAO = {}

    def getGeneri(self):
        return DAO.getAllGeneri()


    def buildGraph(self, genere):
        self._graph.clear()
        self._nodes = DAO.getAllNodes(genere)
        self._idMapAO = {}
        for n in self._nodes:
            self._idMapAO[n.ArtistId] = n

        self._graph.add_nodes_from(self._nodes)
        self.addEdges(genere)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def addEdges(self, genere):
        PopolaritaMap = {}
        for artistId, peso in DAO.getPopolarita():
            PopolaritaMap[artistId] = peso

        for n1, n2 in DAO.getCoppie(genere, self._idMapAO):
            v1 = PopolaritaMap.get(n1.ArtistId, 0)
            v2 = PopolaritaMap.get(n2.ArtistId, 0)
            peso = v1 + v2

            if v1 > v2:
                self._graph.add_edge(n1, n2, weight=peso)  # n1 vende più -> ESCE da n1
            elif v2 > v1:
                self._graph.add_edge(n2, n1, weight=peso)
            else:
                self._graph.add_edge(n1, n2, weight=peso)
                self._graph.add_edge(n2, n1, weight=peso)


    def getNumEdges(self):
        return len(self._graph.edges)

    def getMaxInfluenza(self):
        maxInfluenza = None
        maxArtista = None
        for n in self._graph.nodes:
            pesoUscenti = 0
            for v in self._graph.successors(n):
                pesoUscenti += self._graph[n][v]["weight"]
            pesoEntranti = 0
            for u in self._graph.predecessors(n):
                pesoEntranti += self._graph[u][n]["weight"]
            influenza = pesoUscenti - pesoEntranti
            if maxInfluenza is None or influenza > maxInfluenza:
                maxInfluenza = influenza
                maxArtista = n
        return maxArtista, maxInfluenza

    def getTop5Archi(self):
        archi = []
        for u, v, dati in self._graph.edges(data=True):
            archi.append((u, v, dati["weight"]))
        archi.sort(key=lambda x: x[2], reverse=True)
        return archi[:5]