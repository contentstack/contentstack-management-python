
def read_file(self, file_name):
    file_path= f"tests/resources/mockContentType/{file_name}"
    infile = open(file_path, 'r')
    data = infile.read()
    infile.close()
    return data
