from pymongo import MongoClient
from pymongo.database import Database
import csv

class Immatriculation:

    @staticmethod
    def create_coll_immatriculation(db: Database):
        validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["Immatriculation", "Marque", "Nom", "Puissance", "Longueur", "NbPlaces", "NbPortes", "Couleur", "Occasion", "Prix"],
                "properties": {
                    "Immatriculation": {"bsonType": "string"},
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

        db.drop_collection("Immatriculation")
        db.create_collection("Immatriculation", validator=validator)

    @staticmethod
    def insert_immatriculation(immatriculation_arr, collection):
        for vehicule in immatriculation_arr:
            doc = {
                "Immatriculation": vehicule[0],
                "Marque": vehicule[1],
                "Nom": vehicule[2],
                "Puissance": float(vehicule[3]),
                "Longueur": vehicule[4],
                "NbPlaces": int(vehicule[5]),
                "NbPortes": int(vehicule[6]),
                "Couleur": vehicule[7],
                "Occasion": vehicule[8].lower() == 'true',
                "Prix": float(vehicule[9])
            }
            collection.insert_one(doc)

def load_immatriculation_data_from_file(file_path):
    immatriculation_arr = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            immatriculation_arr.append(row)
    return immatriculation_arr

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client["bigdata_exam"]

    Immatriculation.create_coll_immatriculation(db)
    immatriculation_data = load_immatriculation_data_from_file("Immatriculation.csv")
    collection = db["Immatriculation"]
    Immatriculation.insert_immatriculation(immatriculation_data, collection)
