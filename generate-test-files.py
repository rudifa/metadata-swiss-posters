import os
from pathlib import Path

# Créer le répertoire pour les fichiers de test s'il n'existe pas
test_dir = Path("test_posters")
test_dir.mkdir(exist_ok=True)

# Collection d'exemples d'affiches
posters = [
    {
        "filename": "exposition_hodler.txt",
        "content": """FERDINAND HODLER
MAÎTRE DU SYMBOLISME
Une rétrospective majeure

Kunsthaus Zürich
Du 28 septembre au 15 décembre 2024

Vernissage: Vendredi 27 septembre à 18h
Visite guidée tous les mercredis à 14h30

Prix d'entrée:
Adultes: CHF 25.-
AVS/AI: CHF 18.-
Étudiants: CHF 12.-

www.kunsthaus.ch
info@kunsthaus.ch
+41 44 253 84 84"""
    },
    {
        "filename": "festival_jazz.txt",
        "content": """MONTREUX JAZZ FESTIVAL
58e édition

5-20 juillet 2024
Montreux Music & Convention Centre

TÊTES D'AFFICHE:
Marcus Miller
Herbie Hancock
Diana Krall
Robert Glasper

Billets en vente:
www.montreuxjazz.ch
Ticketcorner +41 900 800 800

Pass Festival: CHF 980.-
Billets journaliers dès CHF 75.-"""
    },
    {
        "filename": "theatre_moliere.txt",
        "content": """THÉÂTRE DE CAROUGE
présente

LE MALADE IMAGINAIRE
de Molière
Mise en scène: Omar Porras

du 12 au 31 mars 2024
mardi-samedi 19h30
dimanche 17h00

Avec:
Jean-Marc Rohrer
Marie Fontannaz
Philippe Mathey

Réservations:
www.theatredecarouge.ch
+41 22 343 43 43

Tarifs: CHF 45.- / CHF 35.- / CHF 20.-"""
    },
    {
        "filename": "design_biennale.txt",
        "content": """BIENNALE DU DESIGN SUISSE
DESIGN NOW!

Mudac Lausanne
15.05 - 30.08.2024

EXPOSANTS:
Studio Big-Game
Atelier Oï
ECAL Alumni
Norm Architects

Conférences • Ateliers • Tables rondes
Programme complet sur www.mudac.ch

Entrée libre
Contact: design@mudac.ch
+41 21 315 25 30"""
    },
    {
        "filename": "concert_classique.txt",
        "content": """ORCHESTRE DE LA SUISSE ROMANDE
Direction: Jonathan Nott

MAHLER
Symphonie No 2 "Résurrection"

Victoria Hall, Genève
Jeudi 5 septembre 2024, 20h00

Solistes:
Rachel Harnisch, soprano
Marie-Claude Chappuis, alto

Billetterie:
www.osr.ch
+41 22 807 00 00

Places de CHF 20.- à CHF 120.-"""
    },
    {
        "filename": "expo_photo.txt",
        "content": """REGARDS CROISÉS
PHOTOGRAPHIE CONTEMPORAINE SUISSE

Fotomuseum Winterthur
23.04 - 15.08.2024

Commissaire: Nadine Wietlisbach

PHOTOGRAPHES:
Karlheinz Weinberger
Annelies Štrba
Christian Schwager
Cat Tuong Nguyen

Vernissage: 22.04.2024, 18h30
Visites guidées: chaque dimanche 11h

info@fotomuseum.ch
+41 52 234 10 60
www.fotomuseum.ch"""
    },
    {
        "filename": "salon_livre.txt",
        "content": """34e SALON DU LIVRE DE GENÈVE
Palexpo

26-30 avril 2024
10h00 - 19h00

INVITÉ D'HONNEUR:
Les éditions suisses

200 auteurs
450 éditeurs
750 événements

Dédicaces • Conférences
Ateliers d'écriture • Lectures

Entrée:
1 jour: CHF 15.-
5 jours: CHF 30.-
Gratuit jusqu'à 18 ans

www.salondulivre.ch
info@palexpo.ch"""
    },
    {
        "filename": "art_contemporain.txt",
        "content": """ART BASEL
La foire internationale d'art

11-16 juin 2024
Messe Basel

289 GALERIES
33 PAYS
4000 ARTISTES

Art Unlimited
Art Statements
Art Feature
Art Films

Tickets online:
www.artbasel.com

Day Ticket: CHF 65.-
Permanent Pass: CHF 120.-

Contact:
visit@artbasel.com
+41 58 206 28 28"""
    },
    {
        "filename": "danse_contemporaine.txt",
        "content": """STEPS
Festival de Danse Contemporaine

Présente:
PIXEL
Cie Käfig / Mourad Merzouki

Théâtre de Beaulieu, Lausanne
17 & 18 avril 2024, 20h30

Une fusion spectaculaire
entre danse hip-hop et arts numériques

Réservations:
www.steps.ch
+41 21 642 21 21

Prix des places:
CHF 25.- à CHF 85.-"""
    },
    {
        "filename": "conference_architecture.txt",
        "content": """HABITER DEMAIN
Symposium d'Architecture

ETH Zürich
Hönggerberg Campus
18-19 octobre 2024

INTERVENANTS:
Jacques Herzog
Peter Zumthor
Gion A. Caminada
Anne Lacaton

Langue: Allemand/Français
Traduction simultanée

Inscription obligatoire:
www.arch.ethz.ch/symposium
arch.symposium@ethz.ch

Frais de participation:
Professionnels: CHF 380.-
Étudiants: CHF 80.-"""
    }
]

# Écrire chaque affiche dans un fichier
for poster in posters:
    filepath = test_dir / poster["filename"]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(poster["content"])

print(f"Créé {len(posters)} fichiers d'exemple dans le dossier '{test_dir}':")
for poster in posters:
    print(f"- {poster['filename']}")
