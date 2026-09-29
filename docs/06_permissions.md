# Vérification des permissions

L'audit recherche les répertoires world-writable dans `/var/www` et `/srv`.

Un répertoire accessible en écriture par tout le monde peut faciliter des modifications non autorisées. Le script signale donc les répertoires concernés afin de permettre leur correction.

La vérification est réalisée avec la commande `find` et les permissions `-002`.