#!/usr/bin/env python

import argparse
from Bio import Entrez


def get_order(species_name, email):
    """
    Fetch the taxonomic order for a given species name using NCBI Entrez.

    Args:
        species_name (str): The species name to search for.
        email (str): The email address to use with NCBI Entrez tool.

    Returns:
        str: The taxonomic order for the species or a status message (e.g., error or no data).

    The function first cleans the species name by using only the first two words. It then queries NCBI Entrez
    to retrieve the taxonomic information, focusing on the "order" rank in the lineage.
    """
    if species_name == "ND":
        return "ND"  # Return "ND" if no data is available for the species name

    # Clean species name by using only the first two words (genus and species)
    clean_species_name = " ".join(species_name.split()[:2])

    Entrez.email = email  # Always set this to your email address
    try:
        # Search the taxonomy database for the species
        handle = Entrez.esearch(db="taxonomy", term=clean_species_name)
        record = Entrez.read(handle)
        handle.close()

        # If no results are found, return a message indicating no record
        if not record["IdList"]:
            return f"{species_name} - Note - False record"

        # Fetch detailed taxonomy data for the species
        tax_id = record["IdList"][0]
        handle = Entrez.efetch(db="taxonomy", id=tax_id, retmode="xml")
        records = Entrez.read(handle)
        handle.close()

        # Look through the lineage for the "order"
        lineage = records[0]["LineageEx"]
        for taxon in lineage:
            if taxon["Rank"] == "order":
                return taxon["ScientificName"]
    except Exception as e:
        # Return error message if an exception occurs
        return f"{species_name} - Error - {e}"

    return "ND"  # Return "ND" if no order is found or if an error occurs


def get_hosts_orders(email, input_filename, output_filename):
    """
    Process an input file to associate host organisms with their taxonomic orders and save the results to an output file.

    Args:
        email (str): The email address to use with NCBI Entrez tool.
        input_filename (str): Path to the file containing accession numbers and host species names.
        output_filename (str): Path to save the output file with accession numbers and their corresponding orders.
    """
    with open(input_filename, "r") as infile, open(output_filename, "w") as outfile:
        # Process each line in the input file
        for line in infile:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                accession, species = parts
            else:
                continue  # Skip lines that don't have the expected format

            # Get the taxonomic order for the species, defaulting to "ND" if no species is provided
            order = get_order(species, email) if species != "ND" else "ND"

            # Write the accession and order to the output file
            outfile.write(f"{accession}\t{order}\n")

    # Inform the user that the task has been completed
    print(
        f'The request has been fulfilled.\nFile saved to {output_filename}\nPlease do not forget to edit the file manually.\nThe query to NCBI database from this function is quite difficult.\nSometimes this function prints:\n"Error - HTTP Error 400: Bad Request" in case of bad connection or\n"Note - False record" in case there is no record about the host organism.'
    )


if __name__ == "__main__":
    # Use argparse to handle command-line arguments
    parser = argparse.ArgumentParser(
        description="Fetch taxonomic orders for host organisms based on accession numbers."
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
        help="TXT file containing accession numbers and host species",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output file to save accession numbers with their hosts' taxonomic orders",
    )

    args = parser.parse_args()

    # Call the function with parsed arguments
    get_hosts_orders(args.email, args.input, args.output)
