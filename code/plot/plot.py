import csv

def read_similarity_file(file):
    with open(file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            row.pop(-1)

            city_name = ""

            if len(row) == 0:
                print("empty row")
            elif len(row) == 1:
                city_name = row[0]
            elif row[0] == "categoria":
                continue
            else
                category = row[0]
                wup_best = row[1]
                wup_sim = row[2]
                path_best = row[3]
                path_sim = row[4]
                lch_best = row[5]
                lch_sim = row[6]
                res_best = row[7]
                res_sim = row[8]
                jcn_best = row[9]
                jcn_sim = row[10]
                lin_best = row[11]
                lin_sim = row[12]
                

output_dir = "../output/"
similarityFile = output_dir + "similaridade.csv"

read_similarity_file(similarityFile)