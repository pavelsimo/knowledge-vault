---
title: "WTF is a World Model?"
source: "https://x.com/vai_viswanathan/status/2050177504392998932"
author:
  - "[[@vai_viswanathan]]"
published: 2026-05-01
created: 2026-05-02
description: "\"World model\" is the phrase of the moment. Fei-Fei Li's World Labs raised $230M out of stealth and followed it with a $1B round. Yann LeCun ..."
tags:
  - "clippings"
---
![[raw/00-clippings/images/33abb7f255ddf690b062f88bea8d2ea1_MD5.jpg]]

"World model" is the phrase of the moment. Fei-Fei Li's World Labs raised [$230M](https://x.com/search?q=%24230M&src=cashtag_click) out of stealth and followed it with a [$1B](https://x.com/search?q=%241B&src=cashtag_click) round. Yann LeCun left Meta to start AMI Labs, which raised $1.03B at a $3.5B valuation to build world models from the ground up. Google DeepMind shipped Genie 3. OpenAI pitched Sora as a "world simulator." NVIDIA released Cosmos. Dreamer 4 solved Minecraft's Diamond Challenge from offline data alone. Every robotics lab worth its salt now has a world model paper.

The problem is that when you actually try to pin down what a world model is, you get five different answers depending on who you ask.

This article is an attempt to unpack the term. First, what is a world model? Second, what are the current approaches? And third — the part that matters if you build robots — where do world models actually earn their keep in a modern robotics stack?

## What Are World Models?

The most important thing to understand up front: **world modeling is a problem statement, not a model architecture.**

The closest analogy here is SLAM — Simultaneous Localization and Mapping. SLAM isn't a specific algorithm. It's a problem: given a stream of sensor data, figure out where you are while building a map of your surroundings. There are dozens of SLAM approaches. Filter-based methods like EKF-SLAM and FastSLAM. Graph-based methods built on optimization backends like GTSAM or Ceres Solver. Different sensor modalities — cameras, LiDAR, IMUs, or fusions of all three. Even within visual SLAM, you have direct methods that work on raw pixel intensities and feature-based methods that extract keypoints like ORB or SIFT.

World models are similar. "Build a world model" is the goal. How you build one is wide open.

**LeCun's Definition**

![[raw/00-clippings/images/fc441d82174d757b44445eec7cee4257_MD5.jpg]]

The cleanest formal definition comes from Yann LeCun ([source](https://x.com/ylecun/status/1759933365241921817)):

Given:

- x(t): an observation
- s(t): a previous estimate of the state of the world
- a(t): an action proposal
- z(t): a latent variable proposal

A world model computes:

- h(t) = Enc(x(t)), the representation
- s(t+1) = Pred(h(t), s(t), z(t), a(t)), the prediction

Where:

- Enc() is an encoder (a trainable deterministic function, e.g. a neural net)
- Pred() is a hidden state predictor (also a trainable deterministic function)
- z(t) represents the unknown information that would allow us to predict exactly what happens. It must be sampled from a distribution or varied over a set. It parameterizes the set (or distribution) of plausible predictions.

Let's ground this formal definition with an example.

**A Worked Example: A Self-Driving Car**

Imagine a self-driving car parked in an empty lot with a single forward-facing camera. It has two controls: a steering angle and an accelerator.

- **x(t)** — the initial image the camera sees. Asphalt, a horizon line, maybe a fence.
- **s(t)** — the car's internal state: position, velocity, heading, current steering angle. It starts at (0, 0, 0) with zero velocity.
- **a(t)** — the action the car decides to take. Let's say we're doing donuts: full steering lock to the left (-1) and full throttle (+1).
- **z(t)** — the unobservable stuff. How much grip the tires have. A gust of wind. Invisible oil on the pavement. Sensor noise. Anything in the real world that would affect the outcome but that you can't read off the current state. A deterministic model ignores z(t). A probabilistic one samples it from a distribution, giving you a set of plausible futures rather than a single prediction.

Given these, the world model predicts s(t+1) — the next state of the car.

**IMPORTANT: this is not a prediction of the next image.** It's a prediction of the underlying state. The car's new position, velocity, and heading after a fraction of a second of flooring it at full lock.

**The Decoder Extension**

If you do want to generate the next image, you add a decoder step ([suggested by Kevin Murphy](https://x.com/sirbayes/status/1759987256994214341)):

x(t+1) = Dec(s(t+1))

This distinction matters more than it looks. LeCun deliberately separates prediction from rendering. The world model's job is to reason about state. Rendering that state back into pixels is a separate, optional step. As we'll see, this separation is exactly where the main schools of world modeling disagree.

![[raw/00-clippings/images/e13b9d5a23ece061afb3e2cc796335cb_MD5.jpg]]

## What Are the Current Approaches?

Today there are three dominant paradigms for building modern world models. Each takes a different stance on what to compress, what to predict, and whether to render.

**1\. Generative World Models**

The headline-grabbing category. Models like **Sora**, **Veo**, **Genie 3**, **GameNGen**, and World Labs' **RTFM** learn to predict the next frame of video given a past context and an action input.

<video preload="auto" tabindex="-1" playsinline="" aria-label="Embedded video" poster="https://pbs.twimg.com/tweet_video_thumb/HHNDEg1WEAAYyWi.jpg" src="https://video.twimg.com/tweet_video/HHNDEg1WEAAYyWi.mp4" type="video/mp4" style="width: 100%; height: 100%; position: absolute; background-color: black; top: 0%; left: 0%; transform: rotate(0deg) scale(1.005);"></video>

GIF

Source: [https://deepmind.google/models/genie/](https://deepmind.google/models/genie/)

Architecturally they're usually **autoregressive transformers** or **video diffusion models**, often combined. You give the model a starting image (or text prompt), optionally a stream of actions, and it predicts the world forward frame by frame.

The framing is straightforward: if the model can generate the future accurately, it must on some level understand the world. Play a game inside Genie and the environment seems to have consistent physics and object permanence. Drive a virtual car and the road responds.

But these models also come with well-known failure modes:

- **Autoregressive drift** — small errors compound over long rollouts
- **Hallucination** — objects appear and disappear when occluded
- **Physical implausibility** — water flows uphill, rigid objects deform, lighting is inconsistent
- **Memory loss** — the world changes when you look away

**How this fits LeCun's definition:** Generative models collapse state and observation into the same thing — they predict directly in observation (pixel) space, skipping the abstract state. LeCun would argue this is an impoverished instantiation: almost all of the model's capacity goes into rendering, leaving less for the parts that matter for reasoning and control.

**2\. Latent World Models**

Instead of predicting pixels, latent world models predict in a compressed, abstract representation space. Two subfamilies dominate, and they're philosophically opposed in a way that's worth taking seriously.

**Latent Dynamics Models** — **Dreamer / DreamerV3 / Dreamer 4**, **PlaNet**, **TD-MPC**. These grew out of model-based reinforcement learning. A recurrent state-space model (RSSM) learns to predict future latent states conditioned on actions. Crucially, these models are typically trained with **reconstruction loss** — a decoder forces the latent to retain enough information to regenerate the observation — alongside **reward prediction** so the latent is grounded in what matters for the task. A policy and value function are then trained on trajectories imagined inside this latent space.

**JEPA — Joint Embedding Predictive Architecture** — **I-JEPA**, **V-JEPA**, **V-JEPA 2**, and most recently **LeWorldModel (LeWM)** from AMI Labs and collaborators. A vision encoder produces embeddings of the current state; a predictor predicts the embeddings of future or masked-out regions. No reward. No pixel reconstruction. The model is trained purely via self-supervised prediction in representation space.

![[raw/00-clippings/images/d07c7c3ad8f410b74f0282a5910134ad_MD5.jpg]]

Source: "V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning"

While both operate in the latent space, they differ in four important ways:

- **Training signal.** Latent Dynamics Models are trained end-to-end with a reconstruction loss (via a decoder) and usually a reward signal; the latent state is shaped by what's needed to regenerate pixels and predict returns. JEPA is trained with a single self-supervised prediction-in-embedding-space objective — no decoder, no reward.
- **Stance on generation.** Latent Dynamics Models embrace generation; Dreamer 4, for instance, can imagine full video rollouts from the latent state. JEPA rejects generation as a training objective entirely. LeCun's argument is that the world contains inherently unpredictable details (leaves on a tree, noise in a sensor) and forcing the model to predict them at the pixel level wastes capacity on things that fundamentally cannot be predicted.
- **Task specificity.** Latent Dynamics Models are typically trained for a specific environment or task, with the reward shaping the latent. JEPA is trained in a task-agnostic, reward-free way on video and then adapted to downstream control via MPC or a small action-conditioned predictor.
- **How control happens.** Latent Dynamics Models usually train an explicit actor-critic inside the world model. JEPA-based controllers typically do MPC at test time: sample candidate action sequences, simulate forward in embedding space, and pick the one whose predicted embedding lands closest to a goal embedding.

**How this fits LeCun's definition:** This is the best fit for the formal definition, unsurprisingly. Latent Dynamics Models have a strong Enc(), a strong Pred() via RSSM, stochastic sampling z(t), and a Dec() used during training but often dropped at plan time. JEPA is the purest fit — Dec() is absent by design, which LeCun argues is a feature, not a bug.

**3\. 3D Neural World Models**

The third category commits to 3D geometry as the representation. **NeRF** pioneered this — an implicit neural function that maps 3D coordinates to color and density, rendered via volumetric ray marching. **3D Gaussian Splatting** has largely replaced NeRF in the last two years by swapping the implicit function for an explicit set of millions of small semitransparent gaussians, which render dramatically faster.

**World Labs** is the flagship company here. Their product **Marble** generates persistent, explorable 3D worlds from text, images, or video. You export the result as a Gaussian splat file, a mesh with collider geometry, or a video — formats you can drop into Unreal, Unity, Blender, or NVIDIA's Isaac Sim.

**How this fits LeCun's definition:** Partial fit. 3D Neural models nail the representation half — Enc() is strong, the 3D structure is an excellent state representation. But Pred() is typically weak. A static NeRF or splat doesn't predict anything; it just renders what it was trained to render. Dynamic extensions exist, but they're not the core design. In LeCun terms, these are better described as world representations than world models — and World Labs' push toward RTFM is an explicit attempt to close that gap.

**Summary**

![[raw/00-clippings/images/4d21415b3077a359165d8edf12d6e95e_MD5.jpg]]

Two columns do most of the work here. The **Pred()** column reveals which approaches are actually doing forward prediction in a meaningful sense. Generative models predict — but they conflate s(t+1) and x(t+1) into a single pixel output, skipping the abstract state entirely. NeRF and 3DGS don't really predict at all; they render a fixed scene from new viewpoints. Only Latent Dynamics Models and JEPA have clean, abstract Pred() over actions.

The **Dec()** column is the real philosophical fault line. Generative and 3D Neural models put most of their capacity into rendering pixels. Latent Dynamics Models use a decoder during training and can optionally drop it at plan time. JEPA refuses a decoder outright. How much a world model invests in decoding back into pixels is arguably the biggest open design question in the field.

## How Are World Models Used in Robotics?

The practical question for anyone building robots: when does a world model actually earn its keep? The honest answer is that world models now show up in almost every phase of the robotics development lifecycle — before training, during training, after training, and at deployment. There are five distinct use cases.

**1\. Evaluation**

Running a policy against a learned world model as a proxy for real-world testing.

This is the use case with the most obvious short-term payoff, because real robot evaluation is brutally slow. Setting up a task, running enough trials for statistical significance, resetting between episodes, and dealing with hardware drift can take days of wall-clock time per policy checkpoint. Teams routinely burn thousands of engineering hours on evaluation alone. A world model lets you run the same suite against hundreds of policy checkpoints in parallel on a cluster — and because the initial frames come from real robot cameras, the evaluation domain is much closer to deployment than a handcrafted simulator.

Examples: **WorldGym** (r = 0.78 correlation with real-world success rates, 3.3% mean error across VLAs), **DreamDojo** (r = 0.995 across policy checkpoints), and the **Veo World Simulator** for Gemini Robotics (validated across 1,600+ real trials).

A closely related use case — really an extension of evaluation — is **safety red-teaming**. Instead of asking "does this policy succeed?" you ask "what scenarios make this policy fail?" The Veo/Gemini paper is the canonical example: generative image editing drops adversarial objects, distractors, and safety-critical elements into scenes, then rolls the policy out to see whether it does something unsafe. No hardware risk, no staged demonstrations, and you can probe scenarios that would be impossible to set up physically (think infants crawling into a robot's workspace, or liquids on a surgical robot's instruments). This is likely the first place where world models deliver undeniable operational value — the alternative isn't just slower, it's impossible.

**2\. Direct Planning**

Querying the world model at runtime to choose actions.

Instead of learning a policy that maps observations directly to actions, the robot proposes candidate action sequences, simulates them inside the world model, and executes whichever one looks best. The world model is the planner.

The JEPA line is the flagship example. **V-JEPA 2-AC** uses Model Predictive Control in embedding space — given a goal image, pick actions that minimize predicted-embedding-to-goal distance, then re-plan at the next step. **LeWorldModel** pushes this further: a compact 15M-parameter JEPA that plans up to 48× faster than foundation-model world models while remaining competitive on manipulation benchmarks. **DreamDojo** uses a similar propose-simulate-score-execute loop, sampling candidate action chunks from a policy ensemble and picking the best via an external value model, yielding roughly 2× improvement over uniform sampling.

**3\. Training Gym (RL in Imagination)**

Training policies inside a world model. This is the direct descendant of Sutton's 1991 Dyna architecture: learn a model, then use it to generate cheap simulated experience for policy updates.

![[raw/00-clippings/images/4f9e0db192c8568bd87f12c6b98a83de_MD5.jpg]]

Source: "World-Gymnast: Training Robots with Reinforcement Learning in a World Model"

**3a. Training in the world model**

The core idea is straightforward: roll the policy forward in the learned world model, score the resulting rollouts (either with a learned reward function or with a VLM judge), and use the scores to update the policy via RL. Real-world interaction budget drops by orders of magnitude.

This paradigm was first proven on physical robots by **DayDreamer** (Berkeley, 2022), which trained a quadruped to walk from scratch in one hour with no simulator. It scales up in **Dreamer 4** (2025), which solved Minecraft's Diamond Challenge — 20,000+ actions from raw pixels — from offline data alone. On the robotics side, **Robotic World Model (RWM)** demonstrates zero-shot transfer to ANYmal D legged hardware, **World4RL** uses a diffusion world model to refine imitation-learned manipulation policies, **World-Gymnast** trains VLA policies against WorldGym with VLM reward and outperforms supervised finetuning by up to 18× on Bridge robots, and **GigaBrain-0.5M\*** (RAMP) applies the same recipe at VLA-foundation-model scale.

Worth flagging: the modern versions of this are mostly used to refine pretrained policies, not to train from scratch. Bootstrapping from supervised finetuning on a base VLA is now standard, with the world model providing the RL signal on top. Pure from-scratch training in imagination — DayDreamer-style — is still mostly a locomotion-scale phenomenon.

**3b. Iterative world model updates**

If you stop here, the world model is static — pretrained once and used as a fixed gym. But the same real-world deployments used for evaluation produce trajectories that are exactly what the world model needs to improve. This gives you a closed loop: policy rollouts on real hardware → finetune the world model → better imagined rollouts → better policy updates → repeat.

This is textbook Dyna, 35 years later. **World-Gymnast** implements it explicitly, collecting real-robot trajectories during AutoEval evaluation and using them to finetune WorldGym for 120k steps between rounds. The authors explicitly cite Sutton 1991 and show that iterative refinement matters: trajectories from a Dyna-updated world model adhere to real-world behavior more closely than those from software simulators.

The implications are bigger than the specific paper. It means a production robotics system can improve its world model as a side effect of doing its normal evaluation work. Every evaluation run is also a data collection run for the model that powers the next round of training. The line between "offline pretraining" and "online deployment" starts to dissolve.

**3c. Test-time training (TTT)**

The third sub-theme pushes this further: do the policy update at deployment time, from a novel scene that the pretrained policy hasn't seen.

Start the robot in a new environment. Before executing any actions, finetune the policy via RL inside the world model — imagined rollouts only, no real-world interaction. Then deploy the specialized policy on the actual task.

The numbers from World-Gymnast are striking: on a "close the drawer" task with a novel initial frame, test-time training pushes success from 62% to 100%. No real-world rollouts, no additional demonstrations, no new training data — just a quick RL finetune inside the world model before the policy is allowed to touch the hardware. This is a qualitatively new capability. It means a robot can prepare for a task it hasn't seen by practicing in imagination.

Iterative updates and TTT together turn the training gym from a static pretraining environment into a continuous learning substrate. This is the part of the world model story that is least discussed and arguably most consequential for robotics.

**4\. Synthetic Data Generation**

World model as a data factory.

<video preload="auto" tabindex="-1" playsinline="" aria-label="Embedded video" poster="https://pbs.twimg.com/tweet_video_thumb/HHNERlvXoAAbBWM.jpg" src="https://video.twimg.com/tweet_video/HHNERlvXoAAbBWM.mp4" type="video/mp4" style="width: 100%; height: 100%; position: absolute; background-color: black; top: 0%; left: 0%; transform: rotate(0deg) scale(1.005);"></video>

GIF

Source: [https://www.nvidia.com/en-us/ai/cosmos/](https://www.nvidia.com/en-us/ai/cosmos/)

This is distinct from the Training Gym because there's no policy rollout in the loop, no reward signal, no RL. The world model generates trajectories offline — new viewpoints, new backgrounds, new objects, new lighting conditions — and those trajectories are used for standard supervised imitation learning.

**GigaBrain-0** is the headline example: a VLA foundation model trained on about 1,000 hours of real robot data augmented with large quantities of world-model-generated data (video generation, real-to-real transfer, human-to-robot transfer, view transfer, sim-to-real transfer). Increasing the synthetic-data ratio monotonically improves generalization across appearance, placement, and viewpoint shifts.

**NVIDIA Cosmos** is the closest thing to a general-purpose platform for this. Cosmos is explicitly marketed as a world foundation model for physical AI, used to generate synthetic training data at scale for robotics and autonomous driving. It's now being used as a backbone in downstream work like **Cosmos-Surg-dVRK** (surgical policy evaluation) and as a world model component in broader VLA training pipelines.

**World Labs' Marble → Isaac Sim pipeline** is another flavor of this: generate a photorealistic kitchen or warehouse environment, export the splat and collider mesh, and feed it into a physics simulator for robot training. Weeks of manual environment curation compress into minutes.

**5\. World-Action Models (WAMs)**

A unified architecture in which the world model is the policy.

Classical VLAs map observation + language → action. WAMs jointly predict the future video and future actions in a single model, training with aligned losses. The claim is that learning to predict how the world evolves under action gives much stronger physical priors than learning actions alone.

Examples: **DreamZero** (a 14B autoregressive diffusion transformer built on a video diffusion backbone; reports 2× generalization gain over state-of-the-art VLAs and hits real-time closed-loop control at 7 Hz), **WorldVLA / RynnVLA-002**, **GigaWorld-Policy**, **Motus**, and **Cosmos-Policy**.

<video preload="auto" tabindex="-1" playsinline="" aria-label="Embedded video" poster="https://pbs.twimg.com/tweet_video_thumb/HGmhb4LX0AAsKjK.jpg" src="https://video.twimg.com/tweet_video/HGmhb4LX0AAsKjK.mp4" type="video/mp4" style="width: 100%; height: 100%; position: absolute; background-color: black; top: 0%; left: 0%; transform: rotate(0deg) scale(1.005);"></video>

GIF

Source: [https://dreamzero0.github.io](https://dreamzero0.github.io/)

The category also has its own emerging self-critique. **Fast-WAM** (2026) asks a pointed question: do WAMs actually need to generate video at test time, or is video prediction mainly useful as a training objective? Their answer leans toward the latter — a WAM that video-co-trains but skips future generation at inference runs 4× faster with competitive performance. Early evidence that the core value of the approach may be in representation learning rather than runtime simulation.

**Where They Show Up in the Lifecycle**

Step back and look at the five use cases together, and a pattern emerges. A world model isn't a single tool you reach for at one moment — it's a substrate that shows up across the entire robotics ML pipeline:

![[raw/00-clippings/images/7ac0df510673acd75eb81320ed5d9db1_MD5.jpg]]

Before you train, the world model generates data. During training, it's the environment. After training, it's the grader and the adversary probing for safety failures. At deployment, it's the planner — or, increasingly, it is the policy. And in the iterative-update regime, the line between training and deployment dissolves entirely: the robot's experience in the world feeds back into the world model, which improves the substrate for the next training cycle.

That's a qualitatively different picture from classical robotics, where maps, simulators, dynamics models, and policies were separate artifacts built by separate teams. The trend is toward one learned substrate that does all of these jobs.

## Conclusion

What should be clear by now is how much variation hides inside the phrase "world model." Four quite different architectural approaches — generative, latent dynamics, JEPA, 3D neural — all claim the label, and they disagree on fundamentals: whether to render pixels, whether to use reward, whether to commit to 3D structure, whether the policy and the world model are separate or fused. On top of that sit five distinct robotics use cases — data generation, training gym, evaluation, planning, unified policy — each touching a different phase of the development lifecycle. "World model" is the problem statement; the space of solutions and applications is still rapidly expanding.

We're at the beginning, not the end, of this story. Evaluation pipelines that run overnight on a cluster instead of a week in a lab will let robotics teams iterate at fundamentally different speeds. Test-time training means a robot can prepare for a new task in imagination before touching hardware. Iterative world model updates mean every deployment improves the substrate for the next training cycle. World-Action Models blur the line between simulator and policy. These aren't incremental improvements — they're the kind of shifts that change what's possible.

As the field develops, we'll see which of these threads actually drive the breakthroughs in robotics — which approaches scale, which use cases become standard infrastructure, which combinations turn out to matter most. Robotics hasn't yet had the inflection moment that LLMs had for language, where a new model paradigm made previously impossible capabilities suddenly routine. World models are the most promising candidate for what that inflection looks like. The next few years will tell us whether the bet pays off.