import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self.rifugio_dict = {}


    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        self.G.clear()
        rifugi = DAO.read_rifugi()
        self.rifugio_dict = {rifugio.id: rifugio for rifugio in rifugi} # dizionario per poi creare oggetti rifugio

        sentieri = DAO.read_sentieri()
        for sentiero in sentieri:
            if sentiero.anno <= year:
                if sentiero.difficolta == 'facile':
                    peso = float(sentiero.distanza) * 1
                elif sentiero.difficolta == 'medio':
                    peso = float(sentiero.distanza) * 1.5
                elif sentiero.difficolta == 'difficile':
                    peso = float(sentiero.distanza) * 2
                self.G.add_edge(self.rifugio_dict[sentiero.id_rifugio1], self.rifugio_dict[sentiero.id_rifugio2], peso=peso)


    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        pesi = nx.get_edge_attributes(self.G, 'peso')
        min_peso = min(pesi.values())
        max_peso = max(pesi.values())
        return min_peso, max_peso


    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        pesi = nx.get_edge_attributes(self.G, 'peso')
        minori = []
        maggiori = []

        for arco, peso in pesi.items() :
            if peso < soglia:
                minori.append(arco)
            elif peso > soglia:
                maggiori.append(arco)
        num_minori = len(minori)
        num_maggiori = len(maggiori)

        return num_minori, num_maggiori


    """Implementare la parte di ricerca del cammino minimo"""
    # METODO CON NETWORKX
    def get_cammino_minimo_nx(self, soglia):
        nuovo_grafo = nx.Graph()
        cammino_ottimo = []
        peso_ottimo = float('inf')

        for nodo_p, nodo_a, attr in self.G.edges(data=True): # attr: dizionario con tutti gli attributi di arco
            if attr['peso'] > soglia:
                nuovo_grafo.add_edge(nodo_p, nodo_a, peso=attr['peso']) #grafo solo con archi di peso maggiore alla soglia

        for nodo1 in nuovo_grafo.nodes():
            for nodo2 in nuovo_grafo.nodes():
                if nodo1 != nodo2:
                    try:
                        cammino_minimo = nx.shortest_path(nuovo_grafo, source=nodo1, target=nodo2, weight='peso')
                        if len(cammino_minimo) >= 3:
                            peso_totale = nx.path_weight(nuovo_grafo, cammino_minimo, weight='peso') # calcola il peso totale nel cammino minimo
                            if peso_totale < peso_ottimo:
                                    peso_ottimo = peso_totale
                                    cammino_ottimo = cammino_minimo
                    except nx.NetworkXNoPath:
                        continue
        sentieri = []
        for i in range(len(cammino_ottimo) - 1):
            nodo_iniziale = cammino_ottimo[i]
            nodo_fine = cammino_ottimo[i + 1]
            peso_arco = nuovo_grafo[nodo_iniziale][nodo_fine]['peso']
            sentieri.append({"Partenza": nodo_iniziale, "Arrivo": nodo_fine, "Peso": peso_arco})
        return sentieri




    # METODO RICORSIONE
    def get_cammino_minimo_ricorsione(self, soglia):
        # Inizializzazione delle variabili per la soluzione ottima globale
        self.cammino_ottimo = []
        self.peso_ottimo = float('inf')

        # Poiché non abbiamo un nodo di partenza fisso, proviamo a far partire
        # la ricorsione da OGNI nodo del grafo per trovare il cammino minimo globale.
        # Creiamo una copia dei nodi per iterare
        nodi = list(self.G.nodes())

        for nodo_partenza in nodi:
            # Iniziamo la ricorsione con una lista che contiene il nodo di partenza
            parziale = [nodo_partenza]
            self._ricorsione(parziale, soglia, 0)

        # A fine ricerca, formattiamo il risultato per il Controller
        # Il controller si aspetta una lista di dizionari con keys: 'inizio', 'fine', 'peso'
        result = []
        if self.cammino_ottimo:
            for i in range(len(self.cammino_ottimo) - 1):
                u = self.cammino_ottimo[i]
                v = self.cammino_ottimo[i + 1]
                # Recuperiamo il peso dell'arco dal grafo
                w = self.G[u][v]['peso']
                result.append({"inizio": u, "fine": v, "peso": w})

        return result

    def _ricorsione(self, parziale, soglia, peso_attuale):
        if peso_attuale >= self.peso_ottimo:
            return

        if len(parziale) >= 3:
            self.peso_ottimo = peso_attuale
            self.cammino_ottimo = list(parziale)
            return

        # 3. ESPLORAZIONE VICINI
        ultimo_nodo = parziale[-1]

        for vicino in self.G.neighbors(ultimo_nodo):
            if vicino not in parziale:
                peso_arco = self.G[ultimo_nodo][vicino]['peso']

                if peso_arco > soglia:
                    parziale.append(vicino)
                    self._ricorsione(parziale, soglia, peso_attuale + peso_arco)
                    parziale.pop()