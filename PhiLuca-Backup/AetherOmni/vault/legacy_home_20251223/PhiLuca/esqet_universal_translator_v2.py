#!/usr/bin/env python3
"""
🌍 ESQET UNIVERSAL TRANSLATOR v5.2 - ENHANCED LOCAL OCR + SMART DICTIONARY
"""

import cv2
import numpy as np
import pytesseract
from datetime import datetime

PHI = (1 + np.sqrt(5)) / 2

# EXPANDED LOCAL DICTIONARY (English ↔ Spanish/French/German/Italian + Treasure Terms)
TRANSLATE_DICT = {
    # Common
    "hello": "hola", "hola": "hello",
    "thank you": "gracias", "gracias": "thank you",
    "please": "por favor", "por favor": "please",
    "goodbye": "adiós", "adiós": "goodbye",
    "yes": "sí", "sí": "yes",
    "no": "no", "no": "no",
    "water": "agua", "agua": "water",
    "food": "comida", "comida": "food",
    "money": "dinero", "dinero": "money",
    "store": "tienda", "tienda": "store",
    "open": "abierto", "abierto": "open",
    "closed": "cerrado", "cerrado": "closed",
    "bathroom": "baño", "baño": "bathroom",
    "menu": "menú", "menú": "menu",
    
    # French
    "merci": "thank you", "bonjour": "hello", "au revoir": "goodbye",
    
    # German
    "danke": "thank you", "hallo": "hello",
    
    # Italian
    "grazie": "thank you", "ciao": "hello",
    
    # Treasure/Art Terms
    "antique": "antiguo", "antiguo": "antique",
    "vintage": "vintage", "rare": "raro", "raro": "rare",
    "silver": "plata", "plata": "silver",
    "gold": "oro", "oro": "gold",
    "coin": "moneda", "moneda": "coin",
    "painting": "pintura", "pintura": "painting",
    "signature": "firma", "firma": "signature"
}

class ESQETUniversalTranslator:
    def __init__(self):
        self.running = True
        # Better Tesseract config
        self.tess_config = '--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789áéíóúñ¿¡.,;!?"\' '
        
    def preprocess_text_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # φ-Gaussian
        ksize = int(5 * PHI); ksize += 1 if ksize % 2 == 0 else 0
        blurred = cv2.GaussianBlur(gray, (ksize, ksize), 0)
        # Better contrast
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(blurred)
        # Adaptive threshold
        thresh = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 21, 10)
        return enhanced, thresh
    
    def extract_text(self, frame, bbox):
        x, y, w, h = bbox
        roi = frame[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi, config=self.tess_config)
        return text.strip().lower()
    
    def translate_text(self, text):
        if not text: return ""
        # Whole-word or phrase match
        for key, value in TRANSLATE_DICT.items():
            if key in text:
                return value
        return "..."  # Unknown
    
    def detect_text_boxes(self, thresh):
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        boxes = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if 100 < w*h < 30000 and 10 < h < 200 and 0.5 < w/h < 15:
                boxes.append((x, y, w, h))
        return sorted(boxes, key=lambda b: b[1])[:10]
    
    def run(self):
        cap = cv2.VideoCapture(0)
        print("🌍 ESQET UNIVERSAL TRANSLATOR v5.2 LIVE")
        print("Point at foreign text → instant local translation")
        
        while self.running:
            ret, frame = cap.read()
            if not ret: continue
            frame = cv2.flip(frame, 1)
            
            _, thresh = self.preprocess_text_frame(frame)
            boxes = self.detect_text_boxes(thresh)
            
            display = frame.copy()
            translations = []
            
            for box in boxes:
                text = self.extract_text(frame, box)
                translated = self.translate_text(text)
                if translated != "...":
                    translations.append((box, text[:20], translated))
                    
                    # Draw overlay
                    x, y, w, h = box
                    cv2.rectangle(display, (x, y), (x+w, y+h), (0, 255, 255), 2)
                    cv2.rectangle(display, (x, y-40), (x+250, y), (0, 100, 255), -1)
                    cv2.putText(display, translated.upper(), (x+5, y-10),
                               cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
            
            status = f"Found: {len(translations)} | φ-Active"
            cv2.putText(display, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)
            
            cv2.imshow("🌍 ESQET TRANSLATOR", display)
            if cv2.waitKey(1) == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    translator = ESQETUniversalTranslator()
    translator.run()
