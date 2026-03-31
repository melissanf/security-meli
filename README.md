# Analyse de Fréquence de la Langue Arabe et Cryptanalyse

Une application complète pour analyser la fréquence des lettres dans les textes arabes et casser des chiffrements classiques (César, Affine, Substitution) en utilisant l'analyse de fréquence.

## Fonctionnalités

- **Analyse de Corpus** : Génère un tableau de fréquences basé sur des textes arabes et des statistiques linguistiques standard
- **Déchiffrement par Fréquence** : Compare les statistiques d'un texte chiffré avec la fréquence standard pour retrouver le texte clair
- **Support des Chiffres Classiques** :
  - **César** (décalage simple de 0 à 27)
  - **Affine** (formule : $c(x) = ax + b \pmod{28}$)
  - **Substitution** (mappage lettre à lettre)
- **Interface Graphique Simple** : Une UI intuitive basée sur Flask pour charger un texte et visualiser les résultats
- **Gestion Unicode Complète** : Support natif de l'alphabet arabe (28 lettres) avec gestion des diacritiques (Tashkeel)

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Méthodologie](#méthodologie)
- [Structure du Projet](#structure-du-projet)
- [API et Fonctions Principales](#api-et-fonctions-principales)
- [Exemples d'Utilisation](#exemples-dutilisation)
- [Notes Techniques](#notes-techniques)

## Installation

### Prérequis

- **Python** 3.7 ou supérieur
- **Flask** 3.0.0+ (installé automatiquement via requirements.txt)

### Étapes

1. **Clonez ou téléchargez le projet** :
**clonez depuis github**
   ```bash
   git clone https://github.com/melissanf/security-meli.git
   cd security-meli
   ```
**telechargez le document**

```
doc > ouvrir avec votre IDE 
```

2.Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

3.*Lancez l'application*:

   ```bash
   python main.py
   ```
4. **Accédez à l'application** :
   Ouvrez votre navigateur à **http://127.0.0.1:5000**

## Utilisation

### Interface Web

### Interface Web

#### Étapes pour utiliser l'application :

1. **Charger un texte chiffré** :
   - Tapez directement votre texte dans la zone « Texte a Analyser »
   - Ou cliquez sur « Charger Exemple » pour charger un exemple de démonstration
   - Ou cliquez sur « Effacer » pour vider la zone de texte

2. **Sélectionner le type d'attaque** :
   - **Chiffre de Cesar** : Teste tous les décalages possibles (0-27)
   - **Chiffre Affine** : Teste toutes les clés valides (a, b)
   - **Chiffre de Substitution** : Utilise l'analyse de fréquence pour une substitution générale
   - **Analyse de Frequence Simple** : Affiche simplement les fréquences du texte

3. **Configurer les paramètres** :
   - Ajustez le nombre de resultats à afficher (1-20)

4. **Lancer l'attaque** :
   - Cliquez sur « Lancer l'Attaque »
   - Les resultats s'affichent dans les onglets « Candidats », « Frequences » et « Reference »

#### Onglets disponibles :

- **Candidats** : Affiche les résultats de l'attaque triés par score
- **Frequences** : Affiche un graphique en barres des fréquences détectées
- **Reference** : Affiche le tableau de fréquence de référence pour l'arabe

### Utilisation Programmatique

```python
from crypto_logic import (
    calculate_frequency, attack_caesar_frequency,
    attack_affine_frequency, attack_substitution_frequency
)
from utils import clean_arabic_text

# Analyser la fréquence d'un texte
text = "أتاح الإنترنت للملايين من الناس إمكانية الاتصال"
freq = calculate_frequency(text)
print(freq)  # {'ا': 0.15, 'ن': 0.10, ...}

# Attaquer un chiffre de César
ciphertext = "بتبذ الإوتروت للملبيين من الوبس إمكبويت الباتصبل"
caesar_results = attack_caesar_frequency(ciphertext)
print(caesar_results[0])  # Meilleur candidat

# Attaquer un chiffre Affine
affine_results = attack_affine_frequency(ciphertext)
print(affine_results[0]['key'])  # (a, b)

# Attaquer un chiffre de Substitution
substitution_results = attack_substitution_frequency(ciphertext)
print(substitution_results[0]['plaintext'])  # Texte probable
```

### Endpoints API

L'application expose également une API REST pour une utilisation programmatique :

- `GET /` - Charge la page d'accueil
- `POST /api/analyze` - Analyse un texte et calcule ses fréquences
- `POST /api/attack` - Lance une attaque cryptographique
- `GET /api/example` - Retourne un exemple de texte arabe
- `GET /api/reference-frequency` - Retourne le tableau de fréquence de référence

## Méthodologie

### 1. Prétraitement du Texte

Le texte arabe subit un nettoyage complet :

- **Suppression des diacritiques (Tashkeel)** : Les signes de vocalisation arabes (Fatha, Damma, Kasra, etc.) sont supprimés
- **Normalisation des variantes** : Les lettres variantes sont normalisées à leurs formes de base :
  - `ة` (Taa Marbuta) → `ه` (Ha)
  - `ى` (Alef Maksura) → `ا` (Alef)
  - `أ`, `إ`, `آ` → `ا` (Alef)
- **Suppression des caractères non-arabes** : Seules les 28 lettres arabes de base sont conservées

### 2. Calcul de la Fréquence

Pour chaque lettre de l'alphabet arabe, on calcule :

$$f(c) = \frac{n_c}{N}$$

Où :

- $n_c$ : nombre d'occurrences du caractère $c$
- $N$ : nombre total de caractères arabes dans le texte

### 3. Mesure de Similitude : Test du Chi-Carré

Pour évaluer la proximité entre deux distributions de fréquences, on utilise le test du Chi-carré :

$$\chi^2 = \sum_{c=1}^{28} \frac{(f_{observée}(c) - f_{référence}(c))^2}{f_{référence}(c)}$$

**Plus la valeur $\chi^2$ est faible, meilleure est la correspondance.**

### 4. Attaques Cryptographiques

#### **Chiffre de César**

- Teste tous les décalages possibles (0 à 27)
- Pour chaque décalage, calcule les fréquences du texte déchiffré
- Classe les résultats par score Chi-carré croissant

**Déchiffrement** : Si $c(x) = x + k \pmod{28}$, alors $x = c(y) - k \pmod{28}$

#### **Chiffre Affine**

- Teste toutes les clés valides $(a, b)$ où $\gcd(a, 28) = 1$
- Il y a $\phi(28) \times 28 = 12 \times 28 = 336$ clés possibles
- Classe les résultats par score Chi-carré

**Déchiffrement** : $x = a^{-1} \times (y - b) \pmod{28}$

#### **Chiffre de Substitution**

- Mappe les lettres du texte chiffré aux lettres de l'alphabet arabe
- Utilise l'analyse de fréquence : la lettre la plus fréquente du chiffré est mappée à la lettre la plus fréquente en arabe
- Classe les résultats par similitude avec le tableau de fréquence de référence

### 5. Tableau de Fréquence de Référence

Basé sur des analyses linguistiques standard de la langue arabe moderne. Les 5 lettres les plus fréquentes sont :

| Lettre   | Fréquence | Pourcentage |
| -------- | --------- | ----------- |
| ا (Alef) | 0.0861    | 8.61%       |
| ل (Lam)  | 0.0761    | 7.61%       |
| م (Meem) | 0.0735    | 7.35%       |
| ن (Noon) | 0.0671    | 6.71%       |
| ي (Ya)   | 0.0635    | 6.35%       |

## Structure du Projet

```plaintext
security-meli/
├── app.py                    # Application Flask principale
├── main.py                   # Point d'entrée
├── crypto_logic.py           # Logique cryptographique et analyse
├── utils.py                  # Utilitaires traitement texte arabe
├── requirements.txt          # Dépendances Python
├── reference_freq.json       # Tableau de fréquence de référence
├── README.md                 # Cette documentation
├── templates/
│   └── index.html           # Interface web HTML/CSS/JS
├── venv/                     # Environnement virtuel (créé automatiquement)
└── __pycache__/              # Cache Python
```

## API et Fonctions Principales

### `utils.py`

```python
def clean_arabic_text(text: str) -> str
    """Nettoie complètement un texte arabe."""

def remove_diacritics(text: str) -> str
    """Supprime les diacritiques (Tashkeel)."""

def normalize_arabic_letters(text: str) -> str
    """Normalise les variantes de lettres."""

def get_text_info(text: str) -> dict
    """Retourne des statistiques sur le texte."""

def is_arabic_text(text: str) -> bool
    """Vérifie si le texte contient des caractères arabes."""
```

### `crypto_logic.py`

#### Analyse de Fréquence

```python
def calculate_frequency(text: str, return_counts=False) -> dict
    """Calcule les fréquences de chaque lettre."""

def chi_squared_test(observed: dict, expected: dict) -> float
    """Effectue un test Chi-carré entre deux distributions."""

def load_reference_frequency(filepath=None) -> dict
    """Charge le tableau de fréquence de référence."""

def save_reference_frequency(freq: dict, filepath: str)
    """Sauvegarde un tableau de fréquence."""
```

#### Attaques Cryptographiques

```python
def attack_caesar_frequency(ciphertext: str, reference_freq=None) -> list
    """Attaque un chiffre de César."""

def attack_affine_frequency(ciphertext: str, reference_freq=None, num_candidates=10) -> list
    """Attaque un chiffre Affine."""

def attack_substitution_frequency(ciphertext: str, reference_freq=None, num_candidates=5) -> list
    """Attaque un chiffre de Substitution."""
```

#### Déchiffrement

```python
def decrypt_caesar(ciphertext: str, shift: int) -> str
    """Déchiffre un texte chiffré par César."""

def decrypt_affine(ciphertext: str, a: int, b: int) -> str
    """Déchiffre un texte chiffré par Affine."""

def apply_substitution(ciphertext: str, key: dict) -> str
    """Applique une clé de substitution."""
```

## Exemples d'Utilisation

### Exemple 1 : Analyser la Fréquence d'un Texte

```python
from crypto_logic import calculate_frequency

text = "السلام عليكم ورحمة الله وبركاته"
frequencies = calculate_frequency(text)

# Afficher les fréquences
for letter, freq in sorted(frequencies.items(), key=lambda x: x[1], reverse=True):
    if freq > 0:
        print(f"{letter}: {freq:.4f} ({freq*100:.2f}%)")
```

### Exemple 2 : Casser un Chiffre de César

```python
from crypto_logic import attack_caesar_frequency

ciphertext = "بسبدة رسمدثة دبحة ديا دبحة بسبدة"
results = attack_caesar_frequency(ciphertext)

# Afficher les 3 meilleurs candidats
for i, result in enumerate(results[:3], 1):
    print(f"Candidat {i}:")
    print(f"  Décalage: {result['shift']}")
    print(f"  Score Chi-carré: {result['score']:.4f}")
    print(f"  Texte: {result['plaintext']}\n")
```

### Exemple 3 : Casser un Chiffre Affine

```python
from crypto_logic import attack_affine_frequency

ciphertext = "بسبدة رسمدثة"
results = attack_affine_frequency(ciphertext, num_candidates=5)

# Afficher les meilleurs résultats
for i, result in enumerate(results[:1], 1):
    print(f"Clé trouvée: a={result['a']}, b={result['b']}")
    print(f"Texte déchiffré: {result['plaintext']}")
```

### Exemple 4 : Charger et Sauvegarder une Fréquence Personnalisée

```python
from crypto_logic import save_reference_frequency, load_reference_frequency
from crypto_logic import calculate_frequency

# Calculer la fréquence d'un corpus
corpus = "نص عربي طويل جداً..."
custom_freq = calculate_frequency(corpus)

# Sauvegarder
save_reference_frequency(custom_freq, "mon_freq.json")

# Charger et utiliser
loaded_freq = load_reference_frequency("mon_freq.json")
```

## Notes Techniques

### Particularités de l'Alphabet Arabe

1. **28 Lettres de Base** :

   ```
   ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي
   ```

2. **Diacritiques (Tashkeel)** : Environ 8 signes de vocalisation principaux qui doivent être supprimés pour une analyse correcte

3. **Variantes de Forme** : Les lettres arabes changent de forme selon leur position (initiale, médiane, finale, isolée), mais pour l'analyse de fréquence, on traite la lettre comme une entité unique

4. **Unicode** : Les lettres arabes occupent la plage U+0600 à U+06FF

### Performance

- **César** : $O(28 \times n)$ où $n$ est la longueur du texte
- **Affine** : $O(336 \times n)$ (336 clés valides)
- **Substitution** : $O(n)$ avec une seule tentative de mappage

### Limitations

1. Fonctionne mieux avec des textes suffisamment longs (> 100 caractères)
2. L'analyse de fréquence suppose une distribution normale de lettres
3. Les textes courts ou spécialisés peuvent ne pas correspondre au tableau de référence
4. Ne détecte pas les chiffres autres que César, Affine et Substitution simples

## Concepts Mathématiques

### Modulo Arithmétique

Pour l'alphabet arabe avec 28 lettres :
$$a \equiv b \pmod{28} \iff 28 \text{ divise } (a - b)$$

### Inverse Modulaire

Pour le chiffre Affine, on a besoin de $a^{-1} \pmod{28}$ :
$$a \times a^{-1} \equiv 1 \pmod{28}$$

Cela n'existe que si $\gcd(a, 28) = 1$. Comme $28 = 4 \times 7$, les valeurs valides de $a$ sont :
$$a \in \{1, 3, 5, 9, 11, 13, 15, 17, 19, 23, 25, 27\}$$

Soit $\phi(28) = 12$ valeurs (Indicatrice d'Euler).

## Cas d'Usage

- **Éducation** : Enseigner la cryptographie et l'analyse de fréquence
- **Cryptanalyse** : Analyse de textes chiffrés historiques
- **Linguistique** : Étude de la fréquence des lettres en arabe
- **Sécurité** : Tester la robustesse des chiffres classiques

## Dépannage

### L'application ne démarre pas

- Vérifiez que Python 3.7+ est installé
- Assurez-vous que Flask est installé : `pip install -r requirements.txt`
- Vérifiez que le port 5000 n'est pas occupé

### Les résultats ne semblent pas corrects

- Vérifiez que le texte chiffré est bien en arabe
- Augmentez la longueur du texte pour une meilleure analyse
- Vérifiez que le type d'attaque correspond au chiffre utilisé

### Erreur Unicode

- Assurez-vous que les fichiers sont encodés en UTF-8
- Les caractères arabes doivent être correctement affichés

## Technologies Utilisées

- **Backend** : Python 3 avec Flask
- **Frontend** : HTML5, CSS3, JavaScript
- **Cryptographie** : Implémentation maison de Caesar, Affine et Substitution
- **Analyse** : Test du Chi-carré et calcul de fréquences
