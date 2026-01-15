import networkx as nx
from database.dao import DAO

FATTORE_DIFFICOLTA = {
            'facile' : 1,
            'media' : 1.5,
            'difficile' : 2
        }

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G = nx.Graph()
        self.rifugi = None # dizionario rifugi
        self._edges = None # dizionario connessioni

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        self.rifugi = DAO.get_all_rifugi(year)
        self.edges = DAO.get_all_connessioni(self.rifugi, year)

        self.G.clear()

        self.G.add_nodes_from(self.rifugi.values())

        for c in self.edges.values():
            rifugio1, rifugio2 = c.rifugio1, c.rifugio2
            peso = self.calcola_peso_arco(c)
            if peso is not None:
                self.G.add_edge(rifugio1, rifugio2, weight=peso)

    def calcola_peso_arco(self, edge):

        try:
            distanza = float(getattr(edge, 'distanza')) #estrae attributo distanza dalla connessione in questione
        except ValueError:
            print('Il valore distanza non è valido')
            return None

        difficolta = getattr(edge, 'difficolta', None)
        if difficolta not in FATTORE_DIFFICOLTA:
            return None

        fattore_difficolta = FATTORE_DIFFICOLTA[difficolta]

        return distanza * fattore_difficolta


    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        #self.G.edges(data=True) restituisce una lista di tuple composte da tre elementi,
        #in questo caso nodo partenza, nodo arrivo, dict di attributi.
        # _, _ si usa per non considerare le parti della tupla che non ci interessano

        # TODO
        pesi = [edge['weight'] for _,_,edge in self.G.edges(data=True)]
        if pesi is not None:
            return min(pesi), max(pesi)
        else:
            return None


    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        minori = sum(1 for _,_,edge in self.G.edges(data=True) if edge['weight'] < soglia)
        maggiori = sum(1 for _,_,edge in self.G.edges(data=True) if edge['weight'] > soglia)

        return minori, maggiori

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO

    def _get_nodes(self):
        return self.G.nodes()

    def cammino_minimo_ricorsione(self, soglia):
        self.best_edges = [] # archi contenuti nel miglior percorso
        self.best_cost = float('inf') # costo minimo trovato

        # ad ogni nodo avvia la ricerca
        for nodo in self._get_nodes():
            partial = [nodo]
            partial_edges = []
            self._ricorsione(soglia, partial, partial_edges)

        return self.best_edges


    def _ricorsione(self, soglia, partial_nodes, partial_edges):
        if partial_edges:
            cost = self._calcolo_weight_path(partial_edges)

            if cost >= self.best_cost:
                return
            if len(partial_edges) >= 2:
                self.best_cost = cost
                self.best_edges = partial_edges[:]

        ultimo_nodo = partial_nodes[-1]
        neighs = self._get_neighs(ultimo_nodo)

        for v in neighs:
            edge_attr = self.G.get_edge_data(ultimo_nodo, v)
            partial_nodes.append(v)
            partial_edges.append(ultimo_nodo, v, edge_attr)
            self._ricorsione(soglia, partial_nodes, partial_edges)
            partial_nodes.pop()
            partial_edges.pop()


    def _calcolo_weight_path(self, edges):
        total = 0.0
        for _,_,weight in edges:
            if weight:
                total += float(weight.get('weight', 0.0))
        return total

    def _get_neighs(self, node, partial_nodes, soglia):
        """
       Restituisce i vicini ammissibili:
         - non ancora visitati (evita cicli)
         - l'arco (node, v) esiste e ha 'weight' > soglia
       :param node: il nodo da considerare
       :param partial_nodes: lista di nodi già considerati nel cammino
       :param soglia: la soglia oltre la quale deve essere il peso di ogni arco
       :return: lista di vicini ammissibili
       """

        neighs = []
        for v in self.G.neighbors(node):
            if v in partial_nodes:
                continue
            attr = self.G.get_edge_data(node, v)
            if not attr:
                continue
            w = attr.get('weight', None)
            if w is None:
                continue
            if w >= soglia:
                neighs.append(v)
        return neighs








