# CORRECTION DES FICHIERS

## Description

Ce dossier contient les scripts de nettoyage des fichiers bruts.

## Fichiers

- Pour le fichier Clients.csv et Marketing.csv, le script de nettoyage est `clean_clients_marketing.py`
- Pour le fichier Immatriculation.csv, le script de nettoyage est `split_immatriculation.py`

## Utilisation du script `clean_clients_marketing.py`

Ouvrez le fichier, dans la fonction `main()`:
- Modifiez les variables `clients_file`, `clients_corrected_csv` et `id_column_name` pour correspondre à l'emplacement du fichier brut, l'emplacement du fichier corrigé et le nom de la colonne ID respectivement (Si le fichier est client , laissé le nom de la colonne ID à `ClientID` et si le fichier est Marketing, laissé le nom de la colonne ID à `MarketingID`) pour le bon fonctionnement des scripts java qui vont utiliser ces fichiers.

### Ce que fait le script `clean_clients_marketing.py`


- Le script prend en entrée un fichier brut et un fichier de sortie.
- Il ajoute une colonne ID à la première position de chaque ligne.
- Il corrige les données en remplaçant les valeurs invalides par des valeurs valides.
- Il remplace les valeurs manquantes par "N/D" qui signifie "Non Disponible".

## Utilisation du script `split_immatriculation.py`

Ouvrez le fichier
- Modifiez les variables `immatriculation_file`, `immatriculation1_csv` et `immatriculation2_csv` pour correspondre à l'emplacement du fichier brut, l'emplacement du fichier corrigé et le nom de la colonne ID respectivement.

### Ce que fait le script `split_immatriculation.py`

- Le script prend en entrée un fichier brut et le divise en deux fichiers de sortie.
- Il divise le fichier brut en deux parties égales.
- Il écrit chaque partie dans un fichier CSV séparé.

## Suite

- Nous allons inserer les données de client et Marketing dans la base de données  cassandra. Cela se fera dans le dossier insertion_marketing