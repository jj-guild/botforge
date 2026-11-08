# ADR-0011: Structural typing with `typing.Protocol` for the core interfaces

- **Status**: Accepted
- **Date**: 2026-09-20
- **Deciders**: developer
- **Reference**: botforge-services#3

## Context

The platform-agnostic contracts (`IPlatform`, `IMessage`, `IChannel`, `IUser`,
`IWorkflow`) were defined as abstract base classes (`abc.ABC` +
`@abstractmethod`). The platform layer implements them through the adapter
pattern (`botforge-services#8`): discord.py objects are converted into core
models. With nominal typing, every adapter model must explicitly inherit from
an `I*` class, coupling the adapter module to the interface module for purely
mechanical reasons.

Python 3.12 is the project baseline and mypy runs in strict mode, so
structural typing is fully supported by the toolchain.

## Decision

The core interfaces in `botforge-services`
(`src/botforge/core/interfaces/platform.py`) are defined as
`typing.Protocol` classes, decorated with `@runtime_checkable`:

- **Implementations satisfy the contracts structurally**: no inheritance
  required. `DiscordPlatform`, adapters and test fakes are plain classes
  whose shape is verified by mypy.
- **`@runtime_checkable`** enables `isinstance` checks for lightweight
  runtime verification (member presence only, not signatures).
- Signature conformance is enforced by **mypy strict**, not at runtime.

`DiscordPlatform` and the adapters therefore no longer inherit from `I*`
classes.

## Alternatives Considered

1. **Keep `abc.ABC`**: explicit inheritance gives fail-fast instantiation
   errors and a visible inheritance graph, but forces adapters to import and
   subclass the contracts for no structural benefit.
2. **Protocols without `@runtime_checkable`**: simplest option, but loses the
   ability for tests and defensive code to assert conformance at runtime.
3. **Plain duck typing without contracts**: no mypy verification at all,
   incompatible with the strict-typing rule.

## Consequences

### Positive

- Adapters and `DiscordPlatform` are decoupled from the interface module
  (import direction inverts: only the core's consumers reference contracts)
- Test doubles (MockDiscord, `botforge-services#2`) are trivial to write
- The adapter pattern gains its natural typing model
- Contracts remain fully checked by mypy strict

### Negative

- Missing methods are no longer caught at instantiation time; they surface
  as mypy errors instead (mitigated by strict CI)
- `@runtime_checkable` `isinstance` only checks member presence, not
  signatures — a partial implementation can pass a runtime check
- The inheritance graph no longer shows which classes implement which
  contract; the pydoc and this ADR carry that knowledge

## References

- [ADR-0001](001-multi-platform-architecture.md) — multi-platform
  architecture (`IPlatform`)
- [../ARCHITECTURE.md](../ARCHITECTURE.md) — generic core, `interfaces/`
- `botforge-services#3` — IPlatform implementation
