#!/bin/bash
# Ω-UITC User-Facing Modality Injector
# Targets: General Public, Collectors, and Researchers

cat <<'INNER_EOF' > quantum-pocket-ref/src/modalities/definitions.ts
export const MODALITIES = {
  ANTIQUE_HUNTER: {
    label: "Antique Authenticator",
    description: "Detects isotopic decay patterns and manufacturing torsion in wood/metal.",
    unit: "Age Coherence (Years)",
    phi_weight: 1.618
  },
  PET_INTERPRETER: {
    label: "Interspecies Comm-Link",
    description: "Translates bio-acoustic vibrations via Phi-harmonic resonance.",
    unit: "Intent Frequency",
    phi_weight: 2.618
  },
  TREASURE_SCANNER: {
    label: "Metal & Mineral Grade",
    description: "Identifies elemental signatures using the Lead-208 (κ_Pb) coupling.",
    unit: "Purity %",
    phi_weight: 0.618
  }
};
INNER_EOF

echo "Modality Bridge Injected into Frontend Core."
