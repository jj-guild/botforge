# Pong — Mod test scenarios

Liste des scénarios qui valident/sécurisent l'implémentation. **Chaque
scénario a exactement un test automatisé**, écrit par l'agent dans
`modules/mods/pong/tests/test_scenarios.py` (botforge-services), joué
par la CI (`pytest tests modules/mods/*/tests/test_scenarios.py`), et
recoupé par la validation des docs (`validate_docs.py` échoue quand
un scénario documenté n'a pas de test).

## Format de scénario

```markdown
### SC-PONG-NNN — titre court

- **Given** …
- **When** …
- **Then** … (le critère d'acceptation que le test vérifie)

Implémenté par `test_SC_PONG_000_*` dans `test_scenarios.py`.
```

Règles :

- un id par scénario, `SC-PONG-NNN` ;
- scénario dans le même PR que la règle et le test qui l'implémentent ;
- le docstring du test porte l'id, pour que doc et code restent appariés.

## Scenarios

_À définir avec les règles (RULES.md) — chaque règle automatisable doit
avoir au moins un scénario._
