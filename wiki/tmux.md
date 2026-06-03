Tmux is a terminal multiplexer that keeps shell sessions alive, splits a terminal into windows and panes, and makes long-running command-line work easier to monitor and steer. In this vault it is especially relevant for coding agents, remote development, build/test loops, and multi-session orchestration.

## Sources

- [[raw/09-tmux/Tmux.md|raw/09-tmux/Tmux.md]]
- [[raw/00-clippings/Tmux Cheat Sheet & Quick Reference  Session, window, pane and more.md|raw/00-clippings/Tmux Cheat Sheet & Quick Reference  Session, window, pane and more.md]]

## Session Commands

| Command | Description |
|---|---|
| `tmux` | Start a new session |
| `tmux new -s <name>` | Start a named session |
| `tmux new-session -A -s <name>` | Attach to an existing named session or create it |
| `tmux ls` | List sessions |
| `tmux a` | Attach to the most recent session |
| `tmux a -t <name>` | Attach to a specific session |
| `tmux kill-session -t <name>` | Kill one session |
| `tmux kill-server` | Kill all sessions |

The high-value pattern is named sessions. A named session turns a task into something you can leave, reattach to, and inspect later.

## Prefix Hotkeys

The default prefix is `Ctrl+B`.

| Area | Key | Description |
|---|---|---|
| Sessions | `Ctrl+B d` | Detach from current session |
| Sessions | `Ctrl+B w` | Interactive session and window browser |
| Windows | `Ctrl+B c` | Create a new window |
| Windows | `Ctrl+B n` | Move to next window |
| Windows | `Ctrl+B p` | Move to previous window |
| Windows | `Ctrl+B ,` | Rename current window |
| Windows | `Ctrl+B &` | Kill current window |
| Panes | `Ctrl+B %` | Split vertically, side by side |
| Panes | `Ctrl+B "` | Split horizontally, top and bottom |
| Panes | `Ctrl+B <arrow>` | Move between panes |
| Panes | `Ctrl+B q <n>` | Jump to pane by index |
| Panes | `Ctrl+B x` | Kill current pane |
| Copy mode | `Ctrl+B [` | Enter copy mode |
| Copy mode | `Space` | Start selection |
| Copy mode | `Enter` | Copy selection |
| Copy mode | `Ctrl+B ]` | Paste |

## Agent Workflows

Tmux is useful for agent workflows because it gives every long-running process a stable terminal target. A common shape:

```bash
tmux new-session -d -s codex-feature -c /path/to/worktree "codex"
tmux send-keys -t codex-feature "Focus on the API layer first." Enter
tmux attach -t codex-feature
```

This pairs with [[ai-agents]] and [[agent-harness]] because a tmux session can be the execution container for an isolated coding agent. It also makes mid-task steering possible without killing the process.

## Recommended Configuration

The local raw note recommends:

```tmux
set -g mouse on
set -g mode-keys vi
```

Mouse support helps with pane selection and scrolling. Vi mode makes copy-mode navigation line up with common terminal muscle memory.

## Related Topics

- [[ai-agents]] - multi-agent execution and worktree isolation
- [[agent-harness]] - orchestration, state, tools, and verification around LLM agents
- [[codex-workflows]] - long-running Codex threads, goals, and automation surfaces
- [[ai-coding]] - disciplined AI-assisted development loops
- [[system-design]] - operational reliability patterns for long-running workflows
