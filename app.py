from flask import Flask, render_template, request, jsonify
from typing import Any, Dict
from crypto_logic import (
    calculate_frequency,
    attack_caesar_frequency,
    attack_affine_frequency,
    attack_substitution_frequency,
    DEFAULT_ARABIC_FREQUENCY,
)
from utils import get_text_info, clean_arabic_text

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze_text():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text.strip():
            return jsonify({"error": "Le texte ne peut pas être vide"}), 400

        freq_data: Any = calculate_frequency(text, return_counts=True)
        assert isinstance(freq_data, dict)
        frequencies: Dict = freq_data.get("frequencies", {})
        counts: Dict = freq_data.get("counts", {})
        total: int = freq_data.get("total", 0)

        text_info = get_text_info(text)

        freq_sorted = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

      
        top_letters = [
            {
                "letter": letter,
                "frequency": freq,
                "percentage": freq * 100,
                "count": counts.get(letter, 0),
            }
            for letter, freq in freq_sorted[:10]
        ]

        return jsonify(
            {
                "success": True,
                "frequencies": frequencies,
                "top_letters": top_letters,
                "text_info": text_info,
                "total_chars": total,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/attack", methods=["POST"])
def attack_cipher():
    try:
        data = request.get_json()
        ciphertext = data.get("ciphertext", "")
        attack_type = data.get("attack_type", "frequency")
        num_results = int(data.get("num_results", 5))

        if not ciphertext.strip():
            return jsonify({"error": "Le texte chiffré ne peut pas être vide"}), 400

        # Nettoyer le texte
        cleaned = clean_arabic_text(ciphertext)

        if not cleaned:
            return jsonify({"error": "Aucun caractère arabe trouvé"}), 400

        results = []

        if attack_type == "caesar":
            attack_results = attack_caesar_frequency(
                ciphertext, DEFAULT_ARABIC_FREQUENCY
            )
            results = [
                {
                    "rank": i + 1,
                    "key": f"shift={result['shift']}",
                    "shift": result["shift"],
                    "score": round(result["score"], 4),
                    "plaintext": result["plaintext"][:200],  # Limiter pour JSON
                }
                for i, result in enumerate(attack_results[:num_results])
            ]

        elif attack_type == "affine":
            attack_results = attack_affine_frequency(
                ciphertext, DEFAULT_ARABIC_FREQUENCY, num_results
            )
            results = [
                {
                    "rank": i + 1,
                    "key": f"a={result['a']}, b={result['b']}",
                    "a": result["a"],
                    "b": result["b"],
                    "score": round(result["score"], 4),
                    "plaintext": result["plaintext"][:200],
                }
                for i, result in enumerate(attack_results)
            ]

        elif attack_type == "substitution":
            attack_results = attack_substitution_frequency(
                ciphertext, DEFAULT_ARABIC_FREQUENCY, num_results
            )
            results = [
                {
                    "rank": i + 1,
                    "key": "Substitution par fréquence",
                    "score": round(result["score"], 4),
                    "plaintext": result["plaintext"][:200],
                }
                for i, result in enumerate(attack_results)
            ]

        elif attack_type == "frequency":
            freq_data: Any = calculate_frequency(ciphertext, return_counts=True)
            assert isinstance(freq_data, dict)
            frequencies: Dict = freq_data.get("frequencies", {})
            total: int = freq_data.get("total", 0)

            freq_sorted = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

            # Comparaison avec la référence
            comparison = []
            for letter, obs_freq in freq_sorted[:15]:
                ref_freq = DEFAULT_ARABIC_FREQUENCY.get(letter, 0)
                comparison.append(
                    {
                        "letter": letter,
                        "observed": round(obs_freq, 4),
                        "reference": round(ref_freq, 4),
                        "difference": round(abs(obs_freq - ref_freq), 4),
                    }
                )

            return jsonify(
                {
                    "success": True,
                    "attack_type": "frequency",
                    "frequencies": frequencies,
                    "comparison": comparison,
                    "total_chars": total,
                }
            )

        return jsonify(
            {
                "success": True,
                "attack_type": attack_type,
                "results": results,
                "num_results": len(results),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/example", methods=["GET"])
def get_example():
    """Retourne un exemple de texte arabe."""
    example = """أتاح الإنترنت للملايين من الناس إمكانية الاتصال ببعضهم البعض بسهولة
وسرعة، وأصبح من الممكن عرض المعلومات بطرق متعددة. وعمّ استخدام الشبكة
الجهات الحكومية والخاصة والفردية، بحيث أصبحت أداة لا غنى عنها في حياتنا.
لكن هذا الانتشار الواسع قد جعل حماية المعلومات والخصوصية أمراً ضرورياً."""
    return jsonify({"example": example})


@app.route("/api/reference-frequency", methods=["GET"])
def get_reference_frequency():
    freq_sorted = sorted(
        DEFAULT_ARABIC_FREQUENCY.items(), key=lambda x: x[1], reverse=True
    )

    frequency_data = [
        {"letter": letter, "frequency": freq, "percentage": freq * 100}
        for letter, freq in freq_sorted
    ]

    return jsonify({"reference_frequency": frequency_data})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint non trouvé"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Erreur serveur"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
