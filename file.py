import os
from supabase import create_client, Client
import streamlit as st
from utilitaire import est_utilisateur_authentifie

# Récupérer les informations de Supabase à partir des variables d'environnement
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Créer un client Supabase
supabase: Client = create_client(url, key)


def afficher_page_inscription():
    st.title("Inscription")
    registration_form()


def registration_form():
    st.title("Formulaire d'Inscription")

    # Champ pour l'adresse e-mail
    email = st.text_input("Adresse e-mail")

    # Champ pour le mot de passe
    password = st.text_input("Mot de passe", type="password")

    # Bouton pour soumettre le formulaire
    if st.button("S'inscrire"):
        try:
            # Tenter de s'inscrire à Supabase
            res = supabase.auth.sign_up({
                "email": email,
                "password": password,
            })
            st.success("Inscription réussie!")

        except Exception as e:
            # Gérer les erreurs (par exemple, afficher un message d'erreur)
            st.error(f"Erreur lors de l'inscription : {e}")


def afficher_page_connexion():
    login()


def login():
    st.title("Connexion")

    # Champ pour l'adresse e-mail
    email = st.text_input("Adresse e-mail")

    # Champ pour le mot de passe
    password = st.text_input("Mot de passe", type="password")

    # Bouton pour se connecter
    if st.button("Se connecter"):
        try:
            # Authentification via Supabase
            data = supabase.auth.sign_in_with_password({"email": email, "password": password})

            # Accéder au jeton d'accès
            access_token = supabase.auth.get_session()

            # Stocker le jeton dans la session (ou tout autre moyen sécurisé)
            st.session_state.access_token = access_token
            est_utilisateur_authentifie(access_token)

            st.success("Connecté avec succès!")

        except Exception as e:
            st.error(f"Erreur de connexion : {e}")


def main():
    st.sidebar.title("Navigation")
    pages = ["Inscription", "Connexion"]
    choix_page = st.sidebar.radio("Sélectionnez une page", pages)

    if choix_page == "Inscription":
        afficher_page_inscription()
    elif choix_page == "Connexion":
        afficher_page_connexion()


if __name__ == "__main__":
    main()
