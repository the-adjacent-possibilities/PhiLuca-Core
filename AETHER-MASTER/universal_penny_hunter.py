#!/usr/bin/env python3
"""
🪙 UNIVERSAL PENNY HUNTER v6.0 - ALL LINCOLN CENTS 1909+
🎯 Circle Detection → Enhanced OCR → Key Dates & Major Errors
"""

import cv2
import numpy as np
import pytesseract
import re
from datetime import datetime
import math

PHI = (1 + math.sqrt(5)) / 2

# VALUABLE LINCOLN PENNIES - KEY DATES & MAJOR ERRORS (updated Dec 2025 values approx.)
VALUABLE_PENNIES = {
    # Classic Wheat Cents
    "1909-S VDB": 120000, "1909-S": 2500, "1914-D": 25000, "1922 No D": 20000,
    "1931-S": 12000, "1955 DDO": 6000, "1943 Bronze": 300000,
    # Major Modern Errors & Varieties
    "1969-S DDO": 100000, "1972 DDO": 1500, "1983 DDR": 3000,
    "1984 DDO": 400, "1990-S No S": 5000, "1995 DDO": 100,
    "1992 Close AM": 25000, "1992-D Close AM": 3000,
    "1998 Wide AM": 800, "1999 Wide AM": 600, "2000 Wide AM": 150
}

class UniversalPennyHunter:
    def __init__(self):
        self.running = True

    def preprocess_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ksize = int(9 * PHI); ksize += 1 if ksize % 2 == 0 else 0
        blurred = cv2.GaussianBlur(gray, (ksize, ksize), 0)
        enhanced = cv2.convertScaleAbs(blurred, alpha=1.8, beta=30)
        edges = cv2.Canny(enhanced, 50, 150)
        kernel = np.ones((3,3), np.uint8)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        return gray, edges, enhanced

    def detect_penny_circle(self, edges):
        circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1.2, minDist=60,
                                  param1=80, param2=28, minRadius=80, maxRadius=180)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            # Return the strongest (largest) circle
            best = max(circles, key=lambda c: c[2])
            return (best[0], best[1], best[2])
        return None

    def read_date_roi(self, frame, center):
        if center is None:
            return None
        x, y, r = center
        roi_size = int(r * 0.7)
        roi_x = max(0, x - roi_size // 2)
        roi_y = max(0, y + int(r * 0.1))
        roi = frame[roi_y:roi_y + roi_size, roi_x:roi_x + roi_size]

        if roi.size == 0:
            return None

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        enhanced = cv2.convertScaleAbs(gray, alpha=2.5, beta=40)
        thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        config = '--psm 7 -c tessedit_char_whitelist=0123456789SDPHVABCEFGIJKLMNOQRSTUWXY'
        text = pytesseract.image_to_string(thresh, config=config).strip()

        # Look for 4-digit year patterns
        year_match = re.search(r'\b(19|20)\d{2}\b', text)
        if year_match:
            year = year_match.group(0)
            # Look for mint marks or variety hints
            mint = ""
            if 'S' in text.upper(): mint = "-S"
            elif 'D' in text.upper(): mint = "-D"
            full_key = year + mint

            # Check for known varieties
            variety_hints = ["DDO", "DDR", "Close AM", "Wide AM", "No S", "No D"]
            variety = next((v for v in variety_hints if v.upper() in text.upper()), "")
            if variety:
                full_key += " " + variety

            if any(key in full_key for key in VALUABLE_PENNIES.keys()) or \
               any(full_key in key for key in VALUABLE_PENNIES.keys()):
                # Find closest match
                for key in VALUABLE_PENNIES:
                    if key.replace(" ", "") in full_key.replace(" ", "") or \
                       full_key.replace(" ", "") in key.replace(" ", ""):
                        return key
            return year  # At minimum return the year

        return None

    def analyze_frame(self, frame):
        _, edges, enhanced = self.preprocess_frame(frame)
        penny_circle = self.detect_penny_circle(edges)
        date = self.read_date_roi(frame, penny_circle) if penny_circle else None

        value = VALUABLE_PENNIES.get(date, 0) if date else 0
        rarity = "KEY DATE!" if value > 1000 else "Valuable" if value > 50 else "Common"

        return {
            "penny_circle": penny_circle,
            "date": date,
            "value": value,
            "rarity": rarity
        }

    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("⚠️  Camera not available - falling back to static image mode if file exists")
            cap = cv2.VideoCapture('penny.jpg')  # optional fallback

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print("🪙 UNIVERSAL PENNY HUNTER v6.0 - ALL LINCOLN CENTS")
        print("🎯 Center any penny (1909+) | Q=Quit  S=Save Photo")

        frame_count = 0
        while self.running:
            ret, frame = cap.read()
            if not ret:
                print("No frame - exiting")
                break
            frame = cv2.flip(frame, 1)
            frame_count += 1

            analysis = self.analyze_frame(frame)
            display = frame.copy()

            if analysis["penny_circle"]:
                x, y, r = analysis["penny_circle"]
                color = (0, 255, 0) if analysis["value"] > 1000 else (0, 255, 255)
                cv2.circle(display, (x, y), r, color, 5)
                cv2.putText(display, "🪙 PENNY LOCKED", (x - r, y - r - 20),
                           cv2.FONT_HERSHEY_DUPLEX, 0.9, color, 2)

            # Overlay text
            y_pos = 30
            cv2.putText(display, "UNIVERSAL PENNY HUNTER v6.0", (10, y_pos),
                       cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
            y_pos += 35

            if analysis["date"]:
                value_text = f"${analysis['value']:,.0f}" if analysis["value"] > 0 else "Face Value"
                color = (0, 255, 255) if analysis["value"] > 1000 else (0, 255, 0)
                cv2.putText(display, f"DATE: {analysis['date']}", (10, y_pos),
                           cv2.FONT_HERSHEY_DUPLEX, 1.2, color, 3)
                y_pos += 45
                cv2.putText(display, value_text, (10, y_pos),
                           cv2.FONT_HERSHEY_DUPLEX, 1.5, color, 4)
                y_pos += 55
                cv2.putText(display, analysis["rarity"], (10, y_pos),
                           cv2.FONT_HERSHEY_DUPLEX, 1.0, color, 3)
            else:
                cv2.putText(display, "SCANNING FOR PENNY...", (10, y_pos),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

            cv2.putText(display, f"F:{frame_count} | Q=Quit S=Save", (10, 460),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

            cv2.imshow("🪙 UNIVERSAL PENNY HUNTER", display)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                filename = f"penny_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(filename, frame)
                print(f"💾 Saved: {filename}")

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    hunter = UniversalPennyHunter()
    hunter.run()
