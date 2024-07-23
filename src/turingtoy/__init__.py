from typing import Dict, List, Optional, Tuple

import poetry_version

__version__ = poetry_version.extract(source_file=__file__)

def run_turing_machine(
    machine: Dict,
    input_: str,
    steps: Optional[int] = None,
) -> Tuple[str, List[Dict[str, str]], bool]:
    vide = machine["blank"]  # Caractère représentant la case vide
    etat = machine["start state"]  # État initial de la machine
    etats_finaux = machine["final states"]  # Liste des états finaux
    table = machine["table"]  # Table de transition

    ruban = list(input_)  # Convertir l'entrée en liste de caractères
    position_tete = 0  # Position initiale de la tête de lecture
    ruban = [vide] + ruban + [vide]  # Ajouter des caractères vides au début et à la fin
    position_tete += 1  # Déplacer la tête après le premier vide

    historique = []  # Liste pour stocker l'historique des transitions

    def enregistrer_historique(etat, lecture, position_tete, ruban, transition):
        # Enregistre l'état actuel, la lecture, la position de la tête, le ruban et la transition
        transition_str = str(transition) if isinstance(transition, dict) else transition
        historique.append({
            "state": etat,
            "reading": lecture,
            "position": str(position_tete),
            "memory": ''.join(ruban),
            "transition": transition_str,
        })

    compte_etapes = 0  # Compteur pour les étapes

    while steps is None or compte_etapes < steps:
        if etat in etats_finaux:  # Vérifier si l'état actuel est un état final
            return ''.join(ruban).strip(vide), historique, True

        lecture = ruban[position_tete]  # Lire le caractère sous la tête de lecture

        if etat not in table or lecture not in table[etat]:  # Si aucune transition n'est définie
            return ''.join(ruban).strip(vide), historique, False

        transition = table[etat][lecture]  # Obtenir la transition

        if isinstance(transition, str):  # Si la transition est une chaîne (R ou L)
            if transition == "R":
                position_tete += 1
            elif transition == "L":
                position_tete -= 1
            enregistrer_historique(etat, lecture, position_tete, ruban, transition)
        else:  # Sinon, la transition est un dictionnaire
            if "write" in transition:
                ruban[position_tete] = transition["write"]  # Écrire sur le ruban
            if "R" in transition:
                etat = transition["R"]
                position_tete += 1
            elif "L" in transition:
                etat = transition["L"]
                position_tete -= 1
            enregistrer_historique(etat, lecture, position_tete, ruban, transition)

        if position_tete < 0:  # Si la tête dépasse le bord gauche du ruban
            ruban.insert(0, vide)
            position_tete = 0
        elif position_tete >= len(ruban):  # Si la tête dépasse le bord droit du ruban
            ruban.append(vide)

        compte_etapes += 1  # Incrémenter le compteur d'étapes

    return ''.join(ruban).strip(vide), historique, etat in etats_finaux  # Retourner le résultat final
