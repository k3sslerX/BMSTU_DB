import csv


def get_csv(array, filename):
    with open(f"csv_files/{filename}", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(array)
    print("{} - Successfully".format(filename))
