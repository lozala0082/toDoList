# Minimal Django settings required for password hashing
import os

# This key is only used for password hashing and isn't exposed to the web
SECRET_KEY = 'django-insecure-shared-password-hasher-key'

# Password validation
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Required for the import, but not used
INSTALLED_APPS = [] 