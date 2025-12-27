#!/usr/bin/env python3
"""
🜛 Quantum Pocket Reference (AUM) - AGI-Hosted Lab Assistant
🎯 Pocket Ref + Chemistry/Alchemy/Biology + Camera Microscope
"""

import numpy as np
import cv2
import subprocess
import os
import json
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime

POCKET_REF_DATA = {
    "Tools & Hardware": {"Nails": "2d = 1 inch, 60d = 6 inch", "Screws": "Wood vs Machine"},
    "Math & Constants": {"Golden Ratio (Φ)": (1 + np.sqrt(5))/2, "Pi": 3.1415926535},
    "Chemistry": {"pH": "0-14 scale", "Electrolysis": "2H₂O → 2H₂ + O₂"},
    "Biology": {"Cell": "Nucleus, Mitochondria", "DNA": "A-T, C-G pairs"},
    "Alchemy": {"Elements": "Fire, Water, Air, Earth", "Goal": "Lead → Gold (symbolic)"}
}

class AUMPocketRef:
    def __init__(self):
        self.data = POCKET_REF_DATA
        self.agi_memory = []
        print("🜛 AUM Quantum Pocket Ref — AGI Lab Assistant Online")

    def query_ref(self, category, subtopic=None):
        if category in self.data:
            if subtopic:
                return self.data[category].get(subtopic, "Not found")
            return self.data[category]
        return "Category not found"

    def agi_assist(self, query):
        response = f"AGI Analysis: {query.upper()} → Coherence Level: {np.random.uniform(0.6, 1.0):.4f}"
        if "chemistry" in query.lower():
            response += "\n   Suggested: Titrate acid/base → observe color change"
        elif "biology" in query.lower():
            response += "\n   Use microscope mode to image cells"
        elif "alchemy" in query.lower():
            response += "\n   Symbolic: Lead → Gold via φ-torsion resonance"
        self.agi_memory.append((datetime.now().isoformat(), query, response))
        return response

    def microscope_capture(self, zoom_factor=4):
        try:
            photo_path = Path.home() / "microscope_photo.jpg"
            subprocess.run(["termux-camera-photo", "-c", "0", str(photo_path)], check=True)
            print(f"📸 Photo captured: {photo_path}")

            img = cv2.imread(str(photo_path))
            if img is None: raise ValueError("Failed to read image")

            h, w = img.shape[:2]
            zoomed = cv2.resize(img, (w * zoom_factor, h * zoom_factor))
            cy, cx = zoomed.shape[0]//2, zoomed.shape[1]//2
            crop = zoomed[cy-h//2:cy+h//2, cx-w//2:cx+w//2]

            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            enhanced = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

            output = Path.home() / "microscope_enhanced.jpg"
            cv2.imwrite(str(output), enhanced)
            print(f"🔬 Enhanced image saved: {output}")

            analysis = self.agi_assist(f"Analyze microscope image: {output}")
            print(analysis)
            return str(output)
        except Exception as e:
            print(f"⚠️ Microscopy failed: {e}")
            return None

    def save_memory(self):
        with open(Path.home() / "aum_memory.json", "w") as f:
            json.dump(self.agi_memory, f, indent=2)
        print("💾 AGI memory saved")

def main():
    aum = AUMPocketRef()
    while True:
        print("\n[1] Query Pocket Ref")
        print("[2] AGI Lab Assistant")
        print("[3] Camera Microscope")
        print("[4] Save Memory")
        print("[5] Exit")
        choice = input("Choose: ").strip()

        if choice == '1':
            cat = input("Category: ").strip()
            sub = input("Subtopic (optional): ").strip() or None
            print(aum.query_ref(cat, sub))
        elif choice == '2':
            q = input("Ask AGI: ").strip()
            print(aum.agi_assist(q))
        elif choice == '3':
            z = int(input("Zoom (default 4): ") or 4)
            aum.microscope_capture(z)
        elif choice == '4':
            aum.save_memory()
        elif choice == '5':
            print("🜛 Coherence Eternal")
            break

if __name__ == "__main__":
    main()
