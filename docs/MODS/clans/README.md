# Clans mod

> Reference example generated via the [mod-intake
> skill](../../.agents/skills/mod-intake/SKILL.md) (botforge-services#267).
> Permanent mod: clan management with mutual-agreement admissions.

## Purpose

Chaque joueur peut créer son clan et le gérer : admissions à accord
mutuel, rôles internes (chef / officier / membre), tableau de bord des
clans, et forum par clan.

## Rules (shaped avec le game designer, 2026-10-20)

1. **Création libre** : n'importe qui crée un clan (nom + description)
   et en devient le chef.
2. **Admission à accord mutuel** : un joueur demande (les admins du clan
   — chef ou officiers — reçoivent la demande et valident) ou un admin
   de clan invite (le joueur accepte). L'accord des deux parties est
   requis dans tous les cas.
3. **Critère déclaré** : ELO RM 1v1 AoE2 > 1000 (`settings.enrollment`).
   Tant qu'aucune seam ELO core n'existe, le critère dégrade en motif
   « revue manuelle » — par design, jamais d'acceptation silencieuse.
4. **Un clan par joueur** à la fois.
5. **Rôles** : chef (gestion complète), officier (valide les
   admissions), membre.
6. **Départ** : un membre part librement ; le chef d'un clan peuplé doit
   d'abord transmettre (ou dissoudre en étant seul).

## Usage

```text
/clan                    — le dashboard : chaque clan, son nombre de membres
/clan (clic sur un clan) — la liste des membres du clan
```

Les surfaces : catégorie mod/clans avec un **forum par clan** (liste des
joueurs, bouton « Demander à rejoindre »).

## Architecture placement

| Concern | Location |
|---|---|
| Business logic (clans, memberships, admissions) | `modules/mods/clans/src/clans/service.py` |
| Inscriptions avec critères | core `EnrollmentService` (`settings.enrollment`) |
| Dashboard, commandes | entrypoint (`modules/mods/clans/src/clans/__init__.py`) |
| Déclaration | `modules/mods/clans/mod.yaml` |

## See also

- [RULES.md](RULES.md) for the mod rules
- [ENVIRONMENT.md](ENVIRONMENT.md) for the mod configuration
- [../GUIDES/mod-init.md](../../GUIDES/mod-init.md) — the canonical mod guide
