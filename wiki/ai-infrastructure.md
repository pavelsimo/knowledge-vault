AI infrastructure is shifting from bursty training systems toward always-on execution systems for agents. GPUs and accelerators remain central for model math, but agentic workloads also rely heavily on CPUs, memory, low-latency coordination, networking, tool execution, file handling, and continuous orchestration.

## Source

- [[raw/clippings/Why CPUs matter for agentic AI.md|raw/clippings/Why CPUs matter for agentic AI.md]]

## Training vs Agentic Workloads

Traditional AI infrastructure discussions center on accelerators because training and high-throughput inference are dominated by parallel matrix math. Agentic systems are different. They do not just generate one answer from one prompt; they loop through planning, tool calls, data retrieval, code execution, browser actions, file parsing, and verification.

| Workload | Dominant pattern | Hardware emphasis |
|---|---|---|
| Model training | Massive parallel math over huge batches | GPUs, TPUs, Trainium-class accelerators |
| Batch inference | High-throughput token generation | GPUs and optimized serving runtimes |
| Agentic AI | Continuous reasoning plus tool execution | CPUs, memory, networking, storage, and accelerators |

The raw source frames the agent as closer to a manager than a calculator: it breaks goals into steps, calls tools, processes files, coordinates state, and loops until a task is done.

## Why CPUs Matter

CPUs are native to many parts of an agent loop:

- Running shell commands
- Managing files
- Calling APIs
- Parsing documents
- Driving browsers or desktop automation
- Scheduling work
- Handling network I/O
- Coordinating many small tasks
- Running verification scripts

Even when token generation runs on an accelerator, the surrounding harness work often lands on CPU. This connects to [[agent-harness]]: the non-model infrastructure is not optional overhead; it is where much of the real system runs.

## Always-On Systems

Agentic AI is often continuous rather than batch-oriented. A thread automation, customer-support triage loop, or monitoring agent may wake up repeatedly, inspect state, call tools, update memory, and decide whether to act.

This changes infrastructure priorities:

| Requirement | Why it matters |
|---|---|
| Sustained performance | Agents run over time, not only in short bursts |
| Fast inter-core communication | Tool loops exchange small pieces of state frequently |
| Energy efficiency | Always-on systems make perf-per-watt economically important |
| Memory capacity | Multiple agents, worktrees, browser sessions, and test runners add up |
| Low latency | Agents often wait on many sequential tool calls |

## Practical Bottlenecks

In local agent workflows, the first bottleneck may not be model price. It may be machine resources:

- Several worktrees duplicate dependencies.
- Multiple TypeScript compilers or test runners compete for RAM.
- Browser automation consumes CPU and memory.
- Long-running tmux sessions need stable process management.
- Local vector stores, OCR, and document conversion add background load.

For agent swarms, this pairs directly with [[tmux]] and [[ai-agents]]: orchestration is constrained by the host machine's CPU, RAM, disk, and thermal behavior.

## Related Topics

- [[gpu-cuda]] - accelerator memory, CUDA kernels, and model-serving constraints
- [[local-models]] - local inference, hardware fit, quantization, and model routing
- [[distributed-training]] - large-scale training infrastructure
- [[agent-harness]] - orchestration and tool infrastructure around LLMs
- [[ai-agents]] - multi-agent coordination and local worktree execution
- [[mlops]] - deployment, monitoring, and production reliability
