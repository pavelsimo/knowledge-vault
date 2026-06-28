---
title: "A Primer on Quantum Computing"
source: "https://x.com/chamath/status/2016972472659431710"
author:
  - "[[@chamath]]"
published: 2026-01-29
created: 2026-04-06
description: "The perception of quantum computing has oscillated between two extremes: it is either treated as distant science fiction or marketed as an a..."
tags:
  - "clippings"
---
The perception of quantum computing has oscillated between two extremes: it is either treated as distant science fiction or marketed as an all-purpose supercomputer posing an imminent threat to modern security and encryption.

The reality is less dramatic, more constrained, but yet still important to understand accurately.

## Quantum Computing 101

To understand the potential promise of quantum computing, we need to start with the familiar: the classical computer sitting in front of you.

Classical computers power virtually everything around us.

At their core, classical computers store and process information using bits. A bit takes one of two values: 1 (on) or 0 (off). Physical switches called transistors enforce that distinction. By coordinating billions of these switches, computers perform logic, store memory, and execute programs.

For a long time, progress came from shrinking those transistors. Smaller transistors mean more transistors per chip, increasing computing power, shrinking form factor, and lowering costs. That trend drove steady gains in capability and performance across all computing.

![[raw/00-clippings/images/9bf516f9d835a5d14cd9e633ecbfb652_MD5.jpg]]

That approach is now constrained by physics. As transistors shrink toward atomic scales, the insulating barriers that separate electrical states become extremely thin. Electrons can tunnel through these barriers, a phenomenon known as quantum tunneling, even when a transistor is meant to be “off.”

That leakage makes it harder to reliably distinguish 0s from 1s. Error rates rise.

**Quantum computing begins at this constraint.**

Instead of forcing classical computers to rely on ever-smaller transistors, quantum computers exploit quantum behavior that already exists at the atomic scale.

One of those behaviors is superposition. In classical computing, a bit is either 0 or 1. In quantum computing, a quantum bit, or qubit, can exist in a superposition of both states at the same time.

A simple analogy to picture this is a coin. A classical bit is like a coin lying flat on a table. It is either heads or tails. A qubit is closer to a coin spinning in the air. Before it lands, it is not one or the other. It exists as a combination of both possibilities.

![[raw/00-clippings/images/3c3684d2b2a42095bb63c3113c9849ea_MD5.jpg]]

When multiple qubits are combined, the system can exist in a superposition that includes many possible states.

Quantum operations then shift the likelihood of these states, increasing the probability of states that satisfy the problem’s structure while suppressing those that do not. When the system is measured, a single result is produced from the adjusted probabilities.

Quantum computers do not work by checking every possible answer faster than a classical computer. They work by using superposition and interference, so that incorrect paths cancel out and correct paths become more likely to appear when measured.

## What Can Quantum Computers Actually Do?

In theory, quantum computing offers advantages across a set of problem types. The most discussed areas include simulating quantum systems such as molecules and materials, solving structured optimization problems, and enabling new forms of secure communication.

However, among these possibilities, cryptography stands out as the most immediate and widely discussed implication.

Modern encryption protects data by relying on mathematical problems that are easy to perform in one direction but extremely hard to reverse. In RSA encryption, this asymmetry arises from multiplying two very large private prime numbers to produce a public number. While multiplication is easy, determining which two primes were used, given only the result, is extraordinarily difficult.

Quantum algorithms can exploit hidden mathematical structure in this arithmetic, revealing periodic relationships that classical computers cannot efficiently detect. This changes how the difficulty of factoring grows with size, turning a problem that scales poorly for classical computers into one that becomes solvable at a sufficient quantum scale.

Despite the theory, quantum computing is still far from breaking real-world encryption.

![[raw/00-clippings/images/85b2367eb51edd5d259774e54effcd68_MD5.jpg]]

Cryptographically relevant attacks require thousands to tens of thousands of logical qubits operating with very low error rates. No existing system is close.

Quantum computing faces multiple scaling constraints at once. Currently, hardware is difficult and expensive to scale, only a small set of algorithms show advantages, and qubits remain fragile and error-prone.

Quantum computing sits between meaningful capability and hard limits. Headlines tend to isolate breakthroughs or failures, without showing how hardware, algorithms, and timelines interact. **That gap between what is technically possible and what is practically achievable is where most confusion comes from.**

My research team created [this Deep Dive](https://chamath.substack.com/p/quantum-computing) from the ground up to explain how quantum computing actually works, place recent developments in context, and support informed discussion about its implications.

**In this Deep Dive, we cover:**

- What quantum computing is and how do they actually work
- Where quantum computers can outperform current systems, and where they never will
- Which industries are most exposed first
- What are the recent cutting-edge breakthroughs, and how to contextualize them
- How to think about timelines, including what is plausible this decade versus further out
- What governments and major technology firms are investing in and why

![[raw/00-clippings/images/79be24b9f5d5908c4dc474939d171387_MD5.png]]

Read the full deep dive here: [https://chamath.substack.com/p/quantum-computing](https://chamath.substack.com/p/quantum-computing)

Hope you enjoy reading and learning with me,

Chamath

PS: We also have a group chat for members to discuss the deep dives and ask me questions. See you there.