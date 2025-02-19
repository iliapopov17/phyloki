#!/usr/bin/env python

import argparse
import os
from Bio import Entrez, SeqIO


def get_sequences(email, file_path, output_dir):
    """
    Fetches nucleotide sequences from NCBI for given accession numbers and saves them as FASTA files.

    Args:
        email (str): User email (required for NCBI API requests).
        file_path (str): Path to a TXT file containing accession numbers (one per line).
        output_dir (str): Directory where the downloaded sequences will be saved.

    Each sequence is saved as a separate FASTA file named <accession>.fasta in the output directory.
    """
    Entrez.email = email

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Read accession numbers from file
    with open(file_path, "r") as file:
        accession_numbers = file.read().split()

    def download_sequence(accession):
        """Fetches a single sequence from NCBI and saves it as a FASTA file."""
        try:
            handle = Entrez.efetch(
                db="nucleotide", id=accession, rettype="fasta", retmode="text"
            )
            record = SeqIO.read(handle, "fasta")
            handle.close()

            output_path = os.path.join(output_dir, f"{accession}.fasta")
            SeqIO.write(record, output_path, "fasta")
            print(f"Downloaded: {accession}")
        except Exception as e:
            print(f"Failed to download {accession}: {e}")

    # Download sequences for each accession number
    for accession in accession_numbers:
        download_sequence(accession)

    print("All downloads completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch nucleotide sequences from NCBI and save them as FASTA files."
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
        "-o", "--output", required=True, help="Directory to save downloaded FASTA files"
    )

    args = parser.parse_args()

    get_sequences(args.email, args.input, args.output)
