from database.DB_connect import DBConnect
from model.rifugio import Rifugio
from model.connessione import Connessione

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO

    @staticmethod
    def get_all_rifugi(year):
        conn = DBConnect.get_connection()
        rifugi = {}

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT r.*
                FROM rifugio r, connessione c
                WHERE (c.id_rifugio1 = r.id or c.id_rifugio2 = r.id)
                AND c.year = %s
                """

        try:
            cursor.execute(query, (year,))
            for row in cursor:
                rifugi[row['id']] = Rifugio(**row)
            conn.close()
            cursor.close()
            return rifugi
        except Exception:
            print("Errore nell'esecuzione della query.")
            return None


    @staticmethod
    def get_all_connessioni(rifugi, year):
        conn = DBConnect.get_connection()
        sentieri = {}

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM connessione c
                WHERE year = %s
                """
        try:
            cursor.execute(query, (year,))
            for row in cursor:
                rifugio1 = rifugi.get(row['id_rifugio1'])
                rifugio2 = rifugi.get(row['id_rifugio2'])

                if rifugio1 is not None and rifugio2 is not None and (rifugio1, rifugio2) not in sentieri:
                    sentieri[rifugio1, rifugio2] = Connessione(
                        rifugio1,
                        rifugio2,
                        row['Distanza'],
                        row['Difficolta'],
                        row['Durata']
                    )

            conn.close()
            cursor.close()
            return sentieri
        except Exception:
            print("Errore nell'esecuzione della query.")
            return None


























