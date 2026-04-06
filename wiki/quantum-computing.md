# Quantum Computing

Quantum computing is a fundamentally different computation model that exploits quantum mechanical phenomena — superposition, entanglement, and interference — rather than classical binary logic. It sits between meaningful capability and hard limits: genuinely useful for specific problem classes, but far from the all-purpose threat to encryption that headlines suggest.

## Source

- `raw/00-clippings/A Primer on Quantum Computing.md`

## Why Quantum Computing Exists: The Classical Limit

Classical computers process information using bits — binary switches that are either 0 or 1, implemented as transistors. Progress came for decades from shrinking transistors, following **Moore's Law**: transistor count roughly doubled every 2 years.

The Moore's Law trajectory from 1960 to today:

| Era | Chip | Transistors |
|---|---|---|
| 1971 | Intel 4004 | ~2,300 |
| 1979 | Motorola 68000 | ~68,000 |
| 1995 | AMD K5 | ~4.3M |
| 2004 | IBM PowerPC | ~58M |
| 2023 | Apple M2 Ultra | ~134B |

The Apple M2 Ultra sits right on the 2× per 2 years exponential trend line at ~100B+ transistors. But this trend is now hitting physics: as transistors shrink toward atomic scales, **quantum tunneling** causes electrons to leak through insulating barriers even when a transistor is meant to be "off." Error rates rise. You can no longer reliably distinguish 0 from 1.

Quantum computing begins at this constraint — instead of fighting quantum effects at the atomic scale, it exploits them.

## Core Quantum Concepts

### Superposition

A classical bit is a coin lying flat — either heads (1) or tails (0). A **qubit** is like a coin spinning in the air: before it lands, it exists as a combination of both 0 and 1 simultaneously. The act of measurement collapses the superposition to a definite 0 or 1.

The three states:
- **1** — definite state (coin flat, heads)
- **Superposition** — 0 and 1 at the same time (coin spinning)
- **0** — definite state (coin flat, tails)

The superposition is not random indecision — it encodes probabilities over possible outcomes, which quantum operations can precisely manipulate.

### Entanglement

When two qubits are entangled, measuring one instantly determines the state of the other, regardless of physical distance. This creates correlated computation that has no classical equivalent.

### Interference

Quantum algorithms work by exploiting interference: quantum operations adjust the probabilities of different computational paths so that:
- **Incorrect paths cancel out** (destructive interference)
- **Correct paths become more likely** (constructive interference)

When the system is measured, the result is drawn from the adjusted probability distribution — most likely to be the correct answer.

**Critical clarification:** quantum computers do not check every possible answer simultaneously. They use superposition and interference so that wrong answers suppress each other and the right answer amplifies. This only works for problems with mathematical structure that allows this interference to be engineered.

## What Quantum Computers Can and Cannot Do

### Where Quantum Has Theoretical Advantage

| Problem Domain | Quantum Algorithm | Speedup Type |
|---|---|---|
| Integer factoring (RSA) | Shor's Algorithm | Exponential |
| Unstructured search | Grover's Algorithm | Quadratic |
| Quantum system simulation | Variational methods | Exponential |
| Certain optimization problems | QAOA | Problem-dependent |

### Where Quantum Has No Advantage

- General-purpose computation (web servers, databases, video rendering)
- Problems without exploitable mathematical structure
- Tasks requiring sequential logic with complex branching

## The Cryptographic Threat — Context

Modern RSA encryption relies on a mathematical asymmetry: multiplying two large primes is easy, but factoring the product back into those primes is computationally intractable for classical computers.

Shor's algorithm solves this efficiently on a quantum computer. **However**, breaking real RSA keys requires **thousands to tens of thousands of logical qubits** operating with very low error rates. No existing system is anywhere near this.

### Physical vs. Logical Qubits

The gap between physical and logical qubits is the central challenge:
- **Physical qubits** — actual hardware qubits; prone to errors (decoherence, gate errors)
- **Logical qubits** — error-corrected qubits constructed from many physical qubits; required for reliable computation
- Current ratio: roughly **1,000 physical qubits per logical qubit** for robust error correction

### Industry Qubit Trajectory (2024–2030+)

Estimated physical qubit counts (Upper/Lower range) vs. logical qubits (source: IBM, Google, Quantinuum):

| Year | Physical Qubits (Est.) | Logical Qubits (Est.) |
|---|---|---|
| 2024 | ~1,000 | ~2 |
| 2025 | ~2,000 | ~5 |
| 2026 | ~7,000 | ~15 |
| 2027 | ~12,000 | ~50 |
| 2028 | ~30,000 | ~100 |
| 2029 | ~100,000 | ~200 |
| 2030+ | ~1,000,000 | ~1,000 |

Breaking RSA-2048 requires ~4,000 logical qubits at low error rates. At the current trajectory, that's likely beyond this decade even under optimistic projections.

## Current Scaling Constraints

Quantum computing faces multiple hard constraints simultaneously:

1. **Hardware scaling is difficult and expensive** — qubits require extreme conditions (near absolute zero temperatures for superconducting qubits)
2. **Limited algorithm advantage** — only a small set of algorithms show clear quantum speedups over the best known classical algorithms
3. **Qubit fragility** — decoherence from environmental noise destroys quantum states; maintaining coherence long enough for deep circuits is the key engineering challenge
4. **Error correction overhead** — the physical-to-logical qubit ratio means any fault-tolerant system requires orders of magnitude more physical qubits than its logical qubit count

## Near-Term Applications

Before fault-tolerant quantum computing is achievable, **Noisy Intermediate-Scale Quantum (NISQ)** devices are being explored for:
- **Quantum chemistry simulation** — modeling molecular structures for drug discovery and materials science; quantum systems are naturally well-suited to simulate other quantum systems
- **Quantum machine learning** — experimental; benefits unclear on near-term hardware
- **Quantum optimization** — portfolio optimization, supply chain; quadratic speedup at best, practical advantage not yet demonstrated

The most credible near-term value is quantum chemistry, where even small quantum advantages could unlock breakthrough drug candidates or novel materials.

## Timeline Expectations

| Timeframe | What's Plausible |
|---|---|
| **Now – 2027** | NISQ experiments; quantum chemistry research; no cryptographic threat |
| **2028–2032** | Early fault-tolerant demonstrations; first practical chemistry applications |
| **2030s** | Potential first meaningful quantum advantage for specific scientific problems |
| **2040s+** | Cryptographically relevant attacks become technically feasible (with extensive hardware investment) |

## Post-Quantum Cryptography

Regardless of timeline, the cryptographic risk is motivating a transition to **post-quantum cryptography (PQC)** — algorithms designed to be hard for quantum computers to break:
- NIST standardized several PQC algorithms in 2024 (CRYSTALS-Kyber, CRYSTALS-Dilithium, SPHINCS+)
- Organizations with long-lived sensitive data should begin migration now — data harvested today could be decrypted later when quantum hardware matures ("harvest now, decrypt later")

## Related Topics

- [[gpu-cuda]] — classical GPU computing and the hardware limits that motivate quantum research
- [[probability-statistics]] — quantum mechanics is fundamentally probabilistic; superposition encodes probability amplitudes
- [[investing]] — major tech companies (IBM, Google, Microsoft, IonQ) and governments are investing heavily in quantum hardware
