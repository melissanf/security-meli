from collections import Counter
from utils import clean_arabic_text, ARABIC_ALPHABET
import json

# Tableau de fréquence de référence pour l'arabe
# Basé sur des analyses linguistiques standard de la langue arabe moderne
DEFAULT_ARABIC_FREQUENCY = {
    "ا": 0.0861,  # ALEF
    "ل": 0.0761,  # LAM
    "م": 0.0735,  # MEEM
    "ن": 0.0671,  # NOON
    "ي": 0.0635,  # YA
    "ت": 0.0612,  # TA
    "ر": 0.0503,  # RA
    "ه": 0.0487,  # HA
    "ك": 0.0463,  # KAF
    "ب": 0.0425,  # BA
    "ع": 0.0382,  # AIN
    "و": 0.0362,  # WAW
    "ق": 0.0285,  # QAF
    "د": 0.0274,  # DAL
    "ح": 0.0265,  # HA JEEM
    "ش": 0.0227,  # SHEEN
    "خ": 0.0190,  # KHAA
    "س": 0.0183,  # SEEN
    "ف": 0.0182,  # FA
    "ج": 0.0176,  # JEEM
    "غ": 0.0160,  # GHAIN
    "ز": 0.0142,  # ZAAY
    "ظ": 0.0137,  # ZA
    "ث": 0.0088,  # THAA
    "ض": 0.0087,  # DAD
    "ص": 0.0086,  # SAD
    "ط": 0.0062,  # TAH
    "ذ": 0.0042,  # THAL
}


def calculate_frequency(text, return_counts=False):

    cleaned_text = clean_arabic_text(text)

    if not cleaned_text:
        return {}

    # Compter les occurrences
    counter = Counter(cleaned_text)
    total = sum(counter.values())

    # Calculer les fréquences
    frequencies = {char: count / total for char, count in counter.items()}

    # Ajouter les lettres absentes avec fréquence 0
    for letter in ARABIC_ALPHABET:
        if letter not in frequencies:
            frequencies[letter] = 0.0

    if return_counts:
        return {"frequencies": frequencies, "counts": counter, "total": total}

    return frequencies


def chi_squared_test(observed_freq, expected_freq):
 
    chi2 = 0.0

    for letter in ARABIC_ALPHABET:
        observed = observed_freq.get(letter, 0)
        expected = expected_freq.get(letter, 0)

        if expected > 0:
            chi2 += ((observed - expected) ** 2) / expected

    return chi2


def decrypt_caesar(ciphertext, shift):

    plaintext = []

    for char in ciphertext:
        if char in ARABIC_ALPHABET:
            # Trouver l'index de la lettre
            index = ARABIC_ALPHABET.index(char)
            # Appliquer le décalage inverse
            new_index = (index - shift) % len(ARABIC_ALPHABET)
            plaintext.append(ARABIC_ALPHABET[new_index])
        else:
            plaintext.append(char)

    return "".join(plaintext)


def attack_caesar_frequency(ciphertext, reference_freq=None):

    if reference_freq is None:
        reference_freq = DEFAULT_ARABIC_FREQUENCY

    results = []

    # Essayer tous les décalages possibles
    for shift in range(len(ARABIC_ALPHABET)):
        plaintext = decrypt_caesar(ciphertext, shift)
        plaintext_freq = calculate_frequency(plaintext)

        # Calculer le score chi-carré
        score = chi_squared_test(plaintext_freq, reference_freq)

        results.append({"shift": shift, "score": score, "plaintext": plaintext})

    # Trier par score (plus petit = meilleur)
    results.sort(key=lambda x: x["score"])

    return results


def create_substitution_key(source_freq, target_freq):

    # Trier les lettres par fréquence
    source_sorted = sorted(source_freq.items(), key=lambda x: x[1], reverse=True)
    target_sorted = sorted(target_freq.items(), key=lambda x: x[1], reverse=True)

    # Créer le mappage
    substitution_key = {}
    for i, (source_letter, _) in enumerate(source_sorted):
        if i < len(target_sorted):
            target_letter = target_sorted[i][0]
            substitution_key[source_letter] = target_letter

    return substitution_key


def apply_substitution(ciphertext, key):

    plaintext = []

    for char in ciphertext:
        if char in key:
            plaintext.append(key[char])
        else:
            plaintext.append(char)

    return "".join(plaintext)


def attack_substitution_frequency(ciphertext, reference_freq=None, num_candidates=5):

    if reference_freq is None:
        reference_freq = DEFAULT_ARABIC_FREQUENCY

    # Calculer les fréquences du texte chiffré
    ciphertext_freq = calculate_frequency(ciphertext)

    # Créer une clé de substitution basée sur les fréquences
    key = create_substitution_key(ciphertext_freq, reference_freq)

    # Déchiffrer
    plaintext = apply_substitution(ciphertext, key)
    plaintext_freq = calculate_frequency(plaintext)

    # Calculer le score chi-carré
    score = chi_squared_test(plaintext_freq, reference_freq)

    candidates = [
        {
            "key": key,
            "plaintext": plaintext,
            "score": score,
            "frequency_diff": plaintext_freq,
        }
    ]

    return candidates


def is_invertible(a, n=28):
    from math import gcd

    return gcd(a, n) == 1


def mod_inverse(a, m):
    """
    Calcule l'inverse modulaire de a modulo m using Extended Euclidean Algorithm.
    """

    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y

    g, x, _ = extended_gcd(a % m, m)

    if g != 1:
        return None
    else:
        return (x % m + m) % m


def decrypt_affine(ciphertext, a, b):
    """
    Déchiffre un texte chiffré par le chiffre affine.
    Formule: c(x) = ax + b (mod 28)
    Déchiffrement: x = a^(-1) * (y - b) (mod 28)
    """
    # Vérifier que a est inversible
    if not is_invertible(a):
        return None

    a_inv = mod_inverse(a, 28)
    plaintext = []

    for char in ciphertext:
        if char in ARABIC_ALPHABET:
            y = ARABIC_ALPHABET.index(char)
            x = (a_inv * (y - b)) % 28
            plaintext.append(ARABIC_ALPHABET[x])
        else:
            plaintext.append(char)

    return "".join(plaintext)


def get_valid_affine_keys():

    valid_keys = []

    for a in range(1, 28):
        if is_invertible(a):
            for b in range(28):
                valid_keys.append((a, b))

    return valid_keys


def attack_affine_frequency(ciphertext, reference_freq=None, num_candidates=10):

    if reference_freq is None:
        reference_freq = DEFAULT_ARABIC_FREQUENCY

    results = []
    valid_keys = get_valid_affine_keys()

    for a, b in valid_keys:
        plaintext = decrypt_affine(ciphertext, a, b)

        if plaintext is not None:
            plaintext_freq = calculate_frequency(plaintext)
            score = chi_squared_test(plaintext_freq, reference_freq)

            results.append(
                {"a": a, "b": b, "key": (a, b), "score": score, "plaintext": plaintext}
            )

    # Trier par score (plus petit = meilleur)
    results.sort(key=lambda x: x["score"])

    return results[:num_candidates]


def load_reference_frequency(filepath=None):

    if filepath is None:
        return DEFAULT_ARABIC_FREQUENCY

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement: {e}")
        return DEFAULT_ARABIC_FREQUENCY


def save_reference_frequency(frequency_table, filepath):

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(frequency_table, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")
