package org.tonde;

import com.datastax.oss.driver.api.core.CqlSession;
import com.datastax.oss.driver.api.core.cql.SimpleStatement;


import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.StringTokenizer;

public class Clients {
    private final CqlSession session;
    // Le nom de l'espace de clés
    private final String $KEYSPACE = "bigdata_exam";  // Changez ceci avec votre espace de clés
    // Le fichier contenant les données des clients
    private final String $FILE = "Clients.csv";  // Changez ceci avec le chemin de votre fichier CSV

    public static void main(String args[]) {
        try {
            Clients arb = new Clients();
            arb.initClientsTablesAndData(arb);
        } catch (RuntimeException e) {
            System.out.println("Erreur : " + e);
        }
    }

    /**
     * Constructeur
     */
    Clients() {
        session = CqlSession.builder()
                .withKeyspace($KEYSPACE)
                .build();
    }

    /**
     * Initialise la table des clients et charge les données à partir d'un fichier
     *
     * @param arb l'objet Clients
     */
    public void initClientsTablesAndData(Clients arb) {
        arb.dropTableClients();
        arb.createTableClients();
        arb.loadClientsDataFromFile($FILE);
    }

    /**
     * Supprime la table Clients
     */
    public void dropTableClients() {
        String statement = "DROP TABLE IF EXISTS Clients";
        executeDDL(statement);
    }

    /**
     * Crée la table Clients
     */
    public void createTableClients() {
        String statement = "CREATE TABLE Clients ("
                + "CLIENTID int PRIMARY KEY,"
                + "AGE int,"
                + "SEXE text,"
                + "TAUX int,"
                + "SITUATION_FAMILIALE text,"
                + "NBR_ENFANT int,"
                + "VOITURE_2 text,"
                + "IMMATRICULATION text)";
        executeDDL(statement);
    }

    /**
     * Charge les données des clients à partir d'un fichier
     *
     * @param clientDataFileName le nom du fichier contenant les données des clients
     */
    void loadClientsDataFromFile(String clientDataFileName) {
        InputStreamReader ipsr;
        BufferedReader br = null;
        InputStream ips;
        String ligne;

        System.out.println("Chargement des clients...");

        try {
            ips = Files.newInputStream(Paths.get(clientDataFileName));
            ipsr = new InputStreamReader(ips);
            br = new BufferedReader(ipsr);
            int i = 0;
            while ((ligne = br.readLine()) != null) {
                ArrayList<String> clientRecord = new ArrayList<>();
                StringTokenizer val = new StringTokenizer(ligne, ",");
                i += 1;
                while (val.hasMoreTokens()) {
                    clientRecord.add(val.nextToken());
                }
                if (clientRecord.get(1).equals("N/D")
                        || clientRecord.get(3).equals("N/D")
                        || clientRecord.get(5).equals("N/D") || clientRecord.get(0).equals("ClientId") || i == 1) {
                    continue;
                }

                int clientid = Integer.parseInt(clientRecord.get(0)) - 1;
                int age = Integer.parseInt(clientRecord.get(1));
                String sexe = clientRecord.get(2);
                int taux = Integer.parseInt(clientRecord.get(3));
                String SFamiliale = clientRecord.get(4);
                int nbEnfantsAcharge = Integer.parseInt(clientRecord.get(5));
                String voiture_2 = clientRecord.get(6);
                String immatriculation = clientRecord.get(7);
                this.insertAClientRow(clientid, age, sexe, taux, SFamiliale, nbEnfantsAcharge, voiture_2, immatriculation);
            }
        } catch (IOException e) {
            System.out.println("Erreur : " + e);
        }
    }

    /**
     * Insère une ligne dans la table Clients
     *
     * @param clientid          l'identifiant du client
     * @param age               l'age du client
     * @param sexe              le sexe du client
     * @param taux              le taux du client
     * @param SFamiliale        la situation familiale du client
     * @param nbEnfantsAcharge  le nombre d'enfants à charge du client
     * @param voiture_2         la voiture du client
     * @param immatriculation   l'immatriculation du client
     */
    private void insertAClientRow(int clientid, int age, String sexe, int taux, String SFamiliale, int nbEnfantsAcharge,
                                  String voiture_2, String immatriculation) {
        String statement = "INSERT INTO Clients (CLIENTID, AGE, SEXE, TAUX, SITUATION_FAMILIALE, NBR_ENFANT, VOITURE_2, IMMATRICULATION) " +
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
        session.execute(SimpleStatement.builder(statement)
                .addPositionalValue(clientid)
                .addPositionalValue(age)
                .addPositionalValue(sexe)
                .addPositionalValue(taux)
                .addPositionalValue(SFamiliale)
                .addPositionalValue(nbEnfantsAcharge)
                .addPositionalValue(voiture_2)
                .addPositionalValue(immatriculation)
                .build());
    }

    /**
     * Exécute une instruction DDL
     *
     * @param statement l'instruction DDL à exécuter
     */
    public void executeDDL(String statement) {
        session.execute(statement);
    }
}
