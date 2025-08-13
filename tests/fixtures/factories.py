"""
Factories pour générer des données de test cohérentes.

Factory Boy permet de créer facilement des objets de test
avec des données réalistes pour simuler les vrais utilisateurs MAVECAM.
"""
import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """
    Factory pour créer des utilisateurs pisciculteurs de test.
    
    Génère des données réalistes pour simuler les vrais clients MAVECAM.
    """
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"pisciculteur_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@exemple.com")
    first_name = factory.Faker('first_name', locale='fr_FR')
    last_name = factory.Faker('last_name', locale='fr_FR')
    is_active = True
    is_staff = False
    
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """Définir un mot de passe par défaut pour les tests."""
        password = extracted or 'motdepasse_test123'
        self.set_password(password)
        if create:
            self.save()


class MavecamAdminFactory(UserFactory):
    """
    Factory pour créer des administrateurs MAVECAM.
    
    Simule les comptes du personnel MAVECAM qui gèrent les certifications.
    """
    username = factory.Sequence(lambda n: f"admin_mavecam_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@mavecam.com")
    first_name = "Admin"
    last_name = "MAVECAM"
    is_staff = True
    is_superuser = True


# Exemples d'usage dans les tests :
# 
# user = UserFactory()  # Utilisateur avec données aléatoires
# user = UserFactory(username='nom_specifique')  # Avec username spécifique
# users = UserFactory.create_batch(5)  # 5 utilisateurs d'un coup
# admin = MavecamAdminFactory()  # Administrateur MAVECAM