import csv


FILENAME = "/Users/tzhenghao/Downloads/links.csv"
if __name__ == "__main__":
    with open(FILENAME, newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            print(row[2])
