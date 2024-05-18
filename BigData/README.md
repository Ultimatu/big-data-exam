# Extraction des données

L'extraction des données et leurs traitements
Source Orcale noSQL
Import des données
Pour notre projet nous avons décidé de placer les données clients et marketing dans le serveur Oracle NOSQL. Pour cela nous avons développé deux scripts d'extraction : Clients.java et Marketing.java. Ces deux scripts sont présents dans le dossier "programmesExtraction". Pour les utiliser, veuillez suivre les instructions suivantes :

placer les fichiers Clients.txt, Marketing.txt, Clients.java et Marketing.java dans le repertoire de la machine vagrant.
connecter vous à la machine vagrant avec la commande
vagrant ssh
Démarrer le serveur Oracle NOSQL (KV Store) avec la commande
nohup java -Xmx64m -Xms64m -jar $KVHOME/lib/kvstore.jar kvlite -secure-config disable -root $KVROOT &
réaliser l'import de Marketing
javac -g -cp $KVHOME/lib/kvclient.jar:. Marketing.java
java -cp $KVHOME/lib/kvclient.jar:. Marketing
réaliser l'import de Clients
javac -g -cp $KVHOME/lib/kvclient.jar:. Clients.java
java -cp $KVHOME/lib/kvclient.jar:. Clients
Nous allons maintenant créer les tables externes sur HIVE pour pouvoir accéder aux données.

Création des tables externes sur HIVE
Pour commencer, nous devons démarrer le serveur HIVE avec les commandes suivantes :

start-dfs.sh
start-yarn.sh
nohup hive --service metastore > /dev/null &
nohup hiveserver2 > /dev/null &
maintenant nous accédons à la console HIVE avec la commande : (il est possible que la commande ne fonctionne pas directement à cause du temps de lancement le mieux est d'attendre quelques secondes et de lancer la commande)
beeline -u jdbc:hive2://localhost:10000 vagrant
USE DEFAULT;
script de création de la table Marketing
CREATE EXTERNAL TABLE IF NOT EXISTS MARKETING_H_EXT (
MARKETINGID INTEGER,
AGE INTEGER,
SEXE STRING,
TAUX INTEGER,
SITUATION_FAMILIALE STRING,
NBR_ENFANT INTEGER,
VOITURE_2 STRING
)
STORED BY 'oracle.kv.hadoop.hive.table.TableStorageHandler'
TBLPROPERTIES (
"oracle.kv.kvstore" = "kvstore",
"oracle.kv.hosts" = "localhost:5000",
"oracle.kv.tableName" = "Marketing"
);
script de création de la table Clients
CREATE EXTERNAL TABLE IF NOT EXISTS Clients_H_EXT (
ClIENTID INTEGER,
AGE INTEGER,
SEXE STRING,
TAUX INTEGER,
SITUATION_FAMILIALE STRING,
NBR_ENFANT INTEGER,
VOITURE_2 STRING,
IMMATRICULATION STRING
)
STORED BY 'oracle.kv.hadoop.hive.table.TableStorageHandler'
TBLPROPERTIES (
"oracle.kv.kvstore" = "kvstore",
"oracle.kv.hosts" = "localhost:5000",
"oracle.kv.tableName" = "clients"
);
Source Mongo DB
Import des données
Pour notre projet nous avons décidé de placer les données de Catalogue et d'Immatriculations dans le serveur Mongo DB.

Pour réaliser l'import des données on va utiliser l'utilitaire mongoimport.

On lance MongoDB :

sudo systemctl start mongod
On se connecte ensuite au MongoDB Client

mongo
On execute la serie des commandes suivante :

// Créer la BDD TPA
use TPA
// Créer les deux collections "Immatriculation" "Catalogue" :
db.createCollection("Immatriculation")
db.createCollection("Catalogue")
// Verifier les collections
show collections
//On quitte le mongo shell
quit()
Ensuite dans le bash du vagrant on lance la commande :

//On accede au repertoire ou se trouve nos CSV, dans notre cas, les fichiers sont dans le dossier partagé de Vagrant :
cd /vagrant
Ensuite, on lance la commande pour importer les données pour Catalogue :

mongoimport -d TPA -c Catalogue --type=csv --file={url}/{to}/{file}/Catalogue.csv  --headerline
De meme pour Immatriculation :

mongoimport -d TPA -c Immatriculation --type=csv --file={url}/{to}/{file}/Immatriculation.csv  --headerline
On peut verifier que les donnees on ete bien importees :

mongo
use TPA
db.Catalogue.find({})
db.Immatriculation.find({})
Création des tables externes sur HIVE
Pour démarrer et accéder à la console HIVE il faut suivre les mêmes instructions que pour la source Oracle NOSQL.

script de création de la table Catalogue
CREATE EXTERNAL TABLE catalogue_h_ext ( 
id STRING, 
Marque STRING,
Nom STRING,
Puissance DOUBLE,
Longueur STRING,
NbPlaces INT,
NbPortes INT,
Couleur STRING,
Occasion STRING,
Prix DOUBLE )
STORED BY 'com.mongodb.hadoop.hive.MongoStorageHandler'
WITH SERDEPROPERTIES('mongo.columns.mapping'='{"id":"_id", "Marque":"Marque", "Nom" : "Nom", "Puissance": "Puissance", "Longueur" : "Longueur", "NbPlaces" : "NbPlaces", "NbPortes" : "NbPortes", "Couleur" : "Couleur", "Occasion" : "Occasion", "Prix" : "Prix"}')
TBLPROPERTIES('mongo.uri'='mongodb://localhost:27017/TPA.Catalogue');
script de création de la table Immatriculation
CREATE EXTERNAL TABLE immatriculation_h_ext ( 
id STRING,
Immatriculation STRING, 
Marque STRING,
Nom STRING,
Puissance DOUBLE,
Longueur STRING,
NbPlaces INT,
NbPortes INT,
Couleur STRING,
Occasion STRING,
Prix DOUBLE )
STORED BY 'com.mongodb.hadoop.hive.MongoStorageHandler'
WITH SERDEPROPERTIES('mongo.columns.mapping'='{"id":"_id", "Immatriculation":"Immatriculation", "Marque":"Marque", "Nom" : "Nom", "Puissance": "Puissance", "Longueur" : "Longueur", "NbPlaces" : "NbPlaces", "NbPortes" : "NbPortes", "Couleur" : "Couleur", "Occasion" : "Occasion", "Prix" : "Prix"}')
TBLPROPERTIES('mongo.uri'='mongodb://localhost:27017/TPA.Immatriculation');
Hadoop Distributed File System (HDFS)
Import des données
Tout d'abord il faut mettre le fichier CO2.csv dans la machine virtuelle Ensuite assurez vous d'avoir lancer hdfs et yarn (si c'est déjà fait vous pouvez sauter cette étape) :

start-dfs.sh
start-yarn.sh
nohup hive --service metastore > /dev/null &
nohup hiveserver2 > /dev/null &
Mettre le fichier dans HDFS via la commande :

hadoop fs -put CO2.csv input/CO2.csv
Pour être sûr qu'il n'existe pas de output déjà créer :

hadoop fs -rmr output/*
Maintenant que le fichier est dans HDFS, vous pouvez lancer le script python qui va modifier le csv pour le nettoyer :

spark-submit co2Reader.py
Maintenant nous accédons à la console HIVE avec la commande :
beeline -u jdbc:hive2://localhost:10000 vagrant
USE DEFAULT;
Puis nous allons faire un lien externe vers ce fichier avec HIVE Pour être sûr que la table n'existe pas déjà :

drop table CO2_HDFS_H_EXT;
Maintenant on crée notre table externe :

CREATE EXTERNAL TABLE  CO2_HDFS_H_EXT  (MARQUE STRING,  MALUSBONUS FLOAT, REJET FLOAT, COUTENERGIE FLOAT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE LOCATION 'output/TransformationCO2';
Et voilà maintenant les données devraient être accessible depuis une commande comme celle-ci :

Select * from CO2_HDFS_H_EXT;