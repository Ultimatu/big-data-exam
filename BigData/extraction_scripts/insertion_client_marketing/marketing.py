from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import csv


class Marketings:
    def __init__(self, keyspace, file_path, container_name="cassandra-container"):
        self.keyspace = keyspace
        self.file_path = file_path
        self.cluster = Cluster([container_name])
        self.session = self.cluster.connect(self.keyspace)

    def init_marketings_tables_and_data(self):
        self.drop_table_marketings()
        self.create_table_marketings()
        self.load_marketings_data_from_file(self.file_path)

    def drop_table_marketings(self):
        statement = "DROP TABLE IF EXISTS Marketings"
        self.execute_ddl(statement)

    def create_table_marketings(self):
        statement = """
            CREATE TABLE Marketings (
                MARKETINGID int PRIMARY KEY,
                AGE int,
                SEXE text,
                TAUX int,
                SITUATION_FAMILIALE text,
                NBR_ENFANT int,
                VOITURE_2 text,
            )
        """
        self.execute_ddl(statement)

    def load_marketings_data_from_file(self, file_path):
        print("Chargement des marketings...")
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
                        if i == 1:
                            continue
                        marketingid = int(row[0])
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
                        self.insert_a_client_row(
                            marketingid, age, sexe, taux, s_familiale, nb_enfants_a_charge, voiture_2)
                        print('Row inserted')
                    except ValueError as e:
                        print(f"Error converting row: {row}. Error: {e}")
        except IOError as e:
            print("Erreur : ", e)

    def insert_a_client_row(self, marketingid, age, sexe, taux, s_familiale, nb_enfants_a_charge, voiture_2):
        statement = """
            INSERT INTO marketings (MARKETINGID, AGE, SEXE, TAUX, SITUATION_FAMILIALE, NBR_ENFANT, VOITURE_2) 
            VALUES (%s, %s, '%s', %s, '%s', %s, '%s')
        """ % (marketingid, age, sexe, taux, s_familiale, nb_enfants_a_charge, voiture_2)

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
        marketings = Marketings(keyspace="bigdata_exam", file_path="Marketing.csv")
        marketings.init_marketings_tables_and_data()
    except Exception as e:
        print("Erreur : ", e)
