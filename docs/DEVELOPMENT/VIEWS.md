# VIEWS — la carte des menus et des panels

> **Source de vérité.** Ce document décrit **chaque view** du bot : son
> id, son type, où elle vit, et ses boutons. Le code reflète exactement
> cette liste (`views_declared.py` dans kingdoms-services) : changer
> l'organisation = changer ce doc **et** ce fichier dans le même PR.
> Les agents lisent ce doc avant d'ajouter, déplacer ou retirer une view.

## Les deux types de views

| Type | Rôle | Contenu |
| ---- | ---- | ------- |
| **menu** | Naviguer | Des boutons uniquement — chaque bouton ouvre une autre view. Pas de données, pas d'actions. |
| **panel** | Informer / agir | Des données (listes, stats), des actions, du contenu live. |

Règles communes :

- chaque view porte un **id** (`menu:games:aoe2`, `panel:profile`) rendu
  en **footer** — c'est l'ancre de tous les retours utilisateurs ;
- un bouton **admin** porte l'emoji 🔒 et le style le plus discret ;
- un bouton **sync** (salons & rôles) porte l'emoji 🔄 ;
- les labels passent par le catalogue i18n (clé `ui.views.<id sans :>.title`) ;
- **limites** : 20 maps / map pool · 20 map pools actifs / guilde ·
  20 jeux · 20 mods.

## La carte (aujourd'hui : 1 jeu — aoe2, 0 mod)

```text
menu:home ──┬─> panel:profile
            ├─> menu:games:home ──┬─> menu:games:aoe2 ──┬─> panel:game:aoe2:live
            │                    │                     ├─> panel:game:aoe2:players
            │                    │                     └─> menu:game:aoe2:admin
            │                    └─> menu:games:admin ──> menu:game:aoe2:admin
            ├─> menu:mods:home ──┬─> (menu:mod:ladder      — désactivé)
            │                   ├─> (menu:mod:tournament — désactivé)
            │                   ├─> (menu:mod:kingdom     — désactivé)
            │                   └─> menu:mods:admin
            └─> menu:admin ──┬─> panel:status
                             ├─> menu:games:admin
                             ├─> menu:mods:admin
                             └─ [🔄 sync]
```

## Les views, une par une

### `menu:home` — pin dans `root/général`
Le point de départ.
- → `panel:profile` (👤)
- → `menu:games:home` (🎮)
- → `menu:mods:home` (🧩)
- → `menu:admin` (🔒)

### `panel:profile`
Le profil du joueur (comptes liés, renommage). *Ok avec l'existant.*

### `menu:admin` — pin dans `bot/admin`
- → `panel:status` (📊)
- → `menu:games:admin` (🔒)
- → `menu:mods:admin` (🔒)
- 🔄 sync salons & rôles

### `panel:status` — DM au boot
Le statut du déploiement (version, uptime, services). *Ok avec l'existant.*

### `menu:games:home` — pin dans `games/général`
La liste des jeux disponibles — **un bouton par jeu, label long**
(le nom du jeu, pas son game_key), + admin.
- → `menu:games:aoe2` (⚔️ Age of Empires II)
- → `menu:games:admin` (🔒)

### `menu:games:admin` — pin dans `games/admin`
- → `menu:game:aoe2:admin` (🔒 par jeu)
- 🔄 sync salons & rôles

### `menu:games:aoe2` — pin dans `games/aoe2/général`
Le nom du jeu en titre, puis :
- texte : **les salons** (contenu, restrictions, forums)
- texte : **les rôles** (usage)
- → `panel:game:aoe2:live` (📡)
- → `panel:game:aoe2:players` (👥)
- → `menu:game:aoe2:admin` (🔒)

### `menu:game:aoe2:admin` — pin dans `games/aoe2/admin`
Mêmes sections salons/rôles que le menu du jeu, puis :
- ⭐ Ajouter une map
- 🧱 Créer un map pool
- 🔄 sync salons & rôles

### `panel:game:aoe2:live` — pin dans `games/aoe2/live`
Le dashboard live. *Ok avec l'existant.*

### `panel:game:aoe2:players`
Les joueurs enregistrés **pour ce jeu** — une ligne chacun, pas de
nom de guilde. Générique : `panel:game:<key>:players`.

### `menu:mods:home` — pin dans `mods/general`
La liste des mods (vide aujourd'hui) — **un bouton par mod, label
long**, + admin. Les exemples déclarés sont désactivés :
- (menu:mod:ladder — désactivé)
- (menu:mod:tournament — désactivé)
- (menu:mod:kingdom — désactivé)
- → `menu:mods:admin` (🔒)

### `menu:mods:admin` — pin dans `mods/admin`
- (menu:mod:ladder:admin — désactivé, 🔒)
- (menu:mod:tournament:admin — désactivé, 🔒)
- (menu:mod:kingdom:admin — désactivé, 🔒)
- 🔄 sync salons & rôles

## Ajouter ou déplacer une view (le mode d'emploi)

1. **Déclarer** : `views_declared.py` — une `ViewDecl` (id, type,
   scope du pin, boutons avec leurs cibles). Un menu ne déclare que
   des boutons qui pointent vers des views déclarées (ou sync) ;
2. **Documenter** : ajouter la view ici, dans la carte et sa fiche ;
3. **Câbler** : si la view ouvre un handler, `wire_view("<id>",
   handler)` dans `_wire_declared_views` (factory) — sinon rien ;
3. **Traduire** : `ui.views.<id>.title` / `.description` dans
   `fr.yaml` **et** `en.yaml` ;
4. **Tester** : le registre se valide (`validate_registry`) — une
   cible non déclarée, un bouton de menu sans cible/sync/label sont
   des drifts que les tests rejettent.

Un nouveau jeu suit le même chemin : `menu:games:<key>`,
`menu:game:<key>:admin`, ses panels — le builder déclaratif rend le
menu automatiquement depuis la déclaration.
