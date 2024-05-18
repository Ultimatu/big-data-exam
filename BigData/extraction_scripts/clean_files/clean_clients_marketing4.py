import csv


def convert_csv_to_csv(input_file, output_file, id_column_name):
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        headers = next(reader)
        headers.insert(0, id_column_name)
        writer.writerow(headers)
        
        id = 1
        for row in reader:
            row.insert(0, id)
            id += 1
            # Clean and correct the data
            for i in range(len(row)):
                value = row[i].strip()
                if i == 2:  # Column for gender
                    if value.lower() == "homme":
                        row[i] = "H"
                    elif value.lower() in ["femme", "féminin", "f�minin"]:
                        row[i] = "F"
                elif i in [4, 7]:  # Columns with invalid characters
                    row[i] = value.replace("�", "é")
                if value in ["?", ""]:
                    row[i] = "N/D"
            
            writer.writerow(row)

def main():
    clients_file = "/home/tonde/Bureau/bigdataExam/Data_extraction/datas/Clients_2.csv"
    clients_corrected_csv = "/home/tonde/Bureau/bigdataExam/Data_extraction/datas/Clients_corrected.csv"
    id_column_name = "ClientID"
    convert_csv_to_csv(clients_file, clients_corrected_csv, id_column_name)

if __name__ == "__main__":
    main()
