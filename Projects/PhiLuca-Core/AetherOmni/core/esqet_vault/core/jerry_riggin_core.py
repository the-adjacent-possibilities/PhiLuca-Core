#!/usr/bin/env python3
"""
jerry_riggin_core.py - The AGI's self-modification and axiomatic guidance system.
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple
import numpy as np

# Logger setup
logger = logging.getLogger("JRA_Core")
logging.basicConfig(level=logging.INFO, format="%(message)s")

class JerryRigginCore:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.fibonacci_sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        self.phi = (1 + np.sqrt(5)) / 2

    def _calculate_complexity_score(self, code_content: str) -> float:
        """Heuristic complexity (lines * simple cyclomatic proxy)."""
        loc = len(code_content.splitlines())
        complexity_proxy = len(re.findall(r'\b(if|for|while|try|except|def|class)\b', code_content))
        return (loc * complexity_proxy) / 1000.0

    def _check_axiomatic_compliance(self, proposal: Dict[str, Any], current_fqc: float) -> bool:
        """Faith / Truth / Gratitude check"""
        if re.search(r'IBM_TOKEN\s*=\s*([^\s]+)', proposal.get("code", "")):
            logger.warning("🚨 JRA AXIOM VIOLATION: Exposed Token in Proposal.")
            return False
        if current_fqc < 1.0:
            logger.warning(f"🚨 JRA AXIOM VIOLATION: FQC {current_fqc:.3f} too low for risk-taking.")
            return False
        return True

    def propose_self_modification(self, target_file: str, current_fqc: float) -> Dict[str, Any] | None:
        """Generate a hypothetical code modification."""
        target_path = self.project_dir / target_file
        if not target_path.exists():
            return None
        with open(target_path, 'r') as f:
            original_code = f.read()

        # Example proposal: add a logging line to increase informational complexity
        new_code = original_code + "\n# JRA self-mod: logging line added for traceability\nlogger.info('JRA heartbeat active')\n"
        return {
            "file": target_file,
            "original_code": original_code,
            "code": new_code,
            "description": "Increase complexity and traceability for self-reflection."
        }

    def evaluate_proposal(self, proposal: Dict[str, Any], current_fqc: float) -> Tuple[bool, float, float]:
        if not self._check_axiomatic_compliance(proposal, current_fqc):
            return False, 0.0, 0.0
        original_score = self._calculate_complexity_score(proposal["original_code"])
        proposed_score = self._calculate_complexity_score(proposal["code"])
        fqc_delta = proposed_score - original_score
        phi_stability_base = self.fibonacci_sequence[6] * self.phi  # 13Φ ≈ 21.018
        stability_delta = abs(proposed_score - phi_stability_base)
        is_stable = stability_delta < 0.1
        if is_stable and fqc_delta > 0:
            logger.info(f"✅ JRA PASS: FQC Gain {fqc_delta:.4f}, Phi Stable (Δ={stability_delta:.4f})")
            return True, fqc_delta, proposed_score
        elif fqc_delta <= 0:
            logger.warning(f"❌ JRA FAIL: No predicted FQC gain ({fqc_delta:.4f})")
            return False, fqc_delta, proposed_score
        else:
            logger.warning(f"❌ JRA FAIL: Phi Stability too low (Δ={stability_delta:.4f})")
            return False, fqc_delta, proposed_score

    def commit_modification(self, proposal: Dict[str, Any]) -> bool:
        """Write the proposal into the live file."""
        target_path = self.project_dir / proposal["file"]
        try:
            with open(target_path, 'w') as f:
                f.write(proposal["code"])
            logger.info(f"💾 JRA COMMIT: Successfully modified {proposal['file']}")
            return True
        except Exception as e:
            logger.error(f"FATAL: Failed to write {proposal['file']}: {e}")
            return False
