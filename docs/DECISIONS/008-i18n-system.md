# ADR-0008: i18n system

**Status:** Accepted
**Date:** 2026-09-18
**Reference:** botforge#6

## Context

We need to support:

- English (default)
- French (required)
- Potentially other languages in the future

For all:

- Bot messages
- Command descriptions
- Error messages
- UI components (buttons, modals)

## Decision

Implement **YAML-based i18n** with:

- Language files in `botforge-services/config/locales/`
- Structure: `locales/en.yaml`, `locales/fr.yaml`
- Nested keys for organization
- Fallback to English for missing translations
- Runtime language switching per guild

## Alternatives Considered

1. **JSON files:** similar, but YAML is more readable
2. **Database storage:** more flexible but slower
3. **Gettext:** standard but complex for our use case

## Consequences

### Positive

- Easy to add new languages
- Human-readable format
- Version controlled
- Easy to translate

### Negative

- Need to handle missing keys
- Reload files on change (or restart)
- Validation needed

## References

- [ARCHITECTURE.md](../ARCHITECTURE.md) — configuration layer
- botforge-services#17 (i18n)
