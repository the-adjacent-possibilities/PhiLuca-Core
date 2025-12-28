#!/usr/bin/env python3
"""
🌌 UNIVERSAL ESQET DETECTOR v5.3 - TERMUX READY
🔍 Coins/Jewelry/Art/Bottles/Books - φ-Geometry Analysis
"""

import cv2
import numpy as np
import math
from datetime import datetime

PHI = (1 + math.sqrt(5)) / 2

class UniversalESQETDetector:
    def __init__(self):
        self.running = True
        
    def preprocess_universal(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ksize = int(7 * PHI); ksize += 1 if ksize % 2 == 0 else 0
        blurred = cv2.GaussianBlur(gray, (ksize, ksize), 0)
        edges = cv2.Canny(blurred, 40, int(60 * PHI))
        return gray, edges, blurred
    
    def detect_coins(self, edges):
        circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1.2, 30,
                                  param1=50, param2=25, minRadius=10, maxRadius=50)
        return {"type": "🪙 COIN", "count": len(circles[0]) if circles is not None else 0, 
                "value": "Date scan needed"} if circles is not None else None
    
    def detect_bottles(self, edges):
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        tall = [c for c in contours if cv2.contourArea(c) > 2000 and 
               cv2.boundingRect(c)[3] > cv2.boundingRect(c)[2] * 1.3]
        return {"type": "🍾 BOTTLE", "count": len(tall), "value": "Pontil check"} if tall else None
    
    def detect_jewelry(self, gray):
        bright = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
        contours, _ = cv2.findContours(bright, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        shiny = [c for c in contours if 50 < cv2.contourArea(c) < 800]
        return {"type": "💍 JEWELRY", "count": len(shiny), "value": "925/14K scan"} if shiny else None
    
    def detect_art(self, edges):
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rects = [c for c in contours if len(c) > 8 and cv2.contourArea(c) > 5000]
        return {"type": "🎨 ART", "count": len(rects), "value": "Signature scan"} if rects else None
    
    def universal_analyze(self, frame):
        gray, edges, _ = self.preprocess_universal(frame)
        detections = []
        
        # Run all detectors
        coin = self.detect_coins(edges)
        bottle = self.detect_bottles(edges)
        jewelry = self.detect_jewelry(gray)
        art = self.detect_art(edges)
        
        if coin: detections.append(coin)
        if jewelry: detections.append(jewelry)
        if bottle: detections.append(bottle)
        if art: detections.append(art)
        
        # φ-GEOMETRY
        moments = cv2.moments(edges)
        if moments["m00"] > 0:
            cx, cy = int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])
            phi_ratio = abs((cx - 320) / (cy - 240) - PHI) if cy != 240 else 999
            if phi_ratio < 0.5:
                detections.append({"type": "📐 φ-GOLDEN", "phi_ratio": phi_ratio, "value": f"φ={phi_ratio:.2f}"})
        
        return detections[:4]
    
    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        
        print("🌌 UNIVERSAL DETECTOR v5.3 LIVE | Termux Ready")
        print("🎯 POINT AT TREASURE | Q=Quit S=Save")
        
        frame_count = 0
        while self.running:
            ret, frame = cap.read()
            if not ret: continue
            frame = cv2.flip(frame, 1)
            frame_count += 1
            
            detections = self.universal_analyze(frame)
            display = frame.copy()
            
            # Draw detections
            for i, detection in enumerate(detections):
                y_start = 40 + i * 70
                color = (0, 255, 0) if "COIN" in detection["type"] else (0, 255, 255)
                color = (0, 0, 255) if "JEWELRY" in detection["type"] else color
                
                cv2.rectangle(display, (10, y_start-25), (780, y_start+40), color, 3)
                cv2.putText(display, detection["type"], (20, y_start),
                           cv2.FONT_HERSHEY_DUPLEX, 1.1, color, 3)
                cv2.putText(display, detection["value"][:50], (20, y_start+32),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
            
            status = f"φ-ACTIVE | Finds: {len(detections)} | F:{frame_count}"
            cv2.putText(display, status, (10, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            
            cv2.imshow("🌌 ESQET UNIVERSAL DETECTOR", display)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.running = False
            elif key == ord('s') and detections:
                filename = f"treasure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(filename, frame)
                print(f"💾 SAVED: {filename}")
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = UniversalESQETDetector()
    detector.run()
