# Contrôles de sécurité

Les contrôles automatisés du projet couvrent actuellement neuf points :

1. compte root verrouillé ;
2. `PermitRootLogin no` ;
3. `PasswordAuthentication no` ;
4. `PubkeyAuthentication yes` ;
5. UFW actif ;
6. port SSH autorisé dans UFW ;
7. absence de dossiers world-writable ;
8. absence de comptes avec mot de passe vide ;
9. système à jour.

Chaque contrôle produit un état OK ou FAIL dans le terminal.