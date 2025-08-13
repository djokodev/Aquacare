"""
Configuration globale pour les tests MAVECAM.

Ce fichier contient des fixtures réutilisables et la configuration
partagée entre tous les tests du projet.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def api_client():
    """
    Client API pour les tests d'intégration.
    Permet de simuler les requêtes HTTP depuis l'app mobile.
    """
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def user_factory():
    """
    Factory pour créer des utilisateurs de test.
    Simule les pisciculteurs qui s'inscrivent via l'app mobile.
    """
    def create_user(**kwargs):
        defaults = {
            'phone_number': '+237690123456',
            'email': 'test@mavecam.com',
            'first_name': 'Jean',
            'last_name': 'Farmer',
            'account_type': 'individual',
            'age_group': '26_35',
            'password': 'password123'
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)
    return create_user


@pytest.fixture
@pytest.mark.django_db
def authenticated_user(user_factory):
    """
    Utilisateur authentifié pour les tests nécessitant une connexion.
    """
    return user_factory()


@pytest.fixture
@pytest.mark.django_db
def auth_client(api_client, authenticated_user):
    """
    Client API avec utilisateur connecté (tokens JWT).
    Simule un pisciculteur connecté dans l'app mobile.
    """
    refresh = RefreshToken.for_user(authenticated_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
@pytest.mark.django_db
def mavecam_admin(user_factory):
    """
    Utilisateur administrateur MAVECAM pour les tests nécessitant
    des privilèges élevés (ex: gestion des certifications).
    """
    return user_factory(
        phone_number='+237699000001',
        email='admin@mavecam.com',
        first_name='Admin',
        last_name='MAVECAM',
        is_staff=True,
        is_superuser=True
    )