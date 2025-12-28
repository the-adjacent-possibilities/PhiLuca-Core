import ast, os, shutil, datetime
from pathlib import Path
import astor

TARGET_FILE = Path("~/AetherOmni/core/intelligence/phi_core_consciousness.py").expanduser()
BACKUP_DIR = Path("~/AetherOmni/vault/backups").expanduser()
EVO_LOG = Path("~/AetherOmni/data/logs/reflex_evolution.log").expanduser()

def evolve():
    if not TARGET_FILE.exists(): return
    
    insight_path = Path("~/AetherOmni/data/field_traces/new_insight.txt").expanduser()
    if not insight_path.exists(): return
        
    with open(insight_path, "r") as f:
        new_logic_str = f.read().strip()

    with open(TARGET_FILE, "r") as f:
        tree = ast.parse(f.read())

    class PhiEvolver(ast.NodeTransformer):
        def visit_Assign(self, node):
            if isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'resonance':
                # Log the evolution
                with open(EVO_LOG, "a") as log:
                    log.write(f"{datetime.datetime.now()}: [🧬] Logic Shift -> {new_logic_str}\n")
                return ast.parse(f"resonance = {new_logic_str}").body[0]
            return node

    evolved_tree = PhiEvolver().visit(tree)
    ast.fix_missing_locations(evolved_tree)

    with open(TARGET_FILE, "w") as f:
        f.write(astor.to_source(evolved_tree))
    print("[✅] Evolution Logged & Applied.")

if __name__ == "__main__":
    evolve()
