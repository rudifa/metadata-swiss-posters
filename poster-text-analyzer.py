import re
from datetime import datetime
import spacy
from typing import Dict, List, Optional


class PosterTextAnalyzer:
    def __init__(self):
        # Charger le modèle français de spaCy
        self.nlp = spacy.load("fr_core_news_lg")

        # Patterns réguliers pour différents types d'informations
        self.patterns = {
            'date': r'\b\d{1,2}[\s.-]\d{1,2}[\s.-]\d{2,4}\b|\b\d{4}\b',
            'website': r'www\.[a-zA-Z0-9-]+\.[a-zA-Z]{2,}|https?://[^\s]+',
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'phone': r'\b(?:\+41|0)\s*\d{2}\s*\d{3}\s*\d{2}\s*\d{2}\b',
            'price': r'\b\d+[\s.-]?(?:CHF|Fr\.|francs?)\b|\b(?:CHF|Fr\.)\s*\d+\b',
            'time': r'\b\d{1,2}h\d{2}\b|\b\d{1,2}:\d{2}\b'
        }

        # Mots-clés pour identifier le type d'événement
        self.event_keywords = {
            'exposition': ['exposition', 'vernissage', 'galerie', 'musée'],
            'concert': ['concert', 'festival', 'scène', 'musique'],
            'théâtre': ['théâtre', 'pièce', 'spectacle', 'représentation'],
            'conférence': ['conférence', 'séminaire', 'symposium']
        }

    def extract_dates(self, text: str) -> List[str]:
        """Extrait toutes les dates du texte."""
        return re.findall(self.patterns['date'], text)

    def extract_contact_info(self, text: str) -> Dict[str, List[str]]:
        """Extrait les informations de contact."""
        contact_info = {}
        for info_type in ['website', 'email', 'phone']:
            matches = re.findall(self.patterns[info_type], text)
            if matches:
                contact_info[info_type] = matches
        return contact_info

    def extract_prices(self, text: str) -> List[str]:
        """Extrait les informations de prix."""
        return re.findall(self.patterns['price'], text)

    def identify_event_type(self, text: str) -> Optional[str]:
        """Identifie le type d'événement basé sur les mots-clés."""
        text_lower = text.lower()
        for event_type, keywords in self.event_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return event_type
        return None

    def extract_location(self, text: str) -> List[str]:
        """Extrait les lieux mentionnés dans le texte."""
        doc = self.nlp(text)
        locations = []
        for ent in doc.ents:
            if ent.label_ in ['LOC', 'GPE']:
                locations.append(ent.text)
        return locations

    def extract_organizations(self, text: str) -> List[str]:
        """Extrait les organisations mentionnées."""
        doc = self.nlp(text)
        return [ent.text for ent in doc.ents if ent.label_ == 'ORG']

    def analyze_poster_text(self, text: str) -> Dict:
        """Analyse complète du texte d'une affiche."""
        results = {
            'dates': self.extract_dates(text),
            'contact_info': self.extract_contact_info(text),
            'prices': self.extract_prices(text),
            'event_type': self.identify_event_type(text),
            'locations': self.extract_location(text),
            'organizations': self.extract_organizations(text)
        }

        # Tentative d'identification du titre
        lines = text.split('\n')
        if lines:
            # Suppose que la première ligne non vide est probablement le titre
            title = next((line for line in lines if line.strip()), '')
            results['probable_title'] = title

        return results


def main():
    # Exemple d'utilisation
    analyzer = PosterTextAnalyzer()
    sample_text = """EXPOSITION
    Art Contemporain Suisse
    du 15.03.2024 au 30.04.2024
    Musée des Beaux-Arts de Lausanne
    Vernissage le jeudi 14 mars à 18h30
    Entrée: CHF 15.-
    Contact: info@mba.ch
    www.mba.ch
    +41 21 316 34 45"""

    results = analyzer.analyze_poster_text(sample_text)

    # Affichage des résultats
    for key, value in results.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
