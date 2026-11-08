# ADR-0001: Multi-platform architecture

**Status:** Accepted
**Date:** 2026-09-18
**Reference:** botforge#2, botforge#6

## Context

We need to support Discord now, and want to keep the door open to Twitch
and potentially other platforms in the future. Building platform-specific code for
each would lead to:

- Code duplication
- Inconsistent behavior across platforms
- High maintenance overhead
- Difficulty adding new platforms

## Decision

Implement an **abstract `IPlatform` interface** that defines platform-agnostic
operations (messaging, channel management, roles, DMs). Each platform
(Discord, Twitch, ...) has its own implementation of this interface, plus
adapters that convert platform objects to core models (`IMessage`, `IChannel`,
`IUser`) and back.

Mods and workflows are expressed only against the core interfaces; they never
import platform-specific code.

## Alternatives Considered

1. **Direct platform-specific code:** simple but not scalable, leads to
   duplication
2. **Adapter pattern only:** more complex, less clear abstraction
3. **Plugin system:** overkill for our needs, adds unnecessary complexity

## Consequences

### Positive

- Easy to add new platforms (implement `IPlatform`)
- Consistent API across all platforms
- Core logic remains platform-agnostic
- Easier testing (can mock `IPlatform`, see botforge-services#2 MockDiscord)
- Better separation of concerns

### Negative

- Slight performance overhead (abstraction layer)
- More initial setup work
- Need to maintain multiple implementations

## Diagram

```mermaid
classDiagram
    class IPlatform {
        <<interface>>
        +send_message(message, channel)
        +edit_message(message_id, content)
        +create_channel(name, category)
        +get_user(user_id)
        +get_channel(channel_id)
        +add_reaction(message, emoji)
    }

    class DiscordPlatform {
        +send_message(message, channel)
        +edit_message(message_id, content)
        +create_channel(name, category)
        +get_user(user_id)
        +get_channel(channel_id)
        +add_reaction(message, emoji)
    }

    class TwitchPlatform {
        +send_message(message, channel)
        +edit_message(message_id, content)
        +create_channel(name, category)
        +get_user(user_id)
        +get_channel(channel_id)
        +add_reaction(message, emoji)
    }


    IPlatform <|.. DiscordPlatform
    IPlatform <|.. TwitchPlatform

    class Core {
        -platform: IPlatform
        +execute_workflow()
    }

    Core --> IPlatform : uses
```

## References

- [ARCHITECTURE.md](../ARCHITECTURE.md) — core interfaces
- botforge-services#3 (IPlatform), botforge-services#11 (DiscordPlatform)
