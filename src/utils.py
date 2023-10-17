import csv


def read_ids_from_file(filename) -> list:
    f = csv.reader(open(filename, "r"))
    ret = list()
    for row in f:
        ret.append(row[11])
    return ret


if __name__ == "__main__":
    ids = read_ids_from_file("../data.csv")
    print(ids)
    print(len(ids))
