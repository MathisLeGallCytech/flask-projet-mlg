#!/usr/bin/env python3
"""
Script pour exécuter les tests de l'application Flask
Usage:
    python run_tests.py                    # Tous les tests
    python run_tests.py --fast            # Tests rapides seulement
    python run_tests.py --performance     # Tests de performance seulement
    python run_tests.py --unit            # Tests unitaires seulement
    python run_tests.py --integration     # Tests d'intégration seulement
"""

import sys
import subprocess
import argparse
import time
import os

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    print(f"Commande: {command}")
    print("-" * 60)
    
    start_time = time.time()
    try:
        result = subprocess.run(command, shell=True, capture_output=False, text=True)
        end_time = time.time()
        
        print(f"\n⏱️  Temps d'exécution: {end_time - start_time:.2f} secondes")
        
        if result.returncode == 0:
            print("✅ Succès!")
            return True
        else:
            print(f"❌ Échec (code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Exécuter les tests de l\'application Flask')
    parser.add_argument('--fast', action='store_true', help='Exécuter seulement les tests rapides')
    parser.add_argument('--performance', action='store_true', help='Exécuter seulement les tests de performance')
    parser.add_argument('--unit', action='store_true', help='Exécuter seulement les tests unitaires')
    parser.add_argument('--integration', action='store_true', help='Exécuter seulement les tests d\'intégration')
    parser.add_argument('--coverage', action='store_true', help='Exécuter avec couverture de code')
    parser.add_argument('--verbose', '-v', action='store_true', help='Mode verbeux')
    
    args = parser.parse_args()
    
    print("🧪 Testeur d'Application Flask - Mathis Le Gall")
    print("=" * 60)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists('../app.py'):
        print("❌ Erreur: app.py non trouvé. Assurez-vous d'être dans le bon répertoire.")
        sys.exit(1)
    
    # Vérifier que test_app.py existe
    if not os.path.exists('test_app.py'):
        print("❌ Erreur: test_app.py non trouvé.")
        sys.exit(1)
    
    success = True
    
    # Construire la commande selon les arguments
    if args.fast:
        # Tests rapides (exclure les tests lents)
        command = "python -m pytest test_app.py -v -m 'not slow' --tb=short"
        success &= run_command(command, "Tests Rapides")
        
    elif args.performance:
        # Tests de performance seulement
        command = "python -m pytest test_app.py::PerformanceTestCase -v --tb=short"
        success &= run_command(command, "Tests de Performance")
        
    elif args.unit:
        # Tests unitaires seulement
        command = "python -m pytest test_app.py::FlaskAppTestCase -v --tb=short"
        success &= run_command(command, "Tests Unitaires")
        
    elif args.integration:
        # Tests d'intégration seulement
        command = "python -m pytest test_app.py::ErrorHandlingTestCase -v --tb=short"
        success &= run_command(command, "Tests d'Intégration")
        
    elif args.coverage:
        # Tests avec couverture de code
        print("\n📊 Installation de coverage si nécessaire...")
        subprocess.run("pip install coverage", shell=True, capture_output=True)
        
        command = "coverage run -m pytest test_app.py -v"
        success &= run_command(command, "Tests avec Couverture de Code")
        
        if success:
            print("\n📈 Génération du rapport de couverture...")
            subprocess.run("coverage report", shell=True)
            subprocess.run("coverage html", shell=True)
            print("📁 Rapport HTML généré dans tests/htmlcov/index.html")
        
    else:
        # Tous les tests
        command = "python test_app.py"
        success &= run_command(command, "Tous les Tests")
    
    # Résumé final
    print(f"\n{'='*60}")
    print("📋 RÉSUMÉ FINAL")
    print(f"{'='*60}")
    
    if success:
        print("🎉 Tous les tests ont réussi!")
        print("✅ L'application est prête pour la production")
        sys.exit(0)
    else:
        print("❌ Certains tests ont échoué")
        print("🔧 Veuillez corriger les erreurs avant de continuer")
        sys.exit(1)

if __name__ == '__main__':
    main()
