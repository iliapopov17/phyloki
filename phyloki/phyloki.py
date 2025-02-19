import argparse
import subprocess
import shutil
from pathlib import Path
import sys
from .version import __version__


def main():
    parser = argparse.ArgumentParser(
        description="Phyloki: metadata fetcher for microbial phylogenetics.",
        add_help=False,
    )

    parser.add_argument(
        "--get_sequences",
        action="store_true",
        help="Run the module that retrieves nucleotide sequences from a list of accession numbers.",
    )
    parser.add_argument(
        "--fetch_metadata",
        action="store_true",
        help="Run the module to fetch metadata associated with accession numbers.",
    )
    parser.add_argument(
        "--get_organisms",
        action="store_true",
        help="Run the module that fetches organism names by their corresponding accession versions.",
    )
    parser.add_argument(
        "--update_tree",
        action="store_true",
        help="Run the module that updates a phylogenetic tree by replacing accession numbers with accession numbers + organism names.",
    )
    parser.add_argument(
        "--get_hosts",
        action="store_true",
        help="Run the module that retrieves host information for given accession numbers.",
    )
    parser.add_argument(
        "--get_hosts_order",
        action="store_true",
        help="Run the module that fetches the taxonomic order for host organisms.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Display the version of Phyloki and exit.",
    )

    args, extra_args = parser.parse_known_args()

    package_dir = Path(__file__).resolve().parent

    command_map = {
        "get_sequences": package_dir / "get_seqs.py",
        "fetch_metadata": package_dir / "fetch_metadata.py",
        "get_organisms": package_dir / "get_organisms.py",
        "update_tree": package_dir / "update_tree.py",
        "get_hosts": package_dir / "get_hosts.py",
        "get_hosts_order": package_dir / "get_hosts_order.py",
    }

    if "-h" in sys.argv or "--help" in sys.argv:
        if not any(getattr(args, key) for key in command_map):
            parser.print_help()
            return

    for arg, script in command_map.items():
        if getattr(args, arg):
            subprocess.run(["python", str(script)] + extra_args, check=True)
            return

    parser.print_help()

    pycache_dir = package_dir / "__pycache__"
    if pycache_dir.exists() and pycache_dir.is_dir():
        shutil.rmtree(pycache_dir)


if __name__ == "__main__":
    main()
