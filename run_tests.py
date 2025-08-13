#!/usr/bin/env python
"""
Script pour exécuter les tests MAVECAM AquaCare
"""
import os
import sys
import subprocess

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mavecam_api.settings')
    
    # Setup Django avant d'importer quoi que ce soit
    import django
    django.setup()
    
    # Lancer pytest avec les bonnes options
    cmd = [
        'pytest',
        'tests/',
        '-v',
        '--tb=short',
        '--disable-warnings',
        '--cov=apps',
        '--cov-report=term-missing',
        '--cov-report=html:htmlcov'
    ]
    
    print("Lancement des tests MAVECAM...")
    result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
    return result.returncode

if __name__ == '__main__':
    sys.exit(main())