# INSERTIONS DE CLIENTS.CSV ET MARKETING.CSV DANS LA BASE DE DONNÉES CASSANDRA AVEC PYTHON

## Sommaire

- [Description](#description)
- [Fichiers](#fichiers)
- [Utilisation des scripts](#utilisation-des-scripts)

## NB : cette partie se fait après la correction des fichiers

## Description

Ce dossier contient les scripts Python pour insérer les données des fichiers `Clients.csv` et `Marketing.csv` dans la base de données Cassandra.

## Fichiers

- `Clients.py` : Script  pour insérer les données du fichier `Clients.csv` dans la base de données Cassandra.
- `Marketing.py` : Script pour insérer les données du fichier `Marketing.csv` dans la base de données Cassandra.

## Utilisation des scripts

D'abord assurez-vous que vous avez bien installé cassandra sur votre machine soit en docker ou en local.

1. Connectez-vous à la base de données Cassandra en utilisant la commande suivante :

    ```bash
     #cas docker  (image docker cassandra)

     # * Prérequis : Avoir installé docker sur votre machine
        # installer python et cassandra 
        docker pull cassandra:latest

        docker pull python:3.9-slim

      # - 1 on crée un container cassandra
        docker network create cassandra-network

        docker run --name cassandra-container -p 9042:9042 -d cassandra:latest --network cassandra-network
        #verifier que le container est bien lancé
        docker ps 
        
        # - 2 on se connecte au container (si la commande renvoie error alors il faut attendre quelques secondes)
        docker exec -it cassandra-container cqlsh
        
        # - 3 on crée la keyspace
        CREATE KEYSPACE IF NOT EXISTS "bigdata_exam" WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};
        
        # - 4 quitter cqlsh
        exit

        # - 5 Lancer un container python sur le même réseau
        docker run  -it --network cassandra-network --name python-marketing-m  python:3.9-slim bash
        
        
        #cas local (machine physique)
        # - 1 on lance cassandra
        cqlsh
        
        # - 3 on crée la keyspace
        CREATE KEYSPACE IF NOT EXISTS "bigdata_exam" WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};

        # - 4 quitter cqlsh
        exit
        
    ```

2. **Deplacement des fichiers** `Clients.csv` et `Marketing.csv` corriger dans le dossier `insertion_client_marketing`.

 Copier les fichiers `Clients.csv` et `Marketing.csv` dans le dossier `insertion_client_marketing`.

3 . **Deplacement du dossier dans le container `python-marketing-m`** (pour le cas docker  uniquement)

    ```bash
    #cas docker
    #verifier que le container est bien lancé
    docker ps
    # verifier que le container python-marketing-m est bien lancé dans la sortie de la commande précédente sinon lancer le container avec la commande suivante : docker run  -it --network cassandra-network --name python-marketing-m  python:3.9-slim bash

    #copier le dossier insertion_client_marketing dans le container python-marketing-m, remplacer 'chemin_du_dossier' par le chemin du dossier insertion_client_marketing dans votre machine

    docker cp chemin_du_dossier python-marketing-m:/app

    #entrer dans le container python-marketing-m
    docker exec -it python-marketing-m bash

    #mettre à jour les packages
    apt-get update

    #installer le driver cassandra
    pip install --upgrade pip
    pip install cassandra-driver

    #se deplacer dans le dossier app 
    cd app 

    #executer les scripts python
    python Clients.py #absorver la sortie qui est un message de confirmation "Row inserted"  si tout s'est bien passé à la fin

    python Marketing.py #absorver la sortie qui est un message de confirmation "Row inserted"  si tout s'est bien passé à la fin

    #sortir du container
    exit
    ```

4. **Verifiez** que les données ont été insérées dans la base de données Cassandra en utilisant la commande suivante :

    ```bash
    #cas docker
    docker exec -it cassandra-container cqlsh
    USE bigdata_exam;
    SELECT * FROM clients;
    SELECT * FROM marketing;
    ```

    ```bash
    #cas local
    cqlsh
    USE bigdata_exam;
    SELECT * FROM clients;
    SELECT * FROM marketing;
    ```

7. **Déconnectez-vous** de la base de données Cassandra en utilisant la commande suivante :

```bash
    #stopper le container
    docker stop cassandra-db
```
