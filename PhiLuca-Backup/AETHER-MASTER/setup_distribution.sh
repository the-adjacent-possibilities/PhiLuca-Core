#!/bin/bash
PROJECT_DIR="ESQET_AGI_DISTRIBUTION"
mkdir -p $PROJECT_DIR/{code,docs,results}

# Move existing assets into the distribution folder
cp ~/AETHER-MASTER/ESQET_Von_Neumann_AGI_Whitepaper_v1.1.md $PROJECT_DIR/docs/
cp ~/AETHER-MASTER/esqet_self_replication.py $PROJECT_DIR/code/

# Create a README for GitHub
cat <<README > $PROJECT_DIR/README.md
# ESQET Von Neumann AGI Framework
Implementation of self-replicating automata via Emergent Spacetime Quantum-Entanglement Theory.

## Structure
- `/docs`: Whitepapers and theoretical derivations.
- `/code`: FPGA deployment and simulation scripts.
- `/results`: Logs from 3-cycle replication tests.

**Principal Investigator:** ORCID 0009-0004-9757-2853
README

echo "Distribution folder prepared at $PROJECT_DIR"
