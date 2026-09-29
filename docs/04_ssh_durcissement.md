# Durcissement SSH

La configuration SSH conservée dans `config/sshd_config` sert de référence pour le durcissement.

Les points principaux vérifiés par l'audit sont :

- interdiction de la connexion directe du compte root ;
- désactivation de l'authentification par mot de passe ;
- utilisation de l'authentification par clé publique.

Ces mesures réduisent les possibilités d'accès distant non autorisé.