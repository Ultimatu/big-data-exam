from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from bson import Type
import csv

class Catalogue:
    """Classe pour insérer les données du catalogue dans la base de données MongoDB"""

    @staticmethod
    def create_coll_catalogue(db: Database):
        """Crée la collection Catalogue avec un schéma de validation"""
        validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["Marque", "Nom", "Puissance", "Longueur", "NbPlaces", "NbPortes", "Couleur", "Occasion", "Prix"],
                "properties": {
                    "Marque": {"bsonType": "string"},
                    "Nom": {"bsonType": "string"},
                    "Puissance": {"bsonType": "double"},
                    "Longueur": {"bsonType": "string"},
                    "NbPlaces": {"bsonType": "int"},
                    "NbPortes": {"bsonType": "int"},
                    "Couleur": {"bsonType": "string"},
                    "Occasion": {"bsonType": "bool"},
                    "Prix": {"bsonType": "double"}
                }
            }
        }

        db.drop_collection("Catalogue")
        db.create_collection("Catalogue", validator=validator)

    @staticmethod
    def insert_catalogue(catalogue_arr, collection: Collection):
        """Insère les données du catalogue dans la collection Catalogue"""

        for vehicule in catalogue_arr:
            doc = {
                "Marque": vehicule[0],
                "Nom": vehicule[1],
                "Puissance": float(vehicule[2]),
                "Longueur": vehicule[3],
                "NbPlaces": int(vehicule[4]),
                "NbPortes": int(vehicule[5]),
                "Couleur": vehicule[6],
                "Occasion": vehicule[7].lower() == 'true',
                "Prix": float(vehicule[8])
            }
            collection.insert_one(doc)

def load_catalogue_data_from_file(file_path):
    """Charge les données du catalogue depuis un fichier CSV"""
    catalogue_arr = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            catalogue_arr.append(row)
    return catalogue_arr

if __name__ == "__main__":
    # client = MongoClient("mongodb://localhost:27017/")
    #docker 
    client = MongoClient("mongodb://mongo:27017/")
    db = client["bigdata_exam"]

    Catalogue.create_coll_catalogue(db)
    catalogue_data = load_catalogue_data_from_file("Catalogue.csv")
    collection = db["Catalogue"]
    Catalogue.insert_catalogue(catalogue_data, collection)
