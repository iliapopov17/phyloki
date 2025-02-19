def read_accession_file(filename):
    """
    Reads a file and extracts accession numbers, each assumed to be on a separate line.

    Args:
        filename (str): The path to the file from which accession numbers are to be read.
                        Each accession number should be on its own line, and the file should be
                        plain text with no extra formatting.

    Returns:
        list: A list of strings, where each string is an accession number extracted from the file.
              This list will be empty if the file contains no lines.
    """
    with open(filename, "r") as file:
        accession_numbers = [line.strip() for line in file.readlines()]
    return accession_numbers
