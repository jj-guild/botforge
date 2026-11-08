# Discord.py components guide

This guide documents the discord.py UI component concepts used throughout
BotForge: **embeds**, **Components V2** (`LayoutView`), Buttons, Selects,
Modals, **Persistent Views**, and **Dynamic Items**, with concrete usage
patterns and pitfalls.

BotForge uses **both** systems as complements (ADR-0009):

- **Embeds**: sober, lightweight, read-mostly messages (a result, a
  confirmation, a status update). First choice for simple output.
- **Components V2** (`LayoutView`): rich, structured, interactive UI —
  panels, multi-block layouts, side-by-side text + accessory, galleries.

A message is **either** embed-based or Components V2 — never both in the
same message (Discord rejects `content`/`embeds` on a V2 message, and the
`IS_COMPONENTS_V2` flag is permanent per message).

When in doubt, start with an embed; upgrade to V2 when the layout demands
more than a flat title/description/fields shape. See
[ADR-0009](../DECISIONS/009-discord-components-v2.md).

The goal is that all mods use consistent patterns, so interactions behave the
same everywhere and the game designer can iterate on interactions without
coding.

Implementation lives in `botforge-services` (see botforge-services#13); this
page is the reference for the patterns the implementation must follow.

## 1. Views (basic)

> **Components V2 (discord.py ≥ 2.6):** rich UI uses `discord.ui.LayoutView`
> — see section 1b and [ADR-0009](../DECISIONS/009-discord-components-v2.md).
> The `ui.View` patterns below (interaction checks, timeouts, custom IDs)
> carry over almost unchanged; the container class differs.
>
> **Embeds are not legacy** (ADR-0009): for sober, lightweight messages,
> send a `discord.Embed` (optionally with a `ui.View` for buttons). This
> section's `ui.View` patterns apply to both systems — only the rich-display
> part (V2 layouts, section 1b) is V2-specific.

A `discord.ui.View` is a container for buttons/selects attached to a message.
It dies after its timeout.

Good for: one-off confirmations within a single conversation.

Legacy `ui.View` example (kept for reference — do **not** start new code
this way):

```python
"""
Basic view: buttons attached to a message. Dies after timeout.
Good for: one-off confirmations within a single conversation.
"""
import discord


class ConfirmCancelView(discord.ui.View):
    """Simple confirm/cancel with a timeout."""

    def __init__(self, author_id: int, timeout: int = 60):
        super().__init__(timeout=timeout)
        self.author_id = author_id
        self.value: bool | None = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Only the command author can use these buttons."""
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "This button is not for you.", ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        await interaction.response.send_message("Confirmed!", ephemeral=True)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        await interaction.response.send_message("Cancelled.", ephemeral=True)
        self.stop()
```

Usage:

```python
view = ConfirmCancelView(author_id=interaction.user.id)
await interaction.response.send_message("Are you sure?", view=view, ephemeral=True)
await view.wait()
if view.value:
    # proceed
    ...
```

## 1b. Components V2 — LayoutView (for rich UI)

Discord's Components V2 replaces `content` + `embeds` + rows with a
composable component tree, for messages that need more than a flat embed.
discord.py exposes it since 2.6 (we pin `>=2.7.1`). The root is a
`discord.ui.LayoutView`; inside it:

| Component | Kind | Notes |
| --------- | ---- | ----- |
| `ui.Container` | layout | Rounded card with `accent_color`; children stack vertically |
| `ui.Section` | layout | 1–3 `TextDisplay` children + one accessory (`Thumbnail` or `Button`) |
| `ui.ActionRow` | layout | Up to 5 buttons or 1 select (as before) |
| `ui.Separator` | display | `visible=True/False`, `spacing` small/large |
| `ui.TextDisplay` | display | Markdown text; **4000 chars total per message** |
| `ui.Thumbnail` | display | Only as a `Section` accessory; images/GIF/WebP |
| `ui.MediaGallery` | display | Up to 10 media items |
| `ui.File` | display | Attachment surfaced explicitly |

### Hard incompatibilities to avoid

1. **Never mix systems in one message**: a Components V2 message cannot
   carry `content`, `embeds`, `stickers`, or `poll`. Passing both raises an
   API error. Text belongs in `TextDisplay`, cards in `Container`.
2. **The flag is permanent per message**: once sent with
   `IS_COMPONENTS_V2`, the flag cannot be removed; edits must send a full
   V2 layout again.
3. **Limits**: 40 components per message; 4000 shared characters across all
   `TextDisplay` (`LayoutView.content_length()` returns the total — assert
   it in tests); `Section` max 3 text children; `MediaGallery` max 10 items.
4. **Mentions in `TextDisplay` ping** even inside containers: gate
   mentionable content before rendering.
5. **Attachments are not previewed** by default: surface them via
   `MediaGallery` / `File` / `Thumbnail` (URL auto-embeds are off).
6. **Use `walk_children()`** to iterate/disable interactive items — the
   tree nests (Container → ActionRow → Button).

### Basic V2 confirmation card

```python
"""
Components V2 confirm/cancel card: Container + TextDisplays + ActionRow.
Replaces the embed-based confirm view.
"""
import discord


class ConfirmCancelLayout(discord.ui.LayoutView):
    """Confirm/cancel card with a timeout, restricted to one user."""

    def __init__(self, user_id: int, timeout: float = 60.0) -> None:
        super().__init__(timeout=timeout)
        self.user_id = user_id
        self.value: bool | None = None
        self.container = discord.ui.Container(
            discord.ui.TextDisplay("## Are you sure?"),
            discord.ui.TextDisplay("This action cannot be undone."),
            accent_color=discord.Color.blurple(),
        )
        self.action_row = discord.ui.ActionRow()
        self.container.add_item(self.action_row)
        self.add_item(self.container)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This prompt is not for you.", ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.value = True
        for child in self.walk_children():
            if isinstance(child, (discord.ui.Button, discord.ui.Select)):
                child.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.value = False
        for child in self.walk_children():
            if isinstance(child, (discord.ui.Button, discord.ui.Select)):
                child.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()


# usage — no content=, no embed=; everything is in the layout
view = ConfirmCancelLayout(user_id=interaction.user.id)
await interaction.response.send_message(view=view, ephemeral=True)
await view.wait()
if view.value:
    ...
```

## 2. Persistent Views (survive restarts)

Key rules:

1. `timeout=None`
2. Every component has an explicit, unique `custom_id`
3. The view must be added with `bot.add_view(...)` at startup
4. Callbacks must be able to recover state from `custom_id` or the database

```python
"""
Persistent layout: works even after bot restarts.
Good for: registration welcome panels, leaderboard refresh buttons.
Custom IDs follow the convention: mod:component:payload

`bot.add_view()` works identically for LayoutView as for legacy View.
"""
import discord


class RegistrationPanelLayout(discord.ui.LayoutView):
    """Welcome panel with a Register button that always works."""

    def __init__(self):
        super().__init__(timeout=None)  # MUST be None for persistence
        container = discord.ui.Container(accent_colour=discord.Colour.blurple())
        section = discord.ui.Section(
            discord.ui.TextDisplay("**Welcome to BotForge!**\nPress Register to create your kingdom."),
            accessory=discord.ui.Button(
                label="Register",
                style=discord.ButtonStyle.green,
                custom_id="registration:panel:register",  # Explicit custom_id
                emoji="✅",
            ),
        )
        section.accessory.callback = self.register  # type: ignore[assignment]
        container.add_item(section)
        self.add_item(container)

    async def register(self, interaction: discord.Interaction):
        # No in-memory state here: recover everything from DB/interaction
        await interaction.response.defer(ephemeral=True)
        # ... start registration workflow ...
        await interaction.followup.send(
            "Check your DMs to complete registration!", ephemeral=True
        )


# At bot startup (in setup_hook):
# bot.add_view(RegistrationPanelLayout())
```

> **Legacy note**: the same panel built with `discord.ui.View` + `@discord.ui.button`
> decorators works too, but all **new** UI must be LayoutView per
> [ADR-0009](../DECISIONS/009-discord-components-v2.md).

## 3. Dynamic Items (templated components)

`discord.ui.DynamicItem` allows a **single class** to serve components whose
`custom_id` embeds parameters. The template decorator declares the custom_id
shape:

```python
"""
Dynamic item: one class for many component instances.
Custom ID template: ladder:page:<int>
Example IDs: ladder:page:1, ladder:page:2, ladder:page:17
"""
import discord


class LadderPageButton(
    discord.ui.DynamicItem[discord.ui.Button],
    template=r"ladder:page:(?P<page>\d+)",
):
    """A pagination button that encodes the page number in its custom_id."""

    def __init__(self, page: int):
        super().__init__(
            discord.ui.Button(
                label=f"Page {page}",
                style=discord.ButtonStyle.grey,
                custom_id=f"ladder:page:{page}",
            )
        )
        self.page = page

    @classmethod
    def from_custom_id(cls, interaction, item, match):
        """Reconstruct the item from the custom_id regex match."""
        return cls(int(match["page"]))

    async def callback(self, interaction: discord.Interaction):
        # self.page was recovered from the custom_id
        await interaction.response.defer()
        # ... render page self.page of the leaderboard ...
```

Registration at startup:

```python
# in setup_hook:
bot.add_dynamic_items(LadderPageButton)
```

Why this matters for BotForge: the leaderboard channel can have dozens of page
buttons; a single `DynamicItem` class handles them all, including after
restarts.

### 3b. State reconstruction contract (binding)

A restart wipes every view instance in memory; Discord keeps the messages.
The bot must therefore **reconstruct every persistent view and its state
from the `custom_id` alone**. This contract is binding for every mod:

1. **`timeout=None` + explicit `custom_id`** on every persistent component —
   a view with a timeout or a generated custom_id dies with its process.
2. **All state lives in the `custom_id` payload or the database** — never in
   view/item attributes read by a callback. The only object a callback may
   trust after a restart is the interaction and what the `custom_id` carries.
3. **Registration at startup**: persistent views are re-registered with
   `bot.add_view(...)` and dynamic item classes with
   `bot.add_dynamic_items(...)` in `setup_hook` — a view the factory does not
   re-register is dead UI after the next deploy.
4. **Regex templates extend the convention**: a `DynamicItem` template must
   keep the `<mod>:<component>:<payload>` shape
   (e.g. `r"clans:join:(?P<clan_id>[0-9a-f]+)"`) so the component router and
   the runtime permission checks keep working; the payload group must accept
   the **100-character custom_id limit** (keep payloads compact — IDs, not
   text).
5. **Callbacks stay policy-blind**: rendering (`render_for`, #56) and
   authorization (`require_permission`, #55) are derived at interaction
   time from the `custom_id` and the declared policy — a reconstructed view
   never re-applies destination policies on its own.

A corollary for the archetypes (`PaginationView` & co.): views carrying
**ephemeral session state** (the current page in memory) are fine for
in-place navigation during one session, but must not be used for panels
meant to survive restarts; a persistent pager encodes the page in the
payload (`ladder:page:3`) and reconstructs it via `from_custom_id`.

## 4. Modals (text input forms)

```python
"""
Modal: popup form for text input.
Good for: report details, clan descriptions.
"""
import discord


class ReportModal(discord.ui.Modal, title="Submit a Report"):
    title_input = discord.ui.TextInput(
        label="Title",
        placeholder="Short summary",
        max_length=100,
        required=True,
    )
    description_input = discord.ui.TextInput(
        label="Description",
        style=discord.TextStyle.paragraph,
        placeholder="Describe the issue in detail",
        max_length=1000,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        # Access: self.title_input.value, self.description_input.value
        # ... create report, route to admin channel ...
        await interaction.followup.send("Report submitted. Thank you!", ephemeral=True)

    async def on_error(self, interaction, error):
        await interaction.response.send_message(
            "Something went wrong submitting your report.", ephemeral=True
        )
```

Launching a modal:

```python
@tree.command(name="report", description="Submit a report")
async def report_command(interaction: discord.Interaction):
    await interaction.response.send_modal(ReportModal())
```

## 5. Interaction lifecycle cheat sheet

| Method | When | Notes |
|--------|------|-------|
| `interaction.response.send_message(...)` | First response, < 3s | Public by default; `ephemeral=True` for private |
| `interaction.response.defer()` | First response when slow work follows | Must `followup.send()` later |
| `interaction.response.send_modal(...)` | First response, opens modal | Only valid first response for modals |
| `interaction.response.edit_message(...)` | Component click that edits the host message | For select menus, page turns |
| `interaction.followup.send(...)` | After defer, or second message | Multiple allowed |
| `interaction.edit_original_response(...)` | Edit the deferred first message | |

**Critical pitfall:** you have **3 seconds** to make the first response. Any DB
or external API call before that must use `defer()` first.

## 6. custom_id conventions (project-wide)

```
<mod>:<component>:<payload>
```

Examples:

- `registration:panel:register` — persistent panel button
- `registration:step:game` — select in registration workflow
- `ladder:page:3` — dynamic page button
- `clans:join:<clan_id>` — dynamic join button (payload = clan ID)

These conventions let the **DM listener and component router** dispatch any
interaction to the right mod handler with zero configuration.

> **Permissions**: which user may use which component — and what a DM vs a
> channel message may contain — is governed by the separate
> [Discord permissions & message delivery guide](discord-permissions.md)
> ([ADR-0016](../DECISIONS/016-discord-permissions-and-delivery.md)).

### Component routing

```mermaid
flowchart TD
    A["Component Interaction Received"] --> B{"Known custom_id prefix?"}
    B -->|"registration:"| C["Registration mod router"]
    B -->|"ladder:"| D["Ladder mod router"]
    B -->|"clans:"| E["Clans mod router"]
    C --> F{"Known custom_id?"}
    D --> F
    E --> F
    F -->|"Yes"| G["Call handler with recovered state"]
    F -->|"No"| H["Log warning, ignore"]
    G --> I["Respond within 3s or defer"]
```

## Pitfalls summary

- **Dual UI system** ([ADR-0009](../DECISIONS/009-discord-components-v2.md)):
  embeds for sober, lightweight messages; Components V2 (`LayoutView`) for
  rich UI. Never mix `content`/`embeds`/`stickers`/`poll` with a LayoutView
  message — the `IS_COMPONENTS_V2` flag is permanent per message; keep total
  TextDisplay length ≤ 4000 characters and ≤ 40 components; mentions inside
  TextDisplay ping the mentioned users.
- **`interaction_check`**: always restrict components to the intended user
  (e.g., the command author), with an ephemeral rejection message.
- **`timeout=None` is required** for persistence; any non-`None` timeout kills
  the view after inactivity, including after restarts.
- **Never store workflow state in memory** in persistent/dynamic components:
  recover it from the `custom_id` payload or the database
  (see [ADR-0002](../DECISIONS/002-workflow-engine.md)).
- **3-second rule**: defer before any slow work (DB, external API).
- **Modals have exactly one valid first response**:
  `response.send_modal(...)`.

## See also

- [../ARCHITECTURE.md](../ARCHITECTURE.md) — overall architecture and the UI
  layer placement (`discord/ui/`)
- [discord-permissions.md](discord-permissions.md) — permissions & message
  delivery guide (DM vs channel, runtime role checks, channel access)
- [../WORKFLOWS.md](../WORKFLOWS.md) — how UI components feed the workflow
  engine
- botforge-services#13 — UI components implementation
