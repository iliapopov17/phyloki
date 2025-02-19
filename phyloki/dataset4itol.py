import random
import pandas as pd


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
