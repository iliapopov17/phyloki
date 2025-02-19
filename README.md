![Python3](https://img.shields.io/badge/Language-Python3-steelblue)
![Biopython](https://img.shields.io/badge/Dependecy-Biopython-steelblue)
![Pandas](https://img.shields.io/badge/Dependecy-Pandas-steelblue)
![OS](https://img.shields.io/badge/OS-_Windows_|_Mac_|_Linux-steelblue)
![License](https://img.shields.io/badge/License-MIT-steelblue)

<img src="https://github.com/iliapopov17/phyloki/blob/main/imgs/phyloki_logo_light.png#gh-light-mode-only" width = 50%/>
<img src="https://github.com/iliapopov17/phyloki/blob/main/imgs/phyloki_logo_dark.png#gh-dark-mode-only" width = 50%/>

> Phyloki simplifies phylogenetic tree annotation in microbiology and virology by fetching metadata from NCBI GenBank using accession numbers. It also reinstates organism names in trees constructed with IQ-TREE, retrieves host information about microorganisms, and prepares annotation datasets for further visualization in iTOL.

## Table of contents

- [Features](#features)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Contributing](#contributing)
- [Contact](#contact)

|The Good 😎|The Bad 😒|The Ugly 🚮|
|--------|-------|--------|
|<img src="https://github.com/iliapopov17/Detailed-Sequences-for-Trees-Unblemished/blob/main/imgs/second%20tree.jpg" width="100%">|<img src="https://github.com/iliapopov17/Detailed-Sequences-for-Trees-Unblemished/blob/main/imgs/third%20tree.jpg" width="100%">|<img src="https://github.com/iliapopov17/Detailed-Sequences-for-Trees-Unblemished/blob/main/imgs/first%20tree.jpg" width="100%">|

Phyloki allows easy and simple annotation of phylogenetic trees. See the examples above:
- The best tree contains information about the hosts from which the virus was isolated and the full names of the viruses.
- The so-so tree contains the same information, but is colour annotated with randomly generated colours.
- The worst tree contains only accession numbers on its leaves.

## Features
### Sequence Downloading
- Facilitates the retrieval of sequences from NCBI GenBank using specified accession numbers.
### Metadata Fetching
- Downloads metadata from NCBI GenBank (Accession Number; Organism Name; Country; Year; Host)
### Organism Name Reintegration
- Enhances IQ-TREE constructed trees by replacing accession numbers with the corresponding organism names for clarity and context.
### Host Information Retrieval
- Gathers host data for each microorganism, including the host's taxonomic order.
### Annotation Dataset Preparation for iTOL
- Utilizes the collected host information to prepare detailed annotation datasets, optimizing visualization in iTOL.

## Installation

```python
pip install phyloki
```

## Usage Guide

Demonstrational data is based on the recent paper about identifying novel hantavirus in bats

🔗 Visit [Phyloki wiki](https://github.com/iliapopov17/phyloki/wiki) page

## Contributing
Contributions are welcome! If you have any ideas, bug fixes, or enhancements, feel free to open an issue or submit a pull request.

## Contact
For any inquiries or support, feel free to contact me via [email](mailto:iljapopov17@gmail.com)

Happy tree annotating! 🌳
