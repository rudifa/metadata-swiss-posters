import json
from datetime import datetime
from typing import Dict, List, Optional
import spacy
from difflib import SequenceMatcher

class LearningPosterAnalyzer:
    def __init__(self, rules_file="learned_rules.json"):
        self.nlp = spacy.load("fr_core_news_lg")
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
        # Analyse de base
        base_results = super().analyze_poster_text(text)
        
        # Appliquer les règles apprises
        for field in ['title', 'artist']:
            learned_value = self.apply_learned_rules(text, field)
            if learned_value:
                base_results[field] = learned_value
        
        return base_results

# Exemple d'utilisation
def main():
    analyzer = LearningPosterAnalyzer()
    
    # Analyse initiale
    text = """EXPOSITION
    Jean Dubuffet - Rétrospective
    du 15.03.2024 au 30.04.2024
    Kunsthaus Zürich"""
    
    results = analyzer.analyze_with_learning(text)
    
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
