Team communication works best when real-time chat is reserved for narrow, time-sensitive work and most important decisions move into slower, contextual, reviewable channels. The 37signals group-chat clipping argues that persistent chat becomes harmful when it turns into the default operating system for work: it fragments attention, creates implied consensus, weakens written thought, and makes people chase a moving stream instead of doing deep work.

## Source

- [[raw/clippings/Group Chat The Best Way to Totally Stress Out Your Team.md|raw/clippings/Group Chat The Best Way to Totally Stress Out Your Team.md]]

## Chat Is Useful, But Narrow

The source does not reject chat outright. It identifies a few strong uses:

| Good chat use | Why it works |
|---|---|
| Quick back-and-forth | A small group can resolve a tactical question fast |
| Red alerts | Immediate operational problems need immediate attention |
| Social belonging | Remote teams need lightweight presence and informal texture |
| Fun | Small moments of culture fit chat well |

The problem starts when chat becomes the default place for decisions, announcements, project memory, and all-day coordination.

## Failure Modes

Persistent group chat pushes teams toward "now" as the default. That creates several predictable failure modes:

| Failure mode | Effect |
|---|---|
| Mental fatigue | Many channels become many informal all-day meetings |
| ASAP culture | Everything feels urgent because the medium rewards immediacy |
| FOMO | People watch channels to avoid missing decisions or context |
| One-line thinking | Complex ideas get split into interrupted fragments |
| Implied consensus | Decisions appear settled because they were mentioned in chat |
| Poor record keeping | Later readers cannot tell where the full decision lives |
| Context switching | Unread indicators repeatedly pull attention away from deep work |

For [[ai-coding]] and [[codex-workflows]], this matters because high-quality technical work needs uninterrupted blocks, durable context, and reviewable decisions.

## Better Defaults

The source's main operating rule is:

```text
Real-time sometimes, asynchronous most of the time.
```

Practical defaults:

- Use chat for quick, small, temporary coordination.
- Move important discussions to written posts, tickets, docs, or comments attached to the work item.
- Give people time to respond when the decision matters.
- Summarize event streams instead of piping every event into a channel.
- Stop expecting people to keep chat open all day.
- Treat presence indicators as weak signals, not availability contracts.
- When a chat grows too long, ask someone to write it up.

## Design Principle

Communication tools shape behavior. If the default path is a fast stream, the organization gets faster fragments. If the default path is contextual writing attached to work, the organization gets better memory and more careful decisions.

This is a systems design issue as much as a culture issue: the shape of the tool changes throughput, latency, attention cost, and auditability.

## Related Topics

- [[ai-coding]] - deep technical work needs context, tests, and uninterrupted verification loops
- [[codex-workflows]] - durable threads and artifacts preserve decisions better than ephemeral streams
- [[desktop-ai-automation]] - scheduled briefings and summaries can reduce notification churn
- [[agent-harness]] - explicit state and memory are safer than assuming chat history is reliable context
- [[system-design]] - communication channels have tradeoffs similar to distributed systems
