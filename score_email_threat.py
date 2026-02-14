#!/usr/bin/env python3
"""
Simple threat scoring tool matching the Excel matrix logic.
Edit the CATEGORY definitions or plug in your own indicators.

Outputs:
- Final score (0-100)
- Classification: Safe / Suspicious / Malicious
"""

from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Category:
    name: str
    weight: float           # e.g., 0.30
    indicators: List[Tuple[str, str, float]]  # (indicator, evidence, score 0-10)

CATEGORIES = [
    Category("Sender Authenticity", 0.30, [
        ("SPF result","fail",10),
        ("DKIM result","none",10),
        ("DMARC result","fail/quarantine",10),
        ("From domain legitimacy","secure-paypal.com (not PayPal)",9),
    ]),
    Category("Routing & Infrastructure", 0.20, [
        ("Originating host","infected-pc / 45.67.89.101",9),
        ("Relay host","suspicious.host / 185.203.114.77",9),
        ("HELO/EHLO hygiene","suspicious.host",8),
    ]),
    Category("URL & Link Risk", 0.20, [
        ("HTML link destination","paypalphish.vercel.app",10),
        ("Plain vs HTML mismatch","plaintext paypal.com vs HTML phishing",9),
        ("Hosting platform risk","vercel.app (often abused)",7),
    ]),
    Category("Attachment Risk", 0.15, [
        ("Attachment type","Invoice_99431.docx (claimed)",8),
        ("Encoding / disguise","base64 payload not a real DOCX",7),
        ("User prompt to open attachment","explicit instruction",8),
    ]),
    Category("Social Engineering", 0.10, [
        ("Urgency/threat","account suspension",8),
        ("Generic greeting","Dear Customer",6),
        ("Financial lure","Unpaid invoice #99431",7),
    ]),
    Category("External Reputation / TI", 0.05, [
        ("VirusTotal (EML)","1/62: Suspected HTML.Phishing (VBA32)",6),
    ]),
]

def classify(score: float) -> str:
    if score >= 61:
        return "Malicious"
    if score >= 31:
        return "Suspicious"
    return "Safe"

def main():
    total = 0.0
    print("Category contributions:")
    for cat in CATEGORIES:
        avg = sum(s for _,_,s in cat.indicators) / len(cat.indicators)
        contrib = (avg/10.0) * cat.weight * 100.0
        total += contrib
        print(f"- {cat.name}: avg={avg:.1f}/10, weight={cat.weight:.0%}, contrib={contrib:.1f}")

    print(f"\nFinal Threat Score: {total:.1f}/100")
    print(f"Classification: {classify(total)}")

if __name__ == "__main__":
    main()
