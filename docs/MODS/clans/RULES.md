# Clans mod — Rules

Règles du mod clans (shaped avec le game designer, 2026-10-20). Chaque
règle est automatisable et testée (`modules/mods/clans/tests/`).

## Règle 1 — Création libre

N'importe qui crée un clan (nom unique par guilde, insensible à la
casse) et en devient le chef. Un joueur sans clan seulement.

## Règle 2 — Admission à accord mutuel

- **Le joueur demande** : la candidature part vers les admins du clan
  (chef, officiers), qui l'acceptent ou la refusent avec raison.
- **L'admin invite** : le joueur reçoit la demande et l'accepte.
- Dans les deux sens, l'accord des deux parties est requis.

## Règle 3 — Critère d'élo

ELO RM 1v1 AoE2 > 1000, déclaré dans `settings.enrollment`
(`min_elo: 1000`). Dégrade en « revue manuelle » tant qu'aucune seam
ELO core n'existe — jamais d'acceptation silencieuse.

## Règle 4 — Un clan par joueur

Un joueur appartient à au plus un clan. Toute nouvelle candidature ou
création est refusée tant qu'il est membre (`leave` d'abord).

## Règle 5 — Rôles internes

`leader` (gestion complète) > `officer` (valide les admissions) >
`member`. Seuls le chef et les officiers approuvent les candidatures.

## Règle 6 — Départ

- membre/officier : départ libre ;
- chef : doit d'abord transmettre le clan, ou être seul (le clan est
  alors supprimé).
