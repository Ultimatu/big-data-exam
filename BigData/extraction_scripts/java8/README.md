# INSERTIONS DE CLIENTS.CSV ET MARKETING.CSV DANS LA BASE DE DONNÉES CASSANDRA AVEC JAVA

## Description

Ce dossier contient les scripts Java pour insérer les données des fichiers `Clients.csv` et `Marketing.csv` dans la base de données Cassandra.


## Fichiers

- `Clients.java` : Script Java pour insérer les données du fichier `Clients.csv` dans la base de données Cassandra.
- `Marketing.java` : Script Java pour insérer les données du fichier `Marketing.csv` dans la base de données Cassandra.

## Utilisation des scripts

D'abord assurez-vous que vous avez bien installé cassandra sur votre machine soit en docker ou en local.

1. Connectez-vous à la base de données Cassandra en utilisant la commande suivante :

    ```bash
     #cas docker  (image docker cassandra)
      # - 1 on crée un container cassandra
        docker run --name cassandra-db -p 9042:9042 -d cassandra:latest
        #verifier que le container est bien lancé
        docker ps 
        
        # - 2 on se connecte au container (si la commande renvoie error alors il faut attendre quelques secondes)
        docker exec -it cassandra-db cqlsh
        
        # - 3 on crée la keyspace
        CREATE KEYSPACE IF NOT EXISTS "bigdata_exam" WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};
        
        # - 4 quitter cqlsh
        exit
        
        
        #cas local (machine physique)
        # - 1 on lance cassandra
        cqlsh
        
        # - 3 on crée la keyspace
        CREATE KEYSPACE IF NOT EXISTS "bigdata_exam" WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};
        
    ```

2. **Ouvrez** le dossier `java8` dans (intellij ou eclipse) .
   
   Installer les dépendances nécessaires pour le projet en utilisant le fichier `pom.xml`.
    
3. **Configuration du chemin des fichiers** :
   
   - Ouvrez le fichier `Clients.java` et `Marketing.java` et modifiez le chemin des fichiers `Clients.csv` et `Marketing.csv` en 
   fonction de l'emplacement de ces fichiers sur votre machine dans les variable $FILE et aussi $KEYSPACE si vous avez changé le nom de la keyspace.

4. **Exécutez** le script `Clients.java` pour insérer les données du fichier `Clients.csv` dans la base de données Cassandra.


5. **Exécutez** le script `Marketing.java` pour insérer les données du fichier `Marketing.csv` dans la base de données Cassandra.


6. **Vérifiez** que les données ont été insérées dans la base de données Cassandra en utilisant la commande suivante :

    ```bash
    #cas docker
    docker exec -it cassandra-db cqlsh
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
   


### NB : cette partie se fait après la correction des fichiers


