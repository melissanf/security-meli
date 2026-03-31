
import unicodedata
import re

# Alphabet arabe
ARABIC_ALPHABET = [
    'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر',
    'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف',
    'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي'
]

# Caractères spéciaux et variantes arabes à normaliser
ARABIC_DIACRITICS = [
    '\u064B',  # FATHATAN
    '\u064C',  # DAMMATAN
    '\u064D',  # KASRATAN
    '\u064E',  # FATHA
    '\u064F',  # DAMMA
    '\u0650',  # KASRA
    '\u0651',  # SHADDA
    '\u0652',  # SUKUN
    '\u0653',  # MADDAH
    '\u0654',  # HAMZA ABOVE
    '\u0655',  # HAMZA BELOW
    '\u0656',  # SUBSCRIPT ALEF
    '\u0657',  # INVERTED DAMMA
    '\u0658',  # MARK NOON GHUNNA
    '\u0670',  # SUPERSCRIPT ALEF
]

# Variantes des lettres selon leur position (à normaliser en forme de base)
ARABIC_LETTER_VARIANTS = {
    'ة': 'ه',  # TAA MARBUTA -> HA
    'ى': 'ا',  # ALEF MAKSURA -> ALEF
    'أ': 'ا',  # ALEF WITH HAMZA ABOVE -> ALEF
    'إ': 'ا',  # ALEF WITH HAMZA BELOW -> ALEF
    'آ': 'ا',  # ALEF WITH MADDA ABOVE -> ALEF
}


def remove_diacritics(text):

    # Supprimer tous les diacritiques
    for diacritic in ARABIC_DIACRITICS:
        text = text.replace(diacritic, '')
    
    # Normalisation Unicode (NFC)
    text = unicodedata.normalize('NFC', text)
    
    return text


def normalize_arabic_letters(text):

    for variant, base in ARABIC_LETTER_VARIANTS.items():
        text = text.replace(variant, base)
    
    return text


def clean_arabic_text(text):
    """
    Nettoie complètement un texte arabe :
    1. Supprime les diacritiques
    2. Normalise les variantes de lettres
    3. Supprime les espaces superflus
    4. Convertit en minuscules (s'il y a)
    5. Garde uniquement les lettres arabes """
    # Supprimer les diacritiques
    text = remove_diacritics(text)
    
    # Normaliser les variantes
    text = normalize_arabic_letters(text)
    
    # Supprimer les caractères non-arabes (garder uniquement les 28 lettres)
    # Les lettres arabes sont dans la plage Unicode U+0600 à U+06FF
    text = ''.join(char for char in text if char in ARABIC_ALPHABET)
    
    return text


def is_arabic_text(text):
    """
    Vérifie si le texte contient des caractères arabes.
    """
    arabic_pattern = re.compile(r'[\u0600-\u06FF]')
    return bool(arabic_pattern.search(text))


def get_text_info(text):
    """
    Retourne des informations sur le texte arabe.
    """
    cleaned = clean_arabic_text(text)
    return {
        'original_length': len(text),
        'cleaned_length': len(cleaned),
        'unique_letters': len(set(cleaned)),
        'is_arabic': is_arabic_text(text),
        'total_arabic_chars': len([c for c in text if c in ARABIC_ALPHABET or c in ARABIC_LETTER_VARIANTS])
    }
