from database.DB_connect import DBConnect
from model.Rifugio import Rifugio
from model.Sentiero import Sentiero


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    @staticmethod
    def read_rifugi():
        conn = DBConnect.get_connection()
        result = []

        if conn is None:
            print("❌ Errore connessione DB")
            return result

        try:
            cursor = conn.cursor(dictionary=True)
            # Verifica che la tabella si chiami 'rifugio' nel tuo DB
            query = """ SELECT * FROM rifugio """
            cursor.execute(query)

            for row in cursor:
                result.append(Rifugio(
                    id=row['id'],
                    nome=row['nome'],
                    localita=row['localita']
                ))
            cursor.close()
        except Exception as e:
            print(f"Errore lettura rifugi: {e}")
        finally:
            if conn:
                conn.close()
        return result

    @staticmethod
    def read_sentieri():
        conn = DBConnect.get_connection()
        result = []

        if conn is None:
            return result

        try:
            cursor = conn.cursor(dictionary=True)
            # Verifica che la tabella si chiami 'connessione' nel tuo DB
            query = """ SELECT * FROM connessione """
            cursor.execute(query)

            for row in cursor:
                result.append(Sentiero(
                    id=row['id'],
                    id_rifugio1=row['id_rifugio1'],
                    id_rifugio2=row['id_rifugio2'],
                    distanza=row['distanza'],
                    difficolta=row['difficolta'],
                    anno=row['anno']
                ))
            cursor.close()
        except Exception as e:
            print(f"Errore lettura sentieri: {e}")
        finally:
            if conn:
                conn.close()
        return result


