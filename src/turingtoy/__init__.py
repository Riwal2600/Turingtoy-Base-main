from typing import Dict, List, Optional, Tuple

import poetry_version

__version__ = poetry_version.extract(source_file=__file__)

def run_turing_machine(
    machine: Dict,
    input_: str,
    steps: Optional[int] = None,
) -> Tuple[str, List[Dict[str, str]], bool]:
    vide = machine["blank"]
    etat = machine["start state"]
    etats_finaux = machine["final states"]
    table = machine["table"]

    ruban = list(input_)
    position_tete = 0
    ruban = [vide] + ruban + [vide]
    position_tete += 1

    historique = []

    def enregistrer_historique(etat, lecture, position_tete, ruban, transition):
        transition_str = str(transition) if isinstance(transition, dict) else transition
        historique.append({
            "state": etat,
            "reading": lecture,
            "position": str(position_tete),
            "memory": ''.join(ruban),
            "transition": transition_str,
        })

    compte_etapes = 0

    while steps is None or compte_etapes < steps:
        if etat in etats_finaux:
            return ''.join(ruban).strip(vide), historique, True

        lecture = ruban[position_tete]

        if etat not in table or lecture not in table[etat]:
            return ''.join(ruban).strip(vide), historique, False

        transition = table[etat][lecture]

        if isinstance(transition, str):
            if transition == "R":
                position_tete += 1
            elif transition == "L":
                position_tete -= 1
            enregistrer_historique(etat, lecture, position_tete, ruban, transition)
        else:
            if "write" in transition:
                ruban[position_tete] = transition["write"]
            if "R" in transition:
                etat = transition["R"]
                position_tete += 1
            elif "L" in transition:
                etat = transition["L"]
                position_tete -= 1
            enregistrer_historique(etat, lecture, position_tete, ruban, transition)

        if position_tete < 0:
            ruban.insert(0, vide)
            position_tete = 0
        elif position_tete >= len(ruban):
            ruban.append(vide)

        compte_etapes += 1

    return ''.join(ruban).strip(vide), historique, etat in etats_finaux

