import os
import random
from Bio import Entrez, SeqIO
import pandas as pd


def get_sequences(email, file_path, output_dir):
    """
    Download sequences for accession numbers and save them to specified directory.

    Args:
        email (str): Email address to use with NCBI Entrez tool.
        file_path (str): Path to the file containing accession numbers.
        output_dir (str): Directory to save downloaded sequences.
    """
    # Set the NCBI Entrez email
    Entrez.email = email

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Read accession numbers from file
    with open(file_path, "r") as file:
        accession_numbers = file.read().split()

    # Function to download sequence
    def download_sequence(accession):
        try:
            # Fetching the sequence from NCBI
            handle = Entrez.efetch(
                db="nucleotide", id=accession, rettype="fasta", retmode="text"
            )
            record = SeqIO.read(handle, "fasta")
            handle.close()

            # Saving the sequence to a file
            output_path = os.path.join(output_dir, f"{accession}.fasta")
            SeqIO.write(record, output_path, "fasta")
            print(f"Downloaded: {accession}")
        except Exception as e:
            print(f"Failed to download {accession}: {e}")

    # Download sequences for each accession number
    for accession in accession_numbers:
        download_sequence(accession)

    print("All downloads completed.")


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


def fetch_organism_names(email, accession_numbers):
    """Fetch organism names and versions from NCBI's Entrez for given accession numbers."""
    Entrez.email = email
    organism_dict = {}
    for accession in accession_numbers:
        try:
            handle = Entrez.efetch(db="nucleotide", id=accession, retmode="xml")
            records = Entrez.read(handle)
            organism_name = records[0]["GBSeq_organism"]
            accession_version = records[0][
                "GBSeq_accession-version"
            ]  # Fetch the accession version
            organism_dict[accession_version] = (
                organism_name  # Use accession version as key
            )
            handle.close()
        except IndexError:
            print(f"No data found for {accession}")
        except KeyError:
            print(f"Organism name or accession version missing for {accession}")
        except Exception as e:
            print(f"Error retrieving data for {accession}: {e}")
            handle.close()
    return organism_dict


def get_organisms(email, input_filename, output_filename):
    """Main function to get organisms with version and write them to a file."""
    accession_numbers = read_accession_file(input_filename)
    organism_dict = fetch_organism_names(email, accession_numbers)

    with open(output_filename, "w") as file:
        for accession_version, organism in organism_dict.items():
            file.write(f"{accession_version} {organism}\n")

    print(f"The request has been fulfilled.\nFile saved to {output_filename}")


def load_annotations(file_path):
    """
    Load organism annotations from a given text file into a dictionary.
    """
    annotations = {}
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                annotations[parts[0]] = parts[1]
    return annotations


def replace_names_in_tree(tree_file_path, annotations, output_file_path):
    """
    Replace accession numbers in the tree file with accession numbers and organism names.
    """
    with open(tree_file_path, "r") as tree_file:
        tree_data = tree_file.read()

    for accession, organism in annotations.items():
        tree_data = tree_data.replace(f"{accession}:", f"{accession} {organism}:")

    with open(output_file_path, "w") as output_file:
        output_file.write(tree_data)


def update_tree(annotation_file_path, tree_file_path, output_file_path):
    """
    Update a tree file by replacing accession numbers with annotated names from a given annotation file.

    Args:
        annotation_file_path (str): Path to the text file containing accession numbers and organism names.
        tree_file_path (str): Path to the tree file.
        output_file_path (str): Path to save the updated tree file.
    """
    annotations = load_annotations(annotation_file_path)
    replace_names_in_tree(tree_file_path, annotations, output_file_path)
    print(f"The request has been fulfilled.\nFile saved to {output_file_path}")


def read_accession_file(filename):
    """
    Read accession numbers from a file.
    """
    with open(filename, "r") as file:
        accession_numbers = [line.strip() for line in file.readlines()]
    return accession_numbers


def fetch_host_info(accession_numbers, email):
    """
    Fetch host information for each accession number from NCBI.
    """
    Entrez.email = email  # Always set this to your email address
    host_info = {}
    for accession in accession_numbers:
        try:
            handle = Entrez.efetch(db="nucleotide", id=accession, retmode="xml")
            records = Entrez.read(handle)
            version = records[0][
                "GBSeq_accession-version"
            ]  # Retrieve the versioned accession number
            host = "ND"  # Default if no host information is found
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
    Retrieve host information for accession numbers and save it to a file.

    Args:
        email (str): Email address to use with NCBI Entrez tool.
        input_filename (str): Path to the file containing accession numbers.
        output_filename (str): Path to save the host information.
    """
    accession_numbers = read_accession_file(input_filename)
    host_info = fetch_host_info(accession_numbers, email)

    with open(output_filename, "w") as file:
        file.write("Accession number\thost\n")
        for accession, host in host_info.items():
            file.write(f"{accession}\t{host}\n")
    print(f"The request has been fulfilled.\nFile saved to {output_filename}")


def get_order(species_name, email):
    """
    Fetches the taxonomic order for a given species name using Entrez,
    handling potential errors and ambiguous entries.
    """
    if species_name == "ND":
        return "ND"  # Maintain "ND" for no data entries

    # Extract the relevant part of the species name (typically the first two words)
    clean_species_name = " ".join(species_name.split()[:2])

    Entrez.email = email
    try:
        handle = Entrez.esearch(db="taxonomy", term=clean_species_name)
        record = Entrez.read(handle)
        handle.close()
        if not record["IdList"]:  # Check if any results were found
            return f"{species_name} - Note - False record"
        tax_id = record["IdList"][0]
        handle = Entrez.efetch(db="taxonomy", id=tax_id, retmode="xml")
        records = Entrez.read(handle)
        handle.close()
        lineage = records[0]["LineageEx"]
        for taxon in lineage:
            if taxon["Rank"] == "order":
                return taxon["ScientificName"]
    except Exception as e:
        return f"{species_name} - Error - {e}"

    return "ND"  # Return "ND" if order not found or in case of unexpected errors


def get_hosts_orders(email, input_filename, output_filename):
    """
    Process an input file to associate host organisms with their taxonomic orders and save the results to an output file.

    Args:
        email (str): Email address to use with NCBI Entrez tool.
        input_filename (str): Path to the file containing accession numbers and host organisms.
        output_filename (str): Path to save the host orders.
    """
    with open(input_filename, "r") as infile, open(output_filename, "w") as outfile:
        for line in infile:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                accession, species = parts
            else:
                continue  # Skip lines that don't have two parts
            order = get_order(species, email) if species != "ND" else "ND"
            outfile.write(f"{accession}\t{order}\n")
    print(
        f'The request has been fulfilled.\nFile saved to {output_filename}\nPlease do not forget to edit the file manually.\nThe query to NCBI database from this function is pretty difficult.\nSometimes this function prints:\n"Error - HTTP Error 400: Bad Request" in case of bad connection or\n"Note - False record" in case there is no record about the host organism.'
    )


def get_unique_orders(file_path):
    """
    Extracts and returns a list of unique groups (orders) from the specified file.

    Args:
        file_path (str): Path to the file containing accession numbers and group classifications.

    Returns:
        list: A list of unique group identifiers.
    """
    # Load the data into a DataFrame
    order_df = pd.read_csv(
        file_path, sep="\t", header=None, names=["Accession", "Group"]
    )

    # Get unique groups
    unique_groups = order_df["Group"].unique().tolist()

    return unique_groups


def set_color_map(file_path):
    """
    Prompts the user to set HEX color codes for each unique group found in the file.
    """
    unique_groups = get_unique_orders(file_path)
    color_map = {}

    for group in unique_groups:
        # Keep prompting until a valid HEX color code is entered
        while True:
            color_code = input(
                f"Enter HEX color code for {group} (without #): "
            ).strip()
            # Check if the entered color code is valid
            if len(color_code) == 6 and all(
                c in "0123456789ABCDEFabcdef" for c in color_code
            ):
                color_map[group] = f"#{color_code}"
                break
            else:
                print("Invalid HEX code. Please enter a 6-digit hexadecimal number.")

    return color_map


def generate_random_color():
    """Generate a random hex color."""
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def get_itol_dataset(organism_file, order_file, output_file, color_map=None):
    """
    Generates a dataset for iTOL from given organism and order files, assigning colors to unique groups.
    Allows for optional provision of a custom color map; if not provided, colors are generated randomly.

    Args:
        organism_file (str): Path to the file containing accession numbers and organism names.
        order_file (str): Path to the file containing accession numbers and group classifications.
        output_file (str): Path to save the iTOL dataset file.
        color_map (dict, optional): Dictionary of colors for each group. If None, colors are generated randomly.
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Load order data
    order_df = pd.read_csv(
        order_file, sep="\t", header=None, names=["Accession", "Group"]
    )
    unique_groups = order_df["Group"].unique()

    if color_map is None:
        color_map = {group: generate_random_color() for group in unique_groups}
        print("Colors were not set, they were generated randomly.")
    else:
        print("Colors were set by the user.")

    # Manually parse the organism data
    parsed_data = []
    with open(organism_file, "r") as file:
        for line in file:
            split_line = line.strip().split(maxsplit=1)
            if len(split_line) == 2:
                parsed_data.append(split_line)
            else:
                print(f"Skipping line due to parsing issue: {line.strip()}")

    organism_df = pd.DataFrame(parsed_data, columns=["Accession", "Organism"])

    # Merge the dataframes on Accession number
    merged_df = pd.merge(order_df, organism_df, on="Accession", how="left")
    merged_df["Color"] = merged_df["Group"].map(color_map)

    # Define iTOL dataset headers
    itol_header = [
        "DATASET_COLORSTRIP",
        "SEPARATOR TAB",
        "DATASET_LABEL\tHost Group Colors",
        "DATA",
    ]

    # Format data for iTOL
    data_lines = merged_df.apply(
        lambda row: f"{row['Accession']} {row['Organism']}\t{row['Color']}\t{row['Group']}",
        axis=1,
    ).tolist()
    itol_content = itol_header + data_lines

    # Write to iTOL dataset file
    with open(output_file, "w") as file:
        for line in itol_content:
            file.write(line + "\n")

    print("The request has been fulfilled.")


def fetch_geo_loc(accession_numbers, email):
    """
    Fetch geographical location (geo_loc_name) for each accession number from NCBI.

    Args:
        accession_numbers (list): List of accession numbers to query.
        email (str): Email address for NCBI Entrez.

    Returns:
        dict: A dictionary mapping accession numbers to their geographical location.
    """
    Entrez.email = email
    geo_loc_info = {}

    for accession in accession_numbers:
        try:
            handle = Entrez.efetch(db="nucleotide", id=accession, retmode="xml")
            records = Entrez.read(handle)
            version = records[0]["GBSeq_accession-version"]  # Retrieve versioned accession number
            geo_loc = "ND"  # Default if no geo_loc is found
            
            # Extract geo_loc_name from the feature table
            if "GBSeq_feature-table" in records[0]:
                features = records[0]["GBSeq_feature-table"]
                for feature in features:
                    if feature["GBFeature_key"] == "source":
                        for qualifier in feature["GBFeature_quals"]:
                            if qualifier["GBQualifier_name"] == "geo_loc_name":
                                geo_loc = qualifier["GBQualifier_value"]
                                break
            geo_loc_info[version] = geo_loc  # Map versioned accession to geo_loc_name
            handle.close()
        except Exception as e:
            print(f"Error fetching geo_loc_name for {accession}: {e}")
            geo_loc_info[version] = "ND"  # Assign 'ND' in case of any error
        finally:
            handle.close()
    
    return geo_loc_info

def get_geo_loc(email, input_filename, output_filename):
    """
    Retrieve geographical location (geo_loc_name) for accession numbers and save them to a .tsv file.

    Args:
        email (str): Email address for NCBI Entrez.
        input_filename (str): Path to the file containing accession numbers.
        output_filename (str): Path to save the geo location information as a .tsv file.
    """
    # Read accession numbers from file
    accession_numbers = read_accession_file(input_filename)
    
    # Fetch geo locations for the accession numbers
    geo_loc_info = fetch_geo_loc(accession_numbers, email)
    
    # Write the results to a .tsv file
    with open(output_filename, "w") as file:
        file.write("Accession number\tgeo_loc_name\n")
        for accession, geo_loc in geo_loc_info.items():
            file.write(f"{accession}\t{geo_loc}\n")
    
    print(f"The request has been fulfilled.\nFile saved to {output_filename}")


def fetch_collection_date(accession_numbers, email):
    """
    Fetch collection date (/collection_date) for each accession number from NCBI.

    Args:
        accession_numbers (list): List of accession numbers to query.
        email (str): Email address for NCBI Entrez.

    Returns:
        dict: A dictionary mapping accession numbers to their collection date.
    """
    Entrez.email = email
    collection_date_info = {}

    for accession in accession_numbers:
        try:
            handle = Entrez.efetch(db="nucleotide", id=accession, retmode="xml")
            records = Entrez.read(handle)
            version = records[0]["GBSeq_accession-version"]  # Retrieve versioned accession number
            collection_date = "ND"  # Default if no collection_date is found
            
            # Extract collection_date from the feature table
            if "GBSeq_feature-table" in records[0]:
                features = records[0]["GBSeq_feature-table"]
                for feature in features:
                    if feature["GBFeature_key"] == "source":
                        for qualifier in feature["GBFeature_quals"]:
                            if qualifier["GBQualifier_name"] == "collection_date":
                                collection_date = qualifier["GBQualifier_value"]
                                break
            collection_date_info[version] = collection_date  # Map versioned accession to collection_date
            handle.close()
        except Exception as e:
            print(f"Error fetching collection_date for {accession}: {e}")
            collection_date_info[version] = "ND"  # Assign 'ND' in case of any error
        finally:
            handle.close()
    
    return collection_date_info

def get_year(email, input_filename, output_filename):
    """
    Retrieve collection date (/collection_date) for accession numbers and save them to a .tsv file.

    Args:
        email (str): Email address for NCBI Entrez.
        input_filename (str): Path to the file containing accession numbers.
        output_filename (str): Path to save the collection date information as a .tsv file.
    """
    # Read accession numbers from file
    accession_numbers = read_accession_file(input_filename)
    
    # Fetch collection dates for the accession numbers
    collection_date_info = fetch_collection_date(accession_numbers, email)
    
    # Write the results to a .tsv file
    with open(output_filename, "w") as file:
        file.write("Accession number\tcollection_date\n")
        for accession, collection_date in collection_date_info.items():
            file.write(f"{accession}\t{collection_date}\n")
    
    print(f"The request has been fulfilled.\nFile saved to {output_filename}")


def fetch_metadata_info(accession_numbers, email):
    """
    Fetch metadata information (accession, organism, geo_loc_name, collection_date, and host) for each accession number.

    Args:
        accession_numbers (list): List of accession numbers to query.
        email (str): Email address for NCBI Entrez.

    Returns:
        list: A list of dictionaries with metadata for each accession number.
    """
    Entrez.email = email
    metadata_list = []

    for accession in accession_numbers:
        try:
            handle = Entrez.efetch(db="nucleotide", id=accession, retmode="xml")
            records = Entrez.read(handle)
            version = records[0]["GBSeq_accession-version"]  # Retrieve versioned accession number

            # Extract organism name
            organism_name = records[0]["GBSeq_organism"]

            # Initialize default values
            geo_loc = "ND"
            collection_date = "ND"
            host = "ND"

            # Extract geo_loc_name, collection_date, and host from the feature table
            if "GBSeq_feature-table" in records[0]:
                features = records[0]["GBSeq_feature-table"]
                for feature in features:
                    if feature["GBFeature_key"] == "source":
                        for qualifier in feature["GBFeature_quals"]:
                            if qualifier["GBQualifier_name"] == "geo_loc_name":
                                geo_loc = qualifier["GBQualifier_value"]
                            if qualifier["GBQualifier_name"] == "collection_date":
                                collection_date = qualifier["GBQualifier_value"]
                            if qualifier["GBQualifier_name"] == "host":
                                host = qualifier["GBQualifier_value"]

            # Add all extracted data to the metadata list
            metadata_list.append({
                "Name": version,
                "Full.Name": f"{version} {organism_name}",
                "Country": geo_loc,
                "Year": collection_date,
                "Host": host
            })
            handle.close()
        except Exception as e:
            print(f"Error fetching metadata for {accession}: {e}")
        finally:
            handle.close()
    
    return metadata_list

def fetch_metadata(email, input_filename, output_filename):
    """
    Retrieve metadata for accession numbers (organism, geo_loc_name, collection_date, and host) and save it to a .tsv file.

    Args:
        email (str): Email address for NCBI Entrez.
        input_filename (str): Path to the file containing accession numbers.
        output_filename (str): Path to save the metadata information as a .tsv file.
    """
    # Read accession numbers from file
    accession_numbers = read_accession_file(input_filename)

    # Fetch metadata information for each accession number
    metadata_list = fetch_metadata_info(accession_numbers, email)
    
    # Write the results to a .tsv file
    with open(output_filename, "w") as file:
        file.write("Name\tFull.Name\tCountry\tYear\tHost\n")
        for metadata in metadata_list:
            file.write(f"{metadata['Name']}\t{metadata['Full.Name']}\t{metadata['Country']}\t{metadata['Year']}\t{metadata['Host']}\n")
    
    print(f"The request has been fulfilled.\nFile saved to {output_filename}")

