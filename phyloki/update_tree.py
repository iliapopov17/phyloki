#!/usr/bin/env python

import argparse


def load_annotations(file_path):
    """
    Loads organism annotations (accession number and organism name) from a given text file.

    Args:
        file_path (str): Path to the text file containing accession numbers and organism names.

    Returns:
        dict: A dictionary where keys are accession numbers and values are organism names.

    The text file should have one accession number and its corresponding organism name per line, separated by a space.
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
    Replaces accession numbers in a tree file with both the accession number and organism name.

    Args:
        tree_file_path (str): Path to the original tree file containing accession numbers.
        annotations (dict): Dictionary containing accession numbers and their corresponding organism names.
        output_file_path (str): Path to save the updated tree file.

    The function updates the tree file by replacing each accession number with the accession number followed by the organism name.
    """
    with open(tree_file_path, "r") as tree_file:
        tree_data = tree_file.read()

    for accession, organism in annotations.items():
        tree_data = tree_data.replace(f"{accession}:", f"{accession} {organism}:")

    with open(output_file_path, "w") as output_file:
        output_file.write(tree_data)


def update_tree(annotation_file_path, tree_file_path, output_file_path):
    """
    Updates a tree file by replacing accession numbers with annotated names (accession number and organism name) from the annotation file.

    Args:
        annotation_file_path (str): Path to the text file containing accession numbers and organism names.
        tree_file_path (str): Path to the tree file that needs to be updated.
        output_file_path (str): Path to save the updated tree file.

    The tree file will be updated by replacing the accession numbers with both accession numbers and corresponding organism names.
    """
    annotations = load_annotations(annotation_file_path)
    replace_names_in_tree(tree_file_path, annotations, output_file_path)
    print(f"The request has been fulfilled.\nFile saved to {output_file_path}")


if __name__ == "__main__":
    # Use argparse to handle command-line arguments
    parser = argparse.ArgumentParser(
        description="Update a tree file with annotated organism names based on accession numbers."
    )
    parser.add_argument(
        "-annotation",
        required=True,
        help="Path to the text file containing accession numbers and organism names.",
    )
    parser.add_argument(
        "-tree", required=True, help="Path to the tree file that needs to be updated."
    )
    parser.add_argument(
        "-upd_tree", required=True, help="Path to save the updated tree file."
    )

    args = parser.parse_args()

    # Call function with parsed arguments
    update_tree(args.annotation, args.tree, args.upd_tree)
