# This parser is for plain text files—simple and straightforward!
def parse_txt(file_path):
    """
    Reads the entire contents of a TXT file and returns it as a string.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
