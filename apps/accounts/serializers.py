from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, FarmProfile
from .validators import PhoneNumberValidator


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription des utilisateurs
    """
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(
        validators=[PhoneNumberValidator()],
        help_text="Format: +237XXXXXXXXX ou format international"
    )
    
    class Meta:
        model = User
        fields = (
            'phone_number', 'email', 'first_name', 'last_name',
            'business_name', 'account_type', 'language_preference',
            'password', 'password_confirm', 'activity_type',
            'region', 'department', 'district', 'neighborhood',
            'legal_status', 'promoter_name', 'age_group', 'intervention_zone'
        )
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs
    
    def create(self, validated_data):
        from django.core.exceptions import ValidationError as DjangoValidationError
        from django.db import IntegrityError
        
        validated_data.pop('password_confirm')
        
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except DjangoValidationError as e:
            # Transformer les erreurs de validation Django en erreurs DRF
            if hasattr(e, 'error_dict'):
                # Erreurs multiples
                for field, errors in e.error_dict.items():
                    error_messages = [str(error) for error in errors]
                    raise serializers.ValidationError({field: error_messages})
            else:
                # Erreur simple
                raise serializers.ValidationError(str(e))
        except IntegrityError as e:
            if 'phone_number' in str(e):
                raise serializers.ValidationError({
                    'phone_number': ['Un utilisateur avec ce numéro de téléphone existe déjà.']
                })
            else:
                raise serializers.ValidationError('Une erreur inattendue s\'est produite. Veuillez réessayer.')


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    """
    Serializer simple pour les réponses de registration/login.
    Évite les propriétés complexes qui peuvent causer des erreurs.
    """
    class Meta:
        model = User
        fields = (
            'id', 'phone_number', 'email', 'first_name', 'last_name',
            'business_name', 'account_type', 'is_verified', 'language_preference',
            'activity_type', 'region', 'department', 'district', 'neighborhood',
            'legal_status', 'promoter_name', 'age_group', 'intervention_zone',
            'date_joined', 'is_active'
        )
        read_only_fields = (
            'id', 'phone_number', 'is_verified', 'date_joined'
        )


class LoginSerializer(serializers.Serializer):
    """
    Serializer pour l'authentification MAVECAM.
    
    Supporte deux méthodes de connexion :
    1. login_name + password (nom d'entreprise ou "prénom nom")
    2. phone_number + password (numéro de téléphone)
    """
    login_name = serializers.CharField(
        required=False,
        help_text="Nom de l'entreprise OU nom complet de la personne (ex: 'Jean Farmer')"
    )
    phone_number = serializers.CharField(
        required=False,
        help_text="Numéro de téléphone (format: +237XXXXXXXXX)"
    )
    password = serializers.CharField(write_only=True, required=False)
    
    def validate(self, attrs):
        login_name = attrs.get('login_name')
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        
        # Vérifier qu'au moins un identifiant est fourni
        if not login_name and not phone_number:
            raise serializers.ValidationError(
                "Veuillez fournir soit le nom de connexion soit le numéro de téléphone."
            )
        
        if not password:
            raise serializers.ValidationError("Le mot de passe est requis.")
        
        # Tentative d'authentification avec les paramètres fournis
        user = authenticate(login_name=login_name, phone_number=phone_number, password=password)
        
        if not user:
            if phone_number:
                error_msg = (
                    "Numéro de téléphone ou mot de passe incorrect. "
                    "Vérifiez votre numéro de téléphone et votre mot de passe."
                )
            else:
                error_msg = (
                    "Nom de connexion ou mot de passe incorrect. "
                    "Utilisez le nom de votre entreprise ou votre nom complet."
                )
            raise serializers.ValidationError(error_msg)
        
        if not user.is_active:
            raise serializers.ValidationError("Compte désactivé.")
        
        attrs['user'] = user
        return attrs


class FarmProfileSerializer(serializers.ModelSerializer):
    """
    Serializer pour les profils de fermes MAVECAM.
    """
    is_certified = serializers.BooleanField(read_only=True)
    certification_status_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = FarmProfile
        fields = (
            'id', 'farm_name', 'certification_status', 
            'total_ponds', 'total_area_m2', 'water_source', 'main_species',
            'annual_production_kg', 'created_at', 'updated_at',
            'is_certified', 'certification_status_display'
        )
        read_only_fields = (
            'id', 'certification_status', 
            'created_at', 'updated_at', 'is_certified', 'certification_status_display'
        )
    
    def validate_farm_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Le nom de la ferme ne peut pas être vide.")
        return value.strip()


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer pour le profil utilisateur avec informations de ferme.
    """
    full_name = serializers.CharField(read_only=True)
    login_name = serializers.CharField(read_only=True)
    display_name = serializers.CharField(read_only=True)
    is_individual = serializers.BooleanField(read_only=True)
    is_company = serializers.BooleanField(read_only=True)
    
    # Informations de la ferme via la relation OneToOne
    farm_profile = FarmProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'phone_number', 'email', 'first_name', 'last_name',
            'business_name', 'account_type', 'is_verified', 'language_preference',
            'full_name', 'login_name', 'display_name', 'is_individual', 'is_company',
            'activity_type', 'region', 'department', 'district', 'neighborhood',
            'legal_status', 'promoter_name', 'age_group', 'intervention_zone',
            'farm_profile','date_joined', 'is_active'
        )
        read_only_fields = (
            'id', 'phone_number', 'is_verified', 'date_joined',
            'full_name', 'login_name', 'display_name', 'is_individual', 'is_company',
            'farm_profile'
        )