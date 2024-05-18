import pandas as pd

# Read the CSV file with explicit encoding
immatriculation = pd.read_csv("/home/tonde/Bureau/bigdataExam/Data_extraction/datas/Immatriculations.csv", header=1, sep=",", decimal=".", encoding="ISO-8859-1")

# Split the dataframe into two parts
immatriculation1 = immatriculation.iloc[:1000000]
immatriculation2 = immatriculation.iloc[1000000:2000000]

# Write each part to separate CSV files
immatriculation1.to_csv('/home/tonde/Bureau/bigdataExam/Data_extraction/datas/Immatriculations1.csv', index=False, quoting=False, encoding="ISO-8859-1")
immatriculation2.to_csv('/home/tonde/Bureau/bigdataExam/Data_extraction/datas/Immatriculations2.csv', index=False, quoting=False, encoding="ISO-8859-1")
