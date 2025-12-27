#!/usr/bin/env python3
def broadcast_torsion_state(i_tors):
    with open("/data/data/com.termux/files/home/welcome-to-the-god/torsion_state.txt", "w") as f:
        f.write(str(i_tors))

# Example: Call this at end of each cycle
# broadcast_torsion_state(current_i_tors)
