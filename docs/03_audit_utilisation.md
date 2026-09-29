# Utilisation de l'audit

Le script principal se trouve dans `scripts/audit.py`.

## Exécution

```bash
sudo python3 scripts/audit.py
```

Le script affiche le résultat de chaque contrôle puis calcule un résultat global sous la forme `X/Y vérifications passées`.

Un code de sortie différent de zéro indique qu'au moins un contrôle n'est pas conforme.