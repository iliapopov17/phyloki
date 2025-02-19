#!/usr/bin/env python

import argparse
from Bio import Entrez
from read_accession_file import read_accession_file


def fetch_organism_names(email, accession_numbers):
    """
    Retrieves organism names and accession versions from NCBI for a list of accession numbers.

    Args:
        email (str): User email (required for NCBI API requests).
        accession_numbers (list of str): List of accession numbers to query.

    Returns:
        dict: A dictionary where the keys are accession versions and the values are organism names.

    The dictionary is populated with organism names and corresponding versioned accession numbers for each accession provided.
    """
    Entrez.email = email
    organism_dict = {}

    for accession in accession_numbers:
        try:
            handle = Entrez.efetch(db="nucleotide", id=accession, retmode="xml")
            records = Entrez.read(handle)
            organism_name = records[0]["GBSeq_organism"]
            accession_version = records[0]["GBSeq_accession-version"]

            organism_dict[accession_version] = organism_name
            handle.close()
        except IndexError:
            print(f"No data found for {accession}")
        except KeyError:
            print(f"Missing organism name or accession version for {accession}")
        except Exception as e:
            print(f"Error retrieving data for {accession}: {e}")
            handle.close()

    return organism_dict


def get_organisms(email, input_filename, output_filename):
    """
    Fetches organism names and their corresponding accession versions, then writes the data to a file.

    Args:
        email (str): User email (required for NCBI API requests).
        input_filename (str): Path to a TXT file containing accession numbers (one per line).
        output_filename (str): Path to save the organism names and accession versions.

    The output file will contain the accession version and organism name on each line, formatted as:
    <accession_version> <organism_name>
    """
    accession_numbers = read_accession_file(input_filename)
    organism_dict = fetch_organism_names(email, accession_numbers)

    with open(output_filename, "w") as file:
        for accession_version, organism in organism_dict.items():
            file.write(f"{accession_version} {organism}\n")

    print(f"Metadata retrieval complete.\nFile saved to {output_filename}")


if __name__ == "__main__":
    # Use argparse to handle command-line arguments
    parser = argparse.ArgumentParser(
        description="Fetch organism names and accession versions from NCBI."
    )
    parser.add_argument(
        "-email",
        "--email",
        required=True,
        help="User email (required for NCBI API requests)",
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Path to TXT file containing accession numbers (one per line)",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="File path to save organism names and accession versions",
    )

    args = parser.parse_args()

    get_organisms(args.email, args.input, args.output)
