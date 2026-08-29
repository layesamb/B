import json
import os
from datetime import datetime

CHEMIN_DONNEES = os.path.join("data", "planning.json")

JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


def structure_vide():
    return {
        "planning": {jour: [] for jour in JOURS},
        "historique": []
    }


def charger_donnees():
    if not os.path.exists(CHEMIN_DONNEES):
        os.makedirs("data", exist_ok=True)
        donnees = structure_vide()
        sauvegarder_donnees(donnees)
        return donnees

    try:
        with open(CHEMIN_DONNEES, "r", encoding="utf-8") as f:
            donnees = json.load(f)
            for jour in JOURS:
                if jour not in donnees.get("planning", {}):
                    donnees.setdefault("planning", {})[jour] = []
            donnees.setdefault("historique", [])
            return donnees
    except (json.JSONDecodeError, Exception):
        return structure_vide()


def sauvegarder_donnees(donnees):
    os.makedirs("data", exist_ok=True)
    with open(CHEMIN_DONNEES, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=2, ensure_ascii=False)