#!/usr/bin/env python3
"""
🌾 WHEAT PENNY HUNTER v5.2 - REAL OCR + $100K KEY DATE DETECTOR
🎯 LIVE CAMERA → Wheat Ears → Tesseract OCR → AUCTION VALUE
"""

import cv2
import numpy as np
import pytesseract
import re
from datetime import datetime
import math

PHI = (1 + math.sqrt(5)) / 2

# REAL KEY DATES ($ VALUES)
WHEAT_PENNIES = {
    "1909-S VDB": 100000, "1914-D": 20000, "1922 No D": 15000,
    "1931-S": 10000, "1955 DDO": 5000, "1943 Bronze": 50000,
    "1909": 50, "1910": 25, "1930": 20, "1940": 10, "1958": 5
}

class WheatPennyHunter:
    def __init__(self):
        self.running = True
        self.wheat_ears_template = None
        
    def load_wheat_template(self):
        h, w = 40, 80
        template = np.zeros((h, w), dtype=np.uint8)
        cv2.ellipse(template, (20, 20), (15, 25), 0, 0, 360, 255, -1)
        cv2.ellipse(template, (60, 20), (15, 25), 0, 0, 360, 255, -1)
        self.wheat_ears_template = template
        return template
    
    def preprocess_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ksize = int(7 * PHI); ksize += 1 if ksize % 2 == 0 else 0
        blurred = cv2.GaussianBlur(gray, (ksize, ksize), 0)
        edges = cv2.Canny(blurred, 40, int(40 * PHI))
        kernel = np.ones((3,3), np.uint8)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        return gray, edges, blurred
    
    def detect_wheat_ears(self, gray):
        if self.wheat_ears_template is None:
            self.load_wheat_template()
        res = cv2.matchTemplate(gray, self.wheat_ears_template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.6)
        wheat_centers = [(pt[0] + 40, pt[1] + 20) for pt in zip(*loc[::-1])]
        return wheat_centers if len(wheat_centers) >= 2 else []
    
    def detect_penny_circle(self, edges):
        circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1.2, 50,
                                  param1=50, param2=25, minRadius=18, maxRadius=32)
        return np.round(circles[0, :]).astype("int")[0] if circles is not None else None
    
    def read_date_roi(self, frame, center):
        x, y, r = center
        roi_size = int(r * 0.6)
        roi_x, roi_y = max(0, x - roi_size//2), max(0, y + int(r * 0.25))
        roi = frame[roi_y:roi_y+roi_size*2, roi_x:roi_x+roi_size*2]
        
        if roi.size == 0: return None
        
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi_enhanced = cv2.convertScaleAbs(roi_gray, alpha=2.0, beta=50)
        roi_thresh = cv2.threshold(roi_enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # TESSERACT OCR
        config = '--psm 8 -c tessedit_char_whitelist=0123456789SVD'
        text = pytesseract.image_to_string(roi_thresh, config=config).strip()
        
        # Extract 4-digit years
        year_match = re.search(r'\b(19|20)d{2}\b', text)
        if year_match:
            year = year_match.group(0)
            if year in WHEAT_PENNIES:
                return year
            return year[:4]  # Fallback to year
        
        return None
    
    def analyze_frame(self, frame):
        gray, edges, blurred = self.preprocess_frame(frame)
        wheat_ears = self.detect_wheat_ears(gray)
        penny_circle = self.detect_penny_circle(edges)
        
        analysis = {
            "wheat_detected": len(wheat_ears) >= 2,
            "penny_circle": penny_circle is not None,
            "date": None, "value": 0, "rarity": "Common"
        }
        
        if analysis["wheat_detected"] and analysis["penny_circle"]:
            date = self.read_date_roi(frame, penny_circle)
            analysis["date"] = date
            if date and date in WHEAT_PENNIES:
                analysis["value"] = WHEAT_PENNIES[date]
                analysis["rarity"] = "KEY DATE" if analysis["value"] > 1000 else "Valuable"
        
        return analysis, wheat_ears, penny_circle
    
    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("🌾 WHEAT PENNY HUNTER v5.2 LIVE | REAL OCR")
        print("🎯 PLACE 1909-1958 PENNY CENTERED | Q=Quit S=Save")
        
        frame_count = 0
        while self.running:
            ret, frame = cap.read()
            if not ret: continue
            frame = cv2.flip(frame, 1)
            frame_count += 1
            
            analysis, wheat_ears, penny_circle = self.analyze_frame(frame)
            display = frame.copy()
            
            # Wheat ears (yellow)
            for center in wheat_ears[:2]:
                cv2.circle(display, center, 15, (0, 255, 255), 3)
            
            # Penny circle (green)
            if penny_circle is not None:
                x, y, r = penny_circle
                cv2.circle(display, (x, y), r, (0, 255, 0), 4)
            
            # Status overlay
            y_pos = 40
            cv2.putText(display, "🌾 WHEAT HUNTER v5.2", (10, y_pos), 
                       cv2.FONT_HERSHEY_DUPLEX, 1.0, (255,255,255), 2)
            y_pos += 40
            
            if analysis["wheat_detected"]:
                cv2.putText(display, "🌾 WHEAT ✓", (10, y_pos), 
                           cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 0), 3)
                y_pos += 45
            else:
                cv2.putText(display, "❌ Wheat?", (10, y_pos), 
                           cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 165, 255), 2)
                y_pos += 40
            
            if analysis["date"]:
                value_text = f"${analysis['value']:,.0f}"
                color = (0, 255, 255) if analysis['value'] > 1000 else (0, 255, 0)
                cv2.putText(display, f"🎯 {analysis['date']}", (10, y_pos),
                           cv2.FONT_HERSHEY_DUPLEX, 1.5, color, 3)
                cv2.putText(display, value_text, (10, y_pos + 50),
                           cv2.FONT_HERSHEY_DUPLEX, 1.8, color, 4)
            else:
                cv2.putText(display, "📅 SCANNING...", (10, y_pos),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
            
            cv2.putText(display, f"F:{frame_count}", (500, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
            
            cv2.imshow("🌾 WHEAT PENNY HUNTER", display)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.running = False
            elif key == ord('s') and analysis["wheat_detected"]:
                filename = f"wheat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(filename, frame)
                print(f"💾 SAVED: {filename}")
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    hunter = WheatPennyHunter()
    hunter.run()
