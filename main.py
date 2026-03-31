"""
main.py - Point d'entrée de l'application
Lancez ce fichier pour démarrer l'application Flask de cryptanalyse arabe
"""

import sys
from app import app


def main():
    print(" Démarrage de l'analyseur de fréquence arabe...")
    print(" L'application est accessible à: http://127.0.0.1:5000")
    print(" Appuyez sur Ctrl+C pour arrêter le serveur\n")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
    except Exception as e:
        print(f"Erreur lors du lancement: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✋ Application fermée par l'utilisateur")
        sys.exit(0)
