from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import csv


class Clients:
    def __init__(self, keyspace, file_path, container_name="cassandra-container"):
        self.keyspace = keyspace
        self.file_path = file_path
        self.cluster = Cluster([container_name])
        self.session = self.cluster.connect(self.keyspace)

    def init_clients_tables_and_data(self):
        self.drop_table_clients()
        self.create_table_clients()
        self.load_clients_data_from_file(self.file_path)

    def drop_table_clients(self):
        statement = "DROP TABLE IF EXISTS Clients"
        self.execute_ddl(statement)

    def create_table_clients(self):
        statement = """
            CREATE TABLE Clients (
                CLIENTID int PRIMARY KEY,
                AGE int,
                SEXE text,
                TAUX int,
                SITUATION_FAMILIALE text,
                NBR_ENFANT int,
                VOITURE_2 text,
                IMMATRICULATION text
            )
        """
        self.execute_ddl(statement)

    def load_clients_data_from_file(self, file_path):
        print("Chargement des clients...")
        try:
            with open(file_path, mode='r') as file:
                print('Reading file...')
                reader = csv.reader(file)
                print('Skipping header row...')
                i = 0
                for row in reader:
                    i += 1
                    try:
                        print('ROW: ', row)
                        if row[1] == "N/D" or row[3] == "N/D" or row[5] == "N/D" or i == 1:
                            continue
                        clientid = int(row[0])
                        print('ID is clean')
                        age = int(row[1])
                        print('AGE is clean')
                        sexe = row[2]
                        print('SEXE is clean')
                        taux = int(row[3])
                        print('TAUX is clean')
                        s_familiale = row[4]
                        print('SITUATION_FAMILIALE is clean')
                        nb_enfants_a_charge = int(row[5])
                        print('NBR_ENFANT is clean')
                        voiture_2 = row[6]
                        print('VOITURE_2 is clean')
                        immatriculation = row[7]
                        print('IMMATRICULATION is clean')
                        self.insert_a_client_row(
                            clientid, age, sexe, taux, s_familiale, nb_enfants_a_charge, voiture_2, immatriculation)
                        print('Row inserted')
                    except ValueError as e:
                        print(f"Error converting row: {row}. Error: {e}")
        except IOError as e:
            print("Erreur : ", e)

    def insert_a_client_row(self, clientid, age, sexe, taux, s_familiale, nb_enfants_a_charge, voiture_2, immatriculation):
        statement = """
            INSERT INTO Clients (CLIENTID, AGE, SEXE, TAUX, SITUATION_FAMILIALE, NBR_ENFANT, VOITURE_2, IMMATRICULATION) 
            VALUES (%s, %s, '%s', %s, '%s', %s, '%s', '%s')
        """ % (clientid, age, sexe, taux, s_familiale, nb_enfants_a_charge, voiture_2, immatriculation)

        print('Creating SimpleStatement...')
        print('Statement: ', statement)
        # Créer un objet SimpleStatement à partir de la chaîne de requête
        simple_statement = SimpleStatement(statement)
        print('SimpleStatement created')
        # Passer uniquement l'objet SimpleStatement à la méthode execute
        self.session.execute(simple_statement)


    def execute_ddl(self, statement):
        self.session.execute(statement)


if __name__ == "__main__":
    try:
        clients = Clients(keyspace="bigdata_exam", file_path="Client.csv")
        clients.init_clients_tables_and_data()
    except Exception as e:
        print("Erreur : ", e)
