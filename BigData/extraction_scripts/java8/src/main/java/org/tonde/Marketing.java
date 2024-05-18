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

public class Marketing {
    private final CqlSession session;
    private final String $KEYSPACE = "bigdata_exam";  // Changez ceci avec votre espace de clés
    private final String $FILE = "Marketing.csv";  // Changez ceci avec le chemin de votre fichier CSV

    public static void main(String args[]) {
        try {
            Marketing marketing = new Marketing();
            marketing.initMarketingTableAndData(marketing);
        } catch (RuntimeException e) {
            System.out.println("Erreur : " + e);
        }
    }

    Marketing() {
        session = CqlSession.builder()
                .withKeyspace($KEYSPACE)
                .build();
    }

    public void initMarketingTableAndData(Marketing marketing) {
        marketing.dropTableMarketing();
        marketing.createTableMarketing();
        marketing.loadMarketingDataFromFile($FILE);
    }

    public void dropTableMarketing() {
        String statement = "DROP TABLE IF EXISTS Marketing";
        executeDDL(statement);
    }

    public void createTableMarketing() {
        String statement = "CREATE TABLE Marketing ("
                + "ID int PRIMARY KEY,"
                + "Product text,"
                + "Segment text,"
                + "Revenue int)";
        executeDDL(statement);
    }

    void loadMarketingDataFromFile(String marketingDataFileName) {
        InputStreamReader ipsr;
        BufferedReader br = null;
        InputStream ips;
        String ligne;

        System.out.println("Chargement des données marketing...");

        try {
            ips = Files.newInputStream(Paths.get(marketingDataFileName));
            ipsr = new InputStreamReader(ips);
            br = new BufferedReader(ipsr);
            int i = 0;
            while ((ligne = br.readLine()) != null) {
                ArrayList<String> marketingRecord = new ArrayList<>();
                StringTokenizer val = new StringTokenizer(ligne, ",");
                i += 1;
                while (val.hasMoreTokens()) {
                    marketingRecord.add(val.nextToken());
                }
                if (marketingRecord.get(0).equals("ID") || i == 1) {
                    continue;
                }

                int id = Integer.parseInt(marketingRecord.get(0));
                String product = marketingRecord.get(1);
                String segment = marketingRecord.get(2);
                int revenue = Integer.parseInt(marketingRecord.get(3));
                this.insertMarketingRow(id, product, segment, revenue);
            }
        } catch (IOException e) {
            System.out.println("Erreur : " + e);
        } finally {
            try {
                if (br != null) {
                    br.close();
                }
            } catch (IOException e) {
                System.out.println("Erreur : " + e);
            }
        }
    }

    private void insertMarketingRow(int id, String product, String segment, int revenue) {
        String statement = "INSERT INTO Marketing (ID, Product, Segment, Revenue) " +
                "VALUES (?, ?, ?, ?)";
        session.execute(SimpleStatement.builder(statement)
                .addPositionalValue(id)
                .addPositionalValue(product)
                .addPositionalValue(segment)
                .addPositionalValue(revenue)
                .build());
    }

    public void executeDDL(String statement) {
        session.execute(statement);
    }
}
