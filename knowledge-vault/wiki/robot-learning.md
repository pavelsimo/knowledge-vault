# Robot Learning

Robot learning covers how machines acquire skills through experience, demonstrations, or interaction with the environment. It bridges computer vision, reinforcement learning, and imitation learning to build robots that can perceive, plan, and act in the physical world.

## Source

- `raw/03-stanford-cs231n/Stanford CS231N.md`

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

## Related Topics

- [[computer-vision]] — robot perception relies on vision
- [[3d-vision]] — 3D understanding for manipulation in space
- [[generative-models]] — diffusion models applied to robot policies
- [[attention-transformers]] — transformers backbone for RT-1, RT-2, π₀
- [[self-supervised-learning]] — learning visual representations for robot perception
