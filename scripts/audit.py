#!/usr/bin/env python3
"""
Script d'audit de sécurité - Projet AEGIS / TechSud
Vérifie les points de durcissement définis suite à l'incident.
Usage : sudo python3 audit.py
"""

import subprocess
import re
import sys

OK = "\033[92m[OK]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"

results = []


def run(cmd):
    """Exécute une commande et retourne stdout, ou None en cas d'erreur."""
    try:
        output = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=5
        )
        return output.stdout.strip()
    except Exception:
        return None


def check(name, condition, detail=""):
    status = OK if condition else FAIL
    results.append((name, condition, detail))
    print(f"{status} {name}" + (f" — {detail}" if detail else ""))


def check_root_locked():
    out = run("sudo passwd -S root")
    ok = out is not None and " L " in out
    check("Compte root verrouillé", ok, out or "impossible de vérifier")


def check_sshd_config(option, expected_value):
    out = run(f"sudo sshd -T 2>/dev/null | grep -i '^{option.lower()} '")
    ok = out is not None and out.lower() == f"{option.lower()} {expected_value.lower()}"
    check(f"SSH: {option} = {expected_value}", ok, out or "directive non trouvée")


def check_ufw_active():
    out = run("sudo ufw status")
    ok = out is not None and out.lower().startswith("status: active")
    check("Pare-feu (ufw) actif", ok, out.splitlines()[0] if out else "non détecté")


def check_ssh_port_allowed():
    out = run("sudo ufw status")
    ok = out is not None and re.search(
        r"(22/tcp|OpenSSH).*ALLOW", out, re.IGNORECASE
    ) is not None
    check("Port SSH (22) autorisé dans ufw", ok)


def check_no_open_world_writable(paths=("/var/www", "/srv")):
    problems = []
    for path in paths:
        out = run(f"find {path} -type d -perm -002 2>/dev/null")
        if out:
            problems.extend(out.splitlines())

    ok = len(problems) == 0
    detail = f"{len(problems)} dossier(s) world-writable" if problems else "aucun"
    check("Pas de dossiers world-writable", ok, detail)


def check_updates():
    run("sudo apt update -qq")
    raw_out = run("apt list --upgradable 2>/dev/null")
    pkgs = [line for line in raw_out.splitlines() if "/" in line and "upgradable" in line] if raw_out else []

    ok = len(pkgs) == 0
    detail = f"{len(pkgs)} paquet(s) à mettre à jour" if pkgs else "à jour"
    check("Système à jour", ok, detail)


def check_no_empty_passwords():
    """Vérifie qu'aucun compte ne possède un mot de passe vide."""
    out = run("sudo awk -F: '($2==\"\"){print $1}' /etc/shadow")
    ok = out == "" or out is None
    check("Aucun compte avec mot de passe vide", ok, out or "aucun")


def main():
    print("=" * 55)
    print(" AUDIT DE SÉCURITÉ - TechSud / Projet AEGIS")
    print("=" * 55)

    check_root_locked()
    check_sshd_config("PermitRootLogin", "no")
    check_sshd_config("PasswordAuthentication", "no")
    check_sshd_config("PubkeyAuthentication", "yes")
    check_ufw_active()
    check_ssh_port_allowed()
    check_no_open_world_writable()
    check_no_empty_passwords()
    check_updates()

    print("=" * 55)
    total = len(results)
    passed = sum(1 for _, ok, _ in results if ok)
    print(f"Résultat global : {passed}/{total} vérifications passées")

    if passed < total:
        print("⚠️ Des points de durcissement restent à corriger.")
        sys.exit(1)

    print("✅ Tous les contrôles de sécurité sont conformes.")
    sys.exit(0)


if __name__ == "__main__":
    main()
