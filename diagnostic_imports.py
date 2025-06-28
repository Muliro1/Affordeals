#!/usr/bin/env python3
"""
Diagnostic script to check for missing modules in the Django project.
"""

import sys
import importlib

# List of modules to check based on the settings.py file and discovered missing modules
modules_to_check = [
    'decouple',
    'debug_toolbar',
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap4',
    'djoser',
    'stripe',
    'rest_framework_simplejwt',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'PIL',  # Pillow
    'intasend',
    'rest_framework_nested',
]

print("Checking for missing modules...")
print("=" * 50)

missing_modules = []
available_modules = []

for module in modules_to_check:
    try:
        importlib.import_module(module)
        print(f"✓ {module} - Available")
        available_modules.append(module)
    except ImportError as e:
        print(f"✗ {module} - Missing: {e}")
        missing_modules.append(module)

print("\n" + "=" * 50)
print(f"Summary:")
print(f"Available modules: {len(available_modules)}")
print(f"Missing modules: {len(missing_modules)}")

if missing_modules:
    print(f"\nMissing modules that need to be installed:")
    for module in missing_modules:
        if module == 'decouple':
            print("  pip install python-decouple")
        elif module == 'debug_toolbar':
            print("  pip install django-debug-toolbar")
        elif module == 'rest_framework':
            print("  pip install djangorestframework")
        elif module == 'crispy_forms':
            print("  pip install django-crispy-forms")
        elif module == 'crispy_bootstrap4':
            print("  pip install crispy-bootstrap4")
        elif module == 'djoser':
            print("  pip install djoser")
        elif module == 'stripe':
            print("  pip install stripe")
        elif module == 'rest_framework_simplejwt':
            print("  pip install djangorestframework-simplejwt")
        elif module == 'PIL':
            print("  pip install Pillow")
        elif module == 'intasend':
            print("  pip install intasend-python")
        elif module == 'rest_framework_nested':
            print("  pip install drf-nested-routers")
        else:
            print(f"  pip install {module}")
else:
    print("All modules are available!")

print("\n" + "=" * 50) 