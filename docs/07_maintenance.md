# Maintenance et mises à jour

Avant de vérifier les paquets disponibles, le script actualise le cache APT avec :

```bash
sudo apt update -qq
```

Il recherche ensuite les paquets pouvant être mis à jour. L'objectif est de détecter une VM dont les correctifs ne sont pas appliqués.

Cette étape complète les contrôles SSH, UFW et permissions.