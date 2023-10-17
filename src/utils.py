def read_ids_from_file(filename) -> list:
    f = open(filename, "r")
    ret = list()
    for row in f.readlines():
        ret.append(row.strip())
    return ret
