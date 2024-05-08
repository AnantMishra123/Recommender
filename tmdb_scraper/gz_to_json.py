import gzip
import os

def get_file_names_by_extension(path = ".", file_extension = ".gz"):
    file_names = []
    for x in os.listdir(path):
        if x.endswith(file_extension):
            file_names.append(x)
    return file_names

def write_file(data, destination_path, file_name, encoding = "utf-8"):
    output_file_name = "/".join([destination_path, file_name])
    print(output_file_name)
    with open(output_file_name, "wb") as outfile:
        outfile.write(data.encode(encoding))

def decompress_files(files, destination_path, output_format = ".json", encoding = "utf-8"):
    for file in files:
        _file = gzip.GzipFile(file, "rb")
        content = _file.read()
        content = content.decode(encoding)
        output_file_name = "".join([file.split(".")[0], output_format])
        write_file(content, destination_path, output_file_name, encoding)

        
files = get_file_names_by_extension(path=".", file_extension=".gz")
decompress_files(files, ".", ".json")