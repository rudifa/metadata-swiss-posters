import json
from datetime import datetime
from typing import Dict, List, Optional
import spacy
from difflib import SequenceMatcher
import re

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

class LearningPosterAnalyzer(PosterTextAnalyzer):  # Maintenant hérite de PosterTextAnalyzer
    def __init__(self, rules_file="learned_rules.json"):
        super().__init__()  # Appelle le constructeur de la classe parente
        self.rules_file = rules_file
        
        # Charger les règles apprises
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                self.learned_rules = json.load(f)
        except FileNotFoundError:
            self.learned_rules = {
                'title_patterns': [],      # Patterns pour identifier les titres
                'artist_patterns': [],     # Patterns pour identifier les artistes
                'corrections': {},         # Corrections manuelles validées
                'context_rules': []        # Règles basées sur le contexte
            }
    
    def similarity_score(self, str1: str, str2: str) -> float:
        """Calcule un score de similarité entre deux chaînes."""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def apply_learned_rules(self, text: str, field_type: str) -> Optional[str]:
        """Applique les règles apprises pour extraire une information."""
        if field_type in self.learned_rules:
            for pattern in self.learned_rules[f'{field_type}_patterns']:
                # Vérifier si le pattern correspond avec une certaine tolérance
                if any(self.similarity_score(part, pattern) > 0.8 
                      for part in text.split('\n')):
                    return pattern
        return None
    
    def learn_from_correction(self, original: Dict, correction: Dict):
        """Apprend des corrections manuelles."""
        for field, value in correction.items():
            if field not in self.learned_rules['corrections']:
                self.learned_rules['corrections'][field] = []
            
            # Enregistrer le contexte de la correction
            context = {
                'original': original.get(field),
                'corrected': value,
                'timestamp': datetime.now().isoformat(),
                'surrounding_text': original.get('text', '')[:100]  # Contexte limité
            }
            
            self.learned_rules['corrections'][field].append(context)
            
            # Générer des règles basées sur le contexte
            if len(self.learned_rules['corrections'][field]) >= 3:
                self._generate_new_rules(field)
    
    def _generate_new_rules(self, field: str):
        """Génère de nouvelles règles basées sur les corrections récurrentes."""
        corrections = self.learned_rules['corrections'][field]
        
        # Analyser les patterns récurrents
        patterns = {}
        for corr in corrections[-10:]:  # Analyser les 10 dernières corrections
            original = corr['original']
            corrected = corr['corrected']
            
            # Identifier des patterns communs
            if original and corrected:
                pattern = self._extract_pattern(original, corrected)
                patterns[pattern] = patterns.get(pattern, 0) + 1
        
        # Ajouter les patterns fréquents aux règles
        for pattern, count in patterns.items():
            if count >= 3 and pattern not in self.learned_rules[f'{field}_patterns']:
                self.learned_rules[f'{field}_patterns'].append(pattern)
    
    def _extract_pattern(self, original: str, corrected: str) -> str:
        """Extrait un pattern de correction basé sur l'original et la correction."""
        # Simplifié pour l'exemple, pourrait être plus sophistiqué
        return f"{original} -> {corrected}"
    
    def save_rules(self):
        """Sauvegarde les règles apprises."""
        with open(self.rules_file, 'w', encoding='utf-8') as f:
            json.dump(self.learned_rules, f, ensure_ascii=False, indent=2)
    
    def analyze_with_learning(self, text: str) -> Dict:
        """Analyse le texte en appliquant les règles apprises."""
        # Analyse de base en utilisant la méthode de la classe parente
        base_results = super().analyze_poster_text(text)
        
        # Appliquer les règles apprises
        for field in ['title', 'artist']:
            learned_value = self.apply_learned_rules(text, field)
            if learned_value:
                base_results[field] = learned_value
        
        return base_results

def main():
    analyzer = LearningPosterAnalyzer()
    
    # Analyse initiale
    text = """EXPOSITION
    Jean Dubuffet - Rétrospective
    du 15.03.2024 au 30.04.2024
    Kunsthaus Zürich"""
    
    results = analyzer.analyze_with_learning(text)
    print("Résultats de l'analyse :", json.dumps(results, ensure_ascii=False, indent=2))
    
    # Simulation d'une correction par un utilisateur
    correction = {
        'title': 'Jean Dubuffet - Rétrospective',
        'artist': 'Jean Dubuffet'
    }
    
    # Apprentissage de la correction
    analyzer.learn_from_correction(results, correction)
    analyzer.save_rules()

if __name__ == "__main__":
    main()
