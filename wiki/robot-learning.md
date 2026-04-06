# Robot Learning

Robot learning covers how machines acquire skills through experience, demonstrations, or interaction with the environment. It bridges computer vision, reinforcement learning, and imitation learning to build robots that can perceive, plan, and act in the physical world.

## Source

- [[raw/03-stanford-cs231n/Stanford CS231N.md|raw/03-stanford-cs231n/Stanford CS231N.md]]
- [[raw/00-clippings/(824) Stanford CS231N Deep Learning for Computer Vision  Spring 2025  Lecture 17 Robot Learning - YouTube.md|raw/00-clippings/(824) Stanford CS231N Deep Learning for Computer Vision  Spring 2025  Lecture 17 Robot Learning - YouTube.md]]
- [[raw/00-clippings/Should Robot Generalists Get Off Their High Horse.md|raw/00-clippings/Should Robot Generalists Get Off Their High Horse.md]]
- [[raw/00-clippings/The Physical AI Deployment Gap.md|raw/00-clippings/The Physical AI Deployment Gap.md]]

## Problem Formulation

Goal: learn a **policy** π(s) → a that maps observations/states to actions to maximize cumulative reward.

- **State (s_t):** what the robot perceives (camera images, joint positions, tactile sensors)
- **Action (a_t):** motor commands (joint torques, velocities, gripper open/close)
- **Reward (r_t):** scalar feedback signal indicating success
- **Goal (g):** task specification (text, image of target, goal state)

## Reinforcement Learning (RL)

RL learns by trial and error — the robot interacts with the environment and adjusts behavior to maximize cumulative reward.

**Why RL is different from supervised learning:**
- **Stochasticity:** same action can lead to different outcomes (box rotates unpredictably)
- **Delayed rewards:** in chess or Go, you may not know if you're winning until many moves later
- **Non-differentiable world:** you can't backpropagate through the physics of the real world
- **Non-stationary:** what the agent experiences changes as it improves

### Deep RL Successes

| Task | Approach | Paper |
|------|---------|-------|
| Atari games | DQN (Deep Q-Network) | [Playing Atari with Deep RL](https://arxiv.org/pdf/1312.5602) |
| Go | AlphaGo | [Mastering Go with deep neural networks](https://storage.googleapis.com/deepmind-media/alphago/AlphaGoNaturePaper.pdf) |
| Chess/Shogi | AlphaZero | [Mastering Chess and Shogi by Self-Play](https://arxiv.org/pdf/1712.01815) |
| StarCraft II | AlphaStar | [Grandmaster level in StarCraft II](https://storage.googleapis.com/deepmind-media/research/alphastar/AlphaStar_unformatted.pdf) |
| Dota 2 | OpenAI Five | [OpenAI Five defeats Dota 2 world champions](https://openai.com/index/openai-five-defeats-dota-2-world-champions/) |
| Quadruped locomotion | Model-free RL | [Learning Quadrupedal Locomotion over Challenging Terrain](https://arxiv.org/pdf/2010.11251) |
| Rubik's Cube | Dexterous RL | [Solving Rubik's Cube with a Robot Hand](https://arxiv.org/pdf/1910.07113) |

**Key observation:** locomotion (walking, running, jumping) is nearly a solved problem using RL.

### Model-Free RL Problems

- Requires enormous amounts of real-world interaction data
- Robots wear out from millions of trial runs
- Safety: trial and error in the real world is dangerous

### Model-Based Planning

Instead of learning behavior directly from reward, learn a **world model** that predicts future states given actions:

```
(state sₜ, action aₜ) → predicted next state sₜ₊₁
```

Then plan ahead by simulating sequences of actions in the learned model.

**Pixel dynamics:** predict the next video frame from the current image + action.
Paper: [Deep Visual Foresight for Planning Robot Motion](https://arxiv.org/pdf/1610.00696)

**Keypoint dynamics:** instead of predicting full pixel frames, track a few important keypoints on objects.
Paper: [Keypoints into the Future](https://arxiv.org/pdf/2009.05085)

**Particle dynamics:** represent objects (especially deformable materials like piles of rice) as collections of "particles" at adaptive resolution.
Paper: [Dynamic-Resolution Model Learning for Object Pile Manipulation](https://arxiv.org/pdf/2306.16700)

## Imitation Learning

Learn from human demonstrations rather than reward signals.

### Behavior Cloning (BC)

The simplest approach: treat demonstrations as supervised learning.

```
(observation, expert_action) pairs → train a policy with supervised loss
```

**Problem (distribution shift):** if the robot makes a small mistake and drifts from the expert trajectory, it has no data for that situation and will fail catastrophically — like memorizing test answers without understanding the subject.

### Inverse Reinforcement Learning (IRL)

Rather than copying behavior directly, infer the **reward function** the expert was optimizing:

1. Observe expert demonstrations
2. Infer what reward function best explains the behavior
3. Train a policy to maximize that inferred reward

**IRL vs Imitation Learning:**

| | Imitation Learning | IRL |
|--|--|--|
| Learns | Policy (state → action) | Reward function |
| Uses demos to | Directly copy behavior | Understand intent |
| Generalization | Limited | Often better |

### Implicit Behavioral Cloning (IBC)

Instead of explicitly predicting the robot's action, learn an **energy function** E(o, a) that scores action-observation pairs:
- At inference: pick the action with the lowest energy score
- Captures multimodal action distributions (many correct ways to do a task)

Paper: [Implicit Behavioral Cloning](https://arxiv.org/pdf/2109.00137)

### Diffusion Policy

Apply diffusion model technology to robot action generation:
- The robot starts with noisy (random) actions
- Iteratively denoises toward the optimal action trajectory
- Handles multimodal action distributions naturally (unlike explicit policies that average)
- Currently one of the most powerful robot learning approaches

Paper: [Diffusion Policy: Visuomotor Policy Learning via Action Diffusion](https://arxiv.org/abs/2303.04137)

## Robot Foundation Models

Foundation models for robotics — analogous to ChatGPT for text, but for physical action:

- **Input:** camera images + goal specification (text or image)
- **Output:** robot joint commands / end-effector trajectories
- **Trained on:** large-scale robot interaction datasets across many robots and tasks

### Evolution of Robotic Foundation Models

| Model | Key innovation |
|-------|---------------|
| [RT-1](https://arxiv.org/pdf/2212.06817) | Robotics Transformer for real-world control at scale |
| [RT-2](https://arxiv.org/pdf/2307.15818) | Vision-Language-Action: web knowledge → robot control |
| [RT-X](https://arxiv.org/pdf/2310.08864) | Cross-embodiment training across many robot types |
| [OpenVLA](https://arxiv.org/pdf/2406.09246) | Open-source VLA model |
| [π₀ (Pi Zero)](https://arxiv.org/pdf/2410.24164) | Flow-based VLA from Physical Intelligence |
| [GR00T N1](https://arxiv.org/pdf/2503.14734) | NVIDIA open foundation model for humanoid robots |
| [Gemini Robotics](https://arxiv.org/pdf/2503.20020) | Bringing Gemini AI into physical world |

## Robot Perception

Robots perceive the world through multiple sensors:
- **Cameras** (RGB, depth/RGB-D)
- **LiDAR** (point clouds for 3D mapping)
- **Tactile sensors** (force and contact)
- **Proprioception** (joint angles, velocities)

**Robot vision is:**
- **Embodied:** the robot has a body and experiences the world directly
- **Active:** the robot chooses what to perceive and from where
- **Situated:** perception is grounded in the "here and now" of the physical environment

## Foundation World Models

The next frontier: instead of just "what to do," teach robots "how the world works":

```
(current state sₜ, action aₜ) → predicted next state sₜ₊₁
```

This lets the robot **simulate actions in its mind** before executing them physically — avoiding mistakes without real-world trial and error.

**The three pillars of physical intelligence:**
1. **Action-conditioned interaction data:** videos of robots doing things + outcomes
2. **Foundation policy (the doer):** (observation, goal) → action
3. **Foundation world model (the predictor):** (state, action) → next state

Reference: [1X World Model](https://www.youtube.com/watch?v=7tjVALT35Pw)

## Generalist vs. Specialist Robotics

### The Generalist Dream and Its Limits

The dominant assumption in frontier robotics research is that if you gather enough multimodal data, train on enough tasks, and scale the model far enough, generality will emerge. A Stanford and Google DeepMind study running 1,600+ real-world robot trials across 14 axes of generalization found that state-of-the-art generalist manipulation policies still struggle with small perturbations — a changed camera angle, a rephrased instruction, or a shift in object properties. The gap between research results and real-world deployability remains large.

**Research vs. commercial evaluation criteria differ fundamentally:**

| Research | Commercial |
|---|---|
| Can the system handle more scenarios? | Does it work consistently? |
| Can it adapt across environments? | What is the throughput and uptime? |
| Can it learn broad capabilities from diverse data? | Does it integrate into an existing workflow? |
| Generalization benchmark scores | Does it save money? |

"You never think about uptime when you're doing research, but if the robot is going down even once a week, your customers are going to give you a lot of grief and maybe walk away." — Ken Goldberg, UC Berkeley

### Good Old-Fashioned Engineering (GOFE)

There is a "purist" attitude in academic robotics that treats any hand-coded component — inverse kinematics, low-pass filters, known workspace boundaries, geometry constraints — as "cheating." The aspiration is to learn everything end-to-end.

**GOFE** (Good Old-Fashioned Engineering, rhymes with "Sophie") is the countervailing principle: use whatever tools are available to make the system work reliably in the real world.

If you know the height of a table, add a rule so the gripper never dips below that threshold and crashes. If you know the boundaries of the workspace, encode them. If there is a mathematical function that reliably solves a subproblem, use it.

"GOFE is viewed as a crutch, something you're encouraged to stay away from at all costs. But GOFE can be extremely helpful to get robots to work reliably in real environments so they can collect data." — Ken Goldberg

Many of the best robotics companies are already doing exactly this — quietly inserting GOFE, constraining environments, adding fallback logic, layering software, and shaping the workflow around the model. They just don't always talk about it.

### The Specialist Path to Production

Near-term commercial opportunities are in **specialist systems**: robots that need bounded generality inside a specific workflow. A robot may need to sort packages, or complete one assembly step. That is often enough to create real value.

The production path:
1. Start with a **specialized use case** using GOFE to get the first system working reliably
2. **Get into production** — this determines whether second and third deployments get easier
3. Collect a large **specialized dataset** around real functionality, not generality
4. Use that dataset to learn **adjacent skills** and expand outward

"Most successes in robotics require 99.99% uptime. Most people underestimate how hard that bar is to hit." — Saman Farid, CEO of Formic

The path to generality runs through specialist systems, not around them. GOFE is not a barrier to generality — it is the scaffold that makes it achievable.

## The Physical AI Deployment Gap

The gap between what robotics research demonstrates and what operates at scale in production environments has never been wider. VLA models follow natural language instructions to manipulate objects they have never seen. Simulation-trained policies transfer to real hardware with increasing reliability. Scaling laws appear to hold for robot actions. And yet the vast majority of robots in production environments remain narrowly preprogrammed, executing fixed routines in carefully controlled conditions.

### Research Frontier (What's Demonstrated)

**Vision-Language-Action (VLA) models** are the most significant architectural shift in recent years. They take vision-language models pretrained on internet-scale data, fine-tune them to output robot actions, and leverage the semantic understanding learned from web data for robotic control. Key milestones:

| Model | Key Contribution |
|---|---|
| RT-2 (Google) | VLM co-fine-tuned on robot + web data; emergent capabilities on novel objects |
| π₀ (Physical Intelligence) | Multi-embodiment training + flow matching for smooth high-frequency actions |
| π₀.5 | Extends π₀ to open-world generalization |
| GEN-0 (Generalist) | Scales pretraining data; harmonic reasoning for sensing + action interplay |
| GR00T N1 (NVIDIA) | Open humanoid robot foundation model; cross-embodiment focus |
| Gemini Robotics | Builds on Gemini 2.0; tasks requiring force control and dexterous manipulation (origami, playing cards) |

**Cross-embodiment results:** The Open X-Embodiment project assembled 1M+ trajectories from 22 robot platforms. RT-1-X achieved ~50% higher success rates than single-robot baselines; RT-2-X showed 3× improvement on emergent skills.

### Deployment Reality (What's Shipped)

Production robots today are largely classical systems:
- **Automotive manufacturing:** welding robots execute the same motion thousands of times with submillimeter precision — manually reprogrammed when the car model changes
- **Warehouse picking:** learned systems handle structured product categories in controlled lighting; unstructured bin picking from arbitrary objects has not been reliably deployed at scale
- **Humanoid robots:** mostly in pilot phases or available as developer platforms; real-world production deployments are rare

The researchers working on learned systems and the regional systems integrators deploying industrial robots largely operate in separate spheres.

### Six Deployment Challenges

**1. Distribution Shift**
Research systems are evaluated on test sets from the same distribution as training data. Deployment environments are, by definition, out of distribution. A manipulation policy trained in a robotics lab encounters different lighting, backgrounds, textures, and camera angles in a warehouse. A policy achieving 95% in the lab might drop to 60% in deployment — not because the policy is wrong, but because the physical world's long tail introduces a large number of potential differences.

**2. Reliability Thresholds**
Research papers report mean success rates. Deployment requires worst-case reliability. A picking robot achieving 95% success attempts thousands of picks per day — that's 50 failures per day, each requiring human intervention. Production systems in manufacturing typically require reliability above 99.9%. Failures in learned policies are not necessarily random; they may cluster around edge cases the training distribution didn't cover.

**3. Latency-Capability Tradeoffs**
The most capable VLA models are often the largest and slowest. Manipulation tasks require control at 20–100Hz. A 7B parameter model on edge hardware might achieve 50–100ms inference — adequate for 10–20Hz, but inadequate for dynamic manipulation needing tight feedback loops. Cloud inference adds network latency that makes real-time control impossible. Dual-system architectures (GR00T N1, Figure's Helix) attempt to resolve this by separating slow semantic reasoning (System 2) from fast motor control (System 1).

**4. Integration Complexities**
A warehouse robot needs to receive task assignments from warehouse management systems (WMS), coordinate with other robots, report status to monitoring dashboards, log events for compliance, and interface with maintenance systems. A research policy that picks objects perfectly is functionally limited if it can't receive instructions, coordinate with conveyor belt timing, or report completion status to inventory tracking.

**5. Safety Certification**
Collaborative robots operating near humans must comply with standards like ISO 10218 and ISO/TS 15066. These standards were written for programmed robots with predictable, analyzable behavior. There is no clear provision for learned policies whose behavior emerges from training data. Formally verifying a 7B parameter neural network is infeasible. Extensive testing can show the presence of failures but not their absence.

**6. Maintenance**
A learned policy that fails in production cannot be debugged by reading code — there is no code, just weights. When a robot behaves unexpectedly, diagnosing whether the problem is perception, planning, control, hardware, or integration requires expertise that most maintenance teams do not currently have.

### Compounding Effects

These challenges interact. Distribution shift degrades performance from 95% to 80%. At 80% reliability, failures occur hundreds of times per day. Running the full VLA on edge hardware to reduce latency further degrades performance. Integrating with WMS introduces additional failure modes. Safety certification takes months. When failures occur, maintenance staff cannot diagnose the root cause. Each challenge makes the others worse — and less deployment data means the distribution shift doesn't improve.

### Closing the Gap

| Challenge | Infrastructure Needed |
|---|---|
| Distribution shift | Scalable teleoperation, deployment-time data collection, domain-specific datasets |
| Reliability | Failure mode characterization, graceful degradation, hybrid learned+programmed architectures, runtime monitoring |
| Latency | Efficient architectures (SmolVLA: 450M params, comparable to larger VLAs), hierarchical systems, hardware-software co-design |
| Integration | Robotics middleware with adapters for WMS/MES/ERP, deployment automation (infrastructure-as-code for physical systems), observability tooling |
| Safety | Behavioral characterization methods, testing frameworks that probe for failure modes, runtime safety override layers, updated standards |

The robotics data flywheel: once robots can collect data while creating economic value, the cost of robot data decreases, subsidized by the value the robot generates. Bootstrapping this flywheel requires crossing an initial deployment threshold — the gap is likely transitory, but it won't close through pure research breakthroughs alone.

## Source

- [[raw/00-clippings/The Physical AI Deployment Gap.md|raw/00-clippings/The Physical AI Deployment Gap.md]]

## Related Topics

- [[computer-vision]] — robot perception relies on vision
- [[3d-vision]] — 3D understanding for manipulation in space
- [[generative-models]] — diffusion models applied to robot policies
- [[attention-transformers]] — transformers backbone for RT-1, RT-2, π₀
- [[self-supervised-learning]] — learning visual representations for robot perception
- [[physical-ai]] — simulation-first training, synthetic data, and world models for embodied systems
- [[omniverse]] — the simulation platform used to build many robot-training environments
