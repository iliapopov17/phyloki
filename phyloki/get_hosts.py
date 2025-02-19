#!/usr/bin/env python

import argparse
from Bio import Entrez
from read_accession_file import read_accession_file


def fetch_host_info(accession_numbers, email):
    """
    Fetches host information (e.g., host species) for each accession number from NCBI Entrez.

    Args:
        accession_numbers (list): List of accession numbers to fetch host information for.
        email (str): Email address to use with NCBI Entrez tool.

    Returns:
        dict: A dictionary with accession versions as keys and host information as values.

    If no host information is found for an accession, the default value 'ND' is used.
    """
    Entrez.email = email  # Always set this to your email address
    host_info = {}

    for accession in accession_numbers:
        try:
            # Fetch the record from NCBI Entrez
            handle = Entrez.efetch(db="nucleotide", id=accession, retmode="xml")
            records = Entrez.read(handle)
            version = records[0][
                "GBSeq_accession-version"
            ]  # Retrieve the versioned accession number

            # Default host value if not found
            host = "ND"

            # Search for host information in the feature table
            if "GBSeq_feature-table" in records[0]:
                features = records[0]["GBSeq_feature-table"]
                for feature in features:
                    if feature["GBFeature_key"] == "source":
                        for qualifier in feature["GBFeature_quals"]:
                            if qualifier["GBQualifier_name"] == "host":
                                host = qualifier["GBQualifier_value"]
                                break
            host_info[version] = host  # Use versioned accession number as the key

        except Exception as e:
            print(f"Error fetching data for {accession}: {e}")
            host_info[version] = "ND"  # Assign 'ND' in case of any error

        finally:
            handle.close()

    return host_info


def get_hosts(email, input_filename, output_filename):
    """
    Retrieve host information for accession numbers and save it to a text file.

    Args:
        email (str): Email address to use with NCBI Entrez tool.
        input_filename (str): Path to the file containing a list of accession numbers.
        output_filename (str): Path to save the host information as a text file.
    """
    accession_numbers = read_accession_file(
        input_filename
    )  # Read accession numbers from the file
    host_info = fetch_host_info(
        accession_numbers, email
    )  # Fetch host info for each accession

    # Write the host information to the output file
    with open(output_filename, "w") as file:
        for accession, host in host_info.items():
            file.write(f"{accession} {host}\n")

    print(f"The request has been fulfilled.\nFile saved to {output_filename}")


if __name__ == "__main__":
    # Use argparse to handle command-line arguments
    parser = argparse.ArgumentParser(
        description="Retrieve host information for a list of accession numbers."
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
        help="TXT file with the list of accession numbers",
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Output file to save host information"
    )

    args = parser.parse_args()

    # Call function with parsed arguments
    get_hosts(args.email, args.input, args.output)
