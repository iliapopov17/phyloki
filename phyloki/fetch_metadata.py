#!/usr/bin/env python

import re
import argparse
from Bio import Entrez
from read_accession_file import read_accession_file


def fetch_metadata_info(accession_numbers, email):
    """
    Fetches metadata for a list of accession numbers from NCBI.

    Metadata includes:
    - Versioned accession number
    - Organism name
    - Geographic location (geo_loc_name)
    - Collection date
    - Host

    Args:
        accession_numbers (list of str): Accession numbers to query from NCBI.
        email (str): User email (required for NCBI API requests).

    Returns:
        list of dict: Each dictionary contains metadata for one accession number.
    """
    Entrez.email = email
    metadata_list = []

    for accession in accession_numbers:
        try:
            handle = Entrez.efetch(db="nucleotide", id=accession, retmode="xml")
            records = Entrez.read(handle)
            version = records[0][
                "GBSeq_accession-version"
            ]  # Retrieve versioned accession number
            organism_name = records[0]["GBSeq_organism"]

            # Default values if metadata is missing
            geo_loc = "ND"
            collection_date = "ND"
            host = "ND"

            # Extract additional metadata
            if "GBSeq_feature-table" in records[0]:
                for feature in records[0]["GBSeq_feature-table"]:
                    if feature["GBFeature_key"] == "source":
                        for qualifier in feature["GBFeature_quals"]:
                            if qualifier["GBQualifier_name"] == "geo_loc_name":
                                geo_loc = qualifier["GBQualifier_value"]
                            elif qualifier["GBQualifier_name"] == "collection_date":
                                collection_date = qualifier["GBQualifier_value"]
                            elif qualifier["GBQualifier_name"] == "host":
                                host = qualifier["GBQualifier_value"]
            taxonomy = (
                records[0]["GBSeq_taxonomy"].split("; ")
                if "GBSeq_taxonomy" in records[0]
                else []
            )

            family = next(
                (taxon for taxon in taxonomy if taxon.endswith(("idae", "aceae"))), "ND"
            )
            order = next((taxon for taxon in taxonomy if taxon.endswith("ales")), "ND")

            metadata_list.append(
                {
                    "AN": version,
                    "AN_OrganismName": f"{version} {organism_name}",
                    "Order": order,
                    "Family": family,
                    "Location": geo_loc,
                    "Country": geo_loc.split(":")[0],
                    "Date": collection_date,
                    "Year": (
                        match.group()
                        if (match := re.search(r"\d{4}", collection_date))
                        else collection_date
                    ),
                    "Host": host,
                }
            )
            handle.close()
        except Exception as e:
            print(f"Error fetching metadata for {accession}: {e}")
        finally:
            handle.close()

    return metadata_list


def fetch_metadata(email, input_filename, output_filename):
    """
    Reads a file with accession numbers, retrieves metadata from NCBI, and saves it as a .tsv file.

    Args:
        email (str): User email (required for NCBI API requests).
        input_filename (str): Path to the file containing accession numbers (one per line).
        output_filename (str): Path to save the metadata as a tab-separated (.tsv) file.

    The output file contains the following columns:
    - AN (Accession number with version)
    - AN_OrganismName (Accession + Organism name)
    - Country (geo_loc_name)
    - Year (collection_date)
    - Host
    """
    accession_numbers = read_accession_file(input_filename)
    metadata_list = fetch_metadata_info(accession_numbers, email)

    with open(output_filename, "w") as file:
        file.write(
            "\t".join(
                [
                    "AN",
                    "AN_OrganismName",
                    "Order",
                    "Family",
                    "Location",
                    "Country",
                    "Date",
                    "Year",
                    "Host",
                ]
            )
            + "\n"
        )
        for metadata in metadata_list:
            fields = [
                metadata["AN"],
                metadata["AN_OrganismName"],
                metadata["Order"],
                metadata["Family"],
                metadata["Location"],
                metadata["Country"],
                metadata["Date"],
                metadata["Year"],
                metadata["Host"],
            ]
            file.write("\t".join(fields) + "\n")

    print(f"Metadata retrieval complete.\nFile saved to {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch metadata for nucleotide sequences from NCBI."
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
        help="Path to output file (.tsv) to save retrieved metadata",
    )

    args = parser.parse_args()

    fetch_metadata(args.email, args.input, args.output)
