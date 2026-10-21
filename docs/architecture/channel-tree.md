# Channel tree — organisation des salons et des menus

> Source de vérité : comment chaque mod/jeu organise ses salons,
> où vivent les menus épinglés, et comment faire évoluer l'arbre.
> Le provisioning applique ces règles automatiquement (SDK panels).

## L'arbre de référence

```
GUILD
│
├── # 🗺️ général ………………… [menu: view:home]
├── # 💬 discussions …………… (libre, public)
│
├── 📂 🤖 bot
│   ├── # 📜 logs
│   ├── # 🛠️ admin …………… [menu: view:bot:admin]
│   └── # ⚖️ décisions ……… (libre, admin)
│
├── 📂 🎮 games
│   ├── # 🗺️ général ……… [menu: view:games:home]
│   └── # 🛠️ admin ………… [menu: view:games:admin]
│
├── 📂 ⚔️ games/aoe2
│   ├── # 🗺️ général ……… [menu: view:aoe2:home]
│   ├── # 📡 live …………… [dashboard: view:aoe2:live]
│   ├── # 🏛️ civilisations (forum, sync)
│   ├── # 🌍 maps …………… (forum, sync)
│   ├── # 🧱 map pools …… (forum, sync)
│   └── # 🛠️ admin ………… [menu: view:aoe2:admin]
│
├── 📂 🧩 mods
│   ├── # 🗺️ général ……… [menu: view:mods:home]
│   └── # 🛠️ admin ………… [menu: view:mods:admin]
│
├── 📂 🧩 mods/<mod>   (un dossier par mod, à venir)
│   ├── # 🗺️ général ……… [menu: view:<mod>:home]
│   ├── # 💬 discussions (libre, public)
│   ├── # <data-*> ………… (readonly, sync)
│   ├── # 🛠️ admin ………… [menu: view:<mod>:admin]
│   └── # ⚖️ décisions … (libre, admin)
│
└── 📂 🎮 games/<jeu>   (un dossier par jeu, à venir)
    ├── # 🗺️ général ……… [menu: view:<jeu>:home]
    ├── # 💬 discussions (libre, public)
    ├── # <forums> ………… (forums, sync)
    ├── # 🛠️ admin ………… [menu: view:<jeu>:admin]
    └── # ⚖️ décisions … (libre, admin)

Les dossiers de **regroupement** (games, mods, games/<jeu>) ne portent
que `général` et `admin` : les échanges et décisions vivent dans les
dossiers de **périmètre** (mods/<mod>, games/<jeu>), jamais dans les
dossiers de regroupement.
```

## Les règles structurelles

1. **Un périmètre = un dossier** (catégorie avec slash :
   `games/aoe2`, `mods/ladder`). Les salons du dossier ne répètent
   pas le scope (`# civs`, pas `# aoe2-civs`). Le scope racine
   (`root`) porte `général` et `discussions` **sans catégorie**.

2. **Le bot s'autorise toujours** : chaque salon provisionné porte
   un overwrite explicite pour le bot lui-même (view, send, manage,
   embed, attach) — sinon un `view_channel=False` pour @everyone
   verrouille le bot hors de son propre salon et toutes les surfaces
   (pins, syncs, dashboards) se dégradent en 403. Règle appliquée
   par le provisioning, jamais contournée à la main.

3. **Best-effort par salon, jamais par scope** : une opération
   Discord qui échoue sur un salon (403 sur un déplacement, quota,
   etc.) saute ce salon et poursuit le scope — les résolutions des
   autres salons se persistent quand même. Un échec de salon ne
   doit jamais vider tout un dossier (leçon du 2026-10-13 : un
   seul 403 sur `channel.edit(category=...)` laissait tout un scope
   non résolu, donc vide).

4. **La résolution se fait par id stocké, jamais par nom** :
   chaque salon provisionné est persisté sous
   `tree:<scope>:<clé>` (collection `channels`) ; les syncs, pins
   et dashboards résolvent par cet id. Le nom affiché n'est qu'un
   libellé traduit — aucun code ne résout par nom. Le
   provisioning est le **seul** propriétaire de la création : une
   résolution qui ne trouve pas d'id stocké ne crée rien (no-op).
5. **L'ordre canonique** dans chaque dossier :
   `général` → `discussions` (public, unique — jamais de doublon
   chat/discussions) → salons data (readonly, sync) → `admin` →
   `décisions`. `admin` et `décisions` ferment toujours le dossier.
6. **La catégorie `bot` est privée** (bot-admins). Les échanges
   publics vivent dans `# discussions` à la racine ; il n'y a pas
   de `bot/chat` ni de `admin-chat` à la racine.
7. **Traduction à la création** : chaque salon est nommé dans la
   langue de la guilde au provisioning (`général`, `discussions`,
   `décisions`, `civs`...). La clé interne (locale key) est stable ;
   seul le nom affiché est traduit ; le heal reconnaît les salons
   par leur clé, jamais par leur nom affiché.
8. **Les salons à menu sont readonly** (personne n'écrit dedans,
   admins compris). Les échanges vont dans `discussions` (public)
   ou `décisions` (admin du périmètre).
9. **Les ids de vues sont plats** : le scope d'un id de vue est le
   **dernier segment** du scope du dossier — `games/aoe2` donne
   `view:aoe2:home`, `view:aoe2:admin`, `view:aoe2:live` ;
   `mods/ladder` donnera `view:ladder:news`. Jamais de slash dans un
   id de vue : ils doivent rester quotables.

0. **Chaque menu est un `PanelSpec`** (SDK `kingdoms.discord.ui`) :
   `name` (registre `view:<guild-id>:<slug>`), `pinned_on`
   (channel + PinMode LATEST_ONLY|ALL|None), `autoheal`,
   `navigable` (False partout : figé, ephemerals), `permissions`
   (rôles requis), `build`. Le SDK provisionne, épingle, traduit ; la cicatrisation
   est à la demande (le bouton Synchroniser du périmètre), jamais
   en temps réel.

## Les menus : figés + navigation ephemeral

Un menu épinglé est **statique** : sa page ne change jamais. Ses
boutons ouvrent des **vues ephemeral** dans lesquelles on navigue
(retour, sous-vues, modals). Les surfaces publiques n'exposent
**jamais** de bouton d'action directement.

### Le bouton Admin unique

Sur un post public (forum map, pool, civ), un seul bouton visible :
**⚙️ Admin**. Il ouvre un ephemeral de gestion, vérifie la
permission au clic, et propose les boutons contextualisés **grisés
selon l'état** :

| Post | Ephemeral admin |
|---|---|
| Map | [Ajouter à un pool] [Supprimer] — supprimer grisé si la map est dans un pool actif ; ajouter grisé si aucun pool éditable |
| Map pool | [Éditer] [Publier] [Fermer] [Supprimer] — grisés selon le lifecycle (édition → Publier actif ; publiée → Fermer actif ; fermée → Supprimer actif, confirmation par le nom) |

**Règle à retenir** : les boutons dangereux ne sont jamais exposés
sur une surface publique ; ils vivent derrière le bouton Admin,
en ephemeral, vérifiés au clic, grisés par contexte.

## Comment ajouter un périmètre (jeu ou mod)

1. **Déclarer les salons** du dossier (clé stable + label i18n +
   kind: text/forum/category + access: public/admin/readonly).
2. **Déclarer les PanelSpecs** : `<scope>-home` (public, readonly,
   autoheal), `<scope>-admin` (bot-admins du périmètre),
   éventuellement `<scope>-live` ou data panels.
3. **Enregistrer** au boot : le SDK provisionne le dossier dans la
   langue de la guilde, épingle les menus, cicatrise.
4. **Les données** (posts de forum) restent gérées par les syncs
   périodiques — un post par entité, avec son bouton Admin.

### Exemple — mod ladder (à venir)

```
📁 mods/ladder
   ├── # général        ……………………………………… [menu: ladder-home]
   ├── # discussions    ……………………………………… (libre, public)
   ├── # classement      ……………………………………… (readonly, sync — top N)
   ├── # news            ……………………………………… (readonly, sync — résultats)
   ├── # matchs          ……………………………………… (readonly, sync — matchs joués)
   ├── # admin          ……………………………………… [menu: ladder-admin]
   └── # décisions      ……………………………………… (libre, admin)
```

### Exemple — mod kingdoms (à venir)

```
📁 mods/kingdoms
   ├── # général        ……………………………………… [menu: kingdoms-home]
   ├── # discussions    ……………………………………… (libre, public)
   ├── # carte          ……………………………………… (readonly, sync)
   ├── # admin          ……………………………………… [menu: kingdoms-admin]
   └── # décisions      ……………………………………… (libre, admin)
```

## Faire évoluer l'arbre

- **Ajouter un salon data** : clé + label + provisioning — le heal
  le recrée ; aucun code de menu à toucher s'il n'a pas de menu.
- **Ajouter un menu** : un PanelSpec de plus ; le SDK l'épingle au
  prochain passage.
- **Renommer** : la clé ne bouge jamais ; seul le label traduit
  change — le heal suit par clé.
- **Retirer** : retirer la déclaration ; le salon devient orphelin
  (à archiver manuellement — le SDK ne supprime jamais).
