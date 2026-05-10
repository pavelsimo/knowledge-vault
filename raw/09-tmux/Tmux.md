## CLI Commands

| Command | Description |
|---------|-------------|
| `tmux` | Start a new session |
| `tmux new -s <name>` | Start a named session |
| `tmux ls` | List all sessions |
| `tmux a` | Attach to the most recent session |
| `tmux a -t <name>` | Attach to a specific session |
| `tmux kill-session -t <name>` | Kill a specific session |
| `tmux kill-server` | Kill all sessions |

## Hotkeys (prefix: `Ctrl+B`)

**Sessions**

| Key | Description |
|-----|-------------|
| `Ctrl+B d` | Detach from current session |
| `Ctrl+B w` | Interactive session + window browser |

**Windows**

| Key | Description |
|-----|-------------|
| `Ctrl+B c` | Create new window |
| `Ctrl+B n` | Next window |
| `Ctrl+B ,` | Rename current window |
| `Ctrl+B &` | Kill current window |

**Panes**

| Key | Description |
|-----|-------------|
| `Ctrl+B %` | Split vertically (side by side) |
| `Ctrl+B "` | Split horizontally (top/bottom) |
| `Ctrl+B <arrow>` | Move between panes |
| `Ctrl+B q <n>` | Jump to pane by index |
| `Ctrl+B Ctrl+<arrow>` | Resize pane (small steps) |
| `Ctrl+B Alt+<arrow>` | Resize pane (large steps) |
| `Ctrl+B Alt+1-5` | Apply preset layout |
| `Ctrl+B x` | Kill current pane |

**Copy Mode**

| Key | Description |
|-----|-------------|
| `Ctrl+B [` | Enter copy mode |
| `Space` | Start selection |
| `Enter` | Copy selection |
| `Ctrl+B ]` | Paste |

## Recommended ~/.tmux.conf

```
set -g mouse on          # enable mouse support
set -g mode-keys vi      # vi keys in copy mode
```
