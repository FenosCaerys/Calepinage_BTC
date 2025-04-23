# Application de Calepinage BTC

## Description

Cette application permet de faciliter le calepinage des Blocs de Terre Comprimée (BTC) pour la construction de murs. Le calepinage est l'étude préalable de la disposition et de l'assemblage des éléments de construction, permettant d'optimiser l'utilisation des matériaux, d'éviter les coupes inutiles, et de garantir la solidité et l'esthétique de l'ouvrage.

## Qu'est-ce que le calepinage ?

Le calepinage est une technique essentielle dans la construction qui consiste à planifier précisément comment les éléments de construction (comme les BTC) seront disposés. Cette planification permet de :
- Éviter les coupes inutiles de matériaux
- Optimiser l'utilisation des ressources
- Assurer une esthétique cohérente
- Garantir la solidité structurelle de l'ouvrage

## Fonctionnalités

- Saisie des dimensions du mur (longueur, épaisseur, hauteur)
- Génération automatique du plan de calepinage avec alternance des couches
- Calcul du nombre de blocs nécessaires par type (standard, 3/4, 1/2)
- Visualisation graphique du calepinage (si matplotlib est disponible)
- Interface graphique intuitive (si PyQt5 est disponible)
- Mode console pour une utilisation sans dépendances graphiques
- Prise en compte de la répétition des deux couches de blocs avec décalage

## Types de blocs supportés

| Type de bloc | Longueur (cm) | Largeur (cm) | Hauteur (cm) | Utilisation |
|--------------|---------------|--------------|---------------|-------------|
| Standard     | 29,5          | 14           | 9,5           | Bloc principal pour la majorité des rangées |
| 3/4          | 21,75         | 14           | 9,5           | Utilisé pour les décalages d'appareil |
| 1/2          | 14            | 14           | 9,5           | Utilisé pour les finitions en bout de mur ou au début de rangée |

## Prérequis

- Python 3.6 ou supérieur

### Dépendances optionnelles

- PyQt5 (pour l'interface graphique)
- Matplotlib (pour la visualisation graphique)
- NumPy (pour les calculs matriciels)

## Installation

### Installation standard

```bash
# Cloner le dépôt (si applicable)
git clone <url-du-depot>
cd <dossier-du-projet>

# Option 1: Installation directe (si votre système le permet)
pip install -r requirements.txt

# Option 2: Utilisation d'un environnement virtuel (recommandé)
python3 -m venv btc_env
source btc_env/bin/activate  # Sur Windows: btc_env\Scripts\activate
pip install -r requirements.txt
```

### Installation sans dépendances graphiques

L'application peut fonctionner en mode console sans aucune dépendance externe :

```bash
# Simplement exécuter le script principal
python3 btc_calepinage.py
```

## Utilisation

### Avec interface graphique

```bash
# Si vous avez installé PyQt5
python btc_calepinage.py
```

1. Entrez les dimensions du mur (longueur, épaisseur, hauteur) en centimètres
2. Cliquez sur "Calculer le calepinage"
3. Consultez le tableau récapitulatif des blocs nécessaires
4. Visualisez le plan de calepinage (si matplotlib est disponible)

### En mode console

```bash
python btc_calepinage.py
```

1. Suivez les instructions à l'écran pour entrer les dimensions du mur
2. Consultez le plan de calepinage généré en ASCII
3. Visualisez le plan graphiquement si matplotlib est disponible (option proposée)

## Structure du projet

- `btc_calepinage.py` : Application principale (mode console et GUI)
- `requirements.txt` : Liste des dépendances
- `README.md` : Documentation du projet

## Principes de calepinage

Le calepinage des BTC suit plusieurs principes importants :

1. **Alternance des couches** : Les blocs sont disposés en couches alternées pour éviter l'alignement des joints verticaux
2. **Décalage** : La seconde couche commence généralement par un demi-bloc pour assurer le décalage
3. **Optimisation** : L'application cherche à utiliser un maximum de blocs standards pour minimiser les coupes
4. **Adaptation** : Des blocs 3/4 et 1/2 sont utilisés pour les ajustements en fin de rangée

## Avantages du calepinage

- Réduction du gaspillage de matériaux
- Gain de temps sur le chantier
- Meilleure qualité de construction
- Esthétique améliorée
- Solidité structurelle optimisée

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à proposer des améliorations ou à signaler des problèmes.

## Licence

Ce projet est distribué sous licence libre.
# Calepinage_BTC
