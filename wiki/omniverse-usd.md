# NVIDIA Omniverse and OpenUSD

NVIDIA Omniverse is a platform for building physically accurate 3D simulation applications, industrial digital twins, and physical AI development environments. At its core is **OpenUSD (Universal Scene Description)**, a Pixar-originated open standard for describing, composing, and simulating 3D scenes. OpenUSD is the interchange format and "connective tissue" across tools, teams, and applications in the Omniverse ecosystem.

## Source

- `raw/05-omniverse/Omniverse.md`
- `raw/05-omniverse/01-create-usd-file.py` – `raw/05-omniverse/20-modifying-attributes.py`

## Core OpenUSD Concepts

### Stage

The **stage** is the scenegraph — the unified, composed view of everything in the scene. Stages are not a single file; they are populated from multiple **layers** that are composed together.

A stage has one **Root** prim at the top of the hierarchy. Below the root, multiple USD files are referenced as children — for example, a vehicle scene might reference `Car.usd`, `Environment.usd`, `Lighting.usd`, and `Cameras.usd` as sibling sub-layers under the root. Each of those USD files contains its own **Prims** (the blue icons inside each layer tile). The stage composes all layers into a single, traversable scenegraph at runtime.

```python
from pxr import Usd, UsdGeom

stage: Usd.Stage = Usd.Stage.CreateNew('assets/first_stage.usda')
UsdGeom.Cube.Define(stage, '/cube')
stage.Save()

# Open existing
stage = Usd.Stage.Open('assets/first_stage.usda')
```

### USD File Formats

| Extension | Type | Use Case |
|-----------|------|----------|
| `.usd` | ASCII or binary (auto) | General; format can change without breaking references |
| `.usda` | ASCII text | Human-readable; good for editing and inspection |
| `.usdc` | Compressed binary (Crate) | Efficient storage and loading |
| `.usdz` | Zipped archive (uncompressed) | Read-only distribution; XR experiences |

### Prims (Primitives)

Prims are the fundamental building blocks — containers for data, attributes, and relationships. Every object in a scene is a prim.

**Imageable prims:** Mesh, Light, Xform, Skeleton  
**Non-imageable prims:** Material, Shader, Skeletal Animation

Key prim types:
- **Scope** — grouping mechanism (like an empty folder)
- **Xform** — stores transformation data (translate, rotate, scale) applied to all children

```python
# Traverse all prims depth-first
for prim in stage.Traverse():
    print(prim)

# Get prim at path
box_prim = stage.GetPrimAtPath("/box")
```

### Properties: Attributes and Relationships

**Attributes** store typed data values (position, color, visibility). They can be animated via time-sampled values.

```python
# Create a custom attribute
box_prim.CreateAttribute("weight_lb", Sdf.ValueTypeNames.Float)
```

**Relationships** establish connections between prims (material bindings, collections, shading networks). They enable non-destructive editing and asset reuse.

**Primvars** bind per-geometry data to shaders — UVs, vertex colors, custom deformation parameters.

### Specifiers

Define how a prim or primSpec is interpreted in the composed scene:

```usd
def Cube "Box" { double size = 4 }       # defines the prim
over "Box" { double size = 10 }           # overrides a value in this layer
class "_box" { double size = 4 }          # reusable blueprint (inherited)
```

### Default Prim

Every stage should set a **default prim** — the primary entry point. Required when the stage is used as a reference or payload in another stage.

```usd
#usda 1.0
( defaultPrim = "Car" )
```

### Schemas

Schemas are blueprints that define standard attributes and behaviors:

- **IsA schemas** (Typed schemas) — tell a prim what it *is* (`UsdGeomMesh`, `UsdLuxDomeLight`); one per prim
- **API schemas** — add optional capabilities to any prim without setting a typeName (`UsdPhysicsRigidBodyAPI`)

Key schema modules: `UsdGeom`, `UsdShade`, `UsdLux`, `UsdPhysics`

### Core Python Modules

| Module | Purpose |
|--------|---------|
| `Usd` | Core client API — stages, prims, properties, metadata, composition arcs |
| `UsdGeom` | Geometric objects: meshes, cameras, curves, Xform |
| `UsdShade` | Materials, shaders, shading networks |
| `UsdLux` | Light types: Distant, Sphere, Dome, Rect, Cylinder, Disk, Portal |
| `Sdf` | Scene Description Foundation — layers, paths (`Sdf.Path`), serialization |
| `Gf` | Graphics Foundation — linear algebra, 3D data types |

### Hydra (Rendering Architecture)

Hydra bridges USD scene data and rendering backends via a plugin system:
- **HdStorm** — real-time OpenGL/Metal/Vulkan render delegate (used in usdview)
- **HdEmbree** — CPU path tracer
- Custom backends can be added as render delegate plugins

## Composition

USD **composition** is the algorithm that assembles multiple layers into a single composed scene. Layers can be referenced, inherited, overridden, or payload-loaded. **Value resolution** determines the final value for any property by evaluating all contributing layers in priority order.

Example: a robot arm base layer defines position (0,0,0); an operational layer overrides it to (5,0,0). The composed result is (5,0,0).

## OpenUSD Ecosystem

OpenUSD is the universal interchange standard at the center of an ecosystem of over 80 tools and applications. A radial diagram of the ecosystem shows OpenUSD at the center with spokes connecting to virtually every major 3D and content-creation tool: Unreal Engine, Blender, Maya, 3ds Max, Cinema 4D, Houdini, ZBrush, Substance Painter, Adobe Photoshop, Illustrator, After Effects, SolidWorks, Autodesk Revit, Rhino, SketchUp, Unity, and dozens of specialized VFX, CAD, and simulation tools. This breadth makes OpenUSD the de-facto language for 3D data exchange across industries — from film VFX to automotive CAD to industrial simulation.

## Kit-Based Applications

NVIDIA Omniverse applications are built with **Kit** — an extension-based runtime:

- An app is defined by a `.kit` file that lists all extensions and settings
- Extensions are isolated units of functionality (Python or C++)
- Common extensions: `omni.kit.window.stage`, `omni.kit.window.property`, `omni.physx.bundle`

## Virtual Factory Integration

One of Omniverse's flagship use cases is the virtual factory — a full digital replica of an industrial facility built from CAD, BIM, and process data from multiple vendors.

The workflow has three stages:

**1. Develop Tools and Apps** — BMW Group, for example, built Factory Viewer Apps and a One-Click-to-XR App on top of the Omniverse platform to navigate and inspect the virtual factory in real time.

**2. Connect Existing Tools and Data** — The factory is assembled from data exported by Autodesk Revit, MicroStation, FlexSim, Siemens, Visual Components, and Unity/Unreal. These tools export structure, layout, equipment, process, metadata, product, logistics, robotics animation, and point cloud data — all unified via **USD as the common exchange format**.

**3. Enable New Workflows and Experiences** — The composed virtual factory becomes a shared collaboration space accessible to engineers, managers, technicians, operators, city planners, AEC firms, assembly and manufacturing technologists, and environmental experts simultaneously.

### Factory USD Layer Hierarchy

A real factory assembly graph in USD looks like this:

```
factory.usd
└── sublayers (via Payloads)
    ├── Factory_Shell_Export.usd  →  Factory_Shell_Adjust.usd
    ├── Vehicle_Hanger_Export.usd →  Vehicle_Hanger_Adjust.usd
    ├── Car_Lift_Export.usd       →  Car_Lift_Adjust.usd
    ├── Robot_Arm_Export.usd      →  Robot_Arm_Adjust.usd
    ├── Welding_Assembly_Export.usd → Welding_Assembly_Adjust.usd
    ├── Safety_Fences_Export.usd  →  Safety_Fences_Adjust.usd
    └── Pedestral_Export.usd      →  Pedestral_Adjust.usd
    (shared sublayers)
    ├── Materials_Samples.usd
    ├── Materials_Grid.usd
    ├── Lighting.usd
    ├── SetDressing.usd
    └── Factory_Floor_Walkways.usd
```

Each asset comes from a CAD tool (Creo, Visual Components, SolidWorks, Autodesk Revit) via an **Export** layer. An **Adjust** layer sits beside each export to apply non-destructive overrides (position, material swaps, LOD settings) without modifying the original CAD data. All adjust layers sublayer into the root `factory.usd` and are loaded as **Payloads** for on-demand streaming.

## Digital Twins

**Digital twins** are virtual representations of physical products, processes, and facilities — dynamic digital models of physical assets kept up-to-date with real-time data. Pioneered by NASA's Apollo 13 mission (Earth-based simulators connected to the spacecraft via real-time telemetry).

IoT sensors continuously feed operational data into the twin, enabling dynamic virtual simulations. This bridges the physical and digital worlds: you can simulate scenarios, optimize operations, safely predict and validate real-world performance in a cost-effective virtual environment before touching physical hardware.

**BMW Group uses digital twins to speed up the planning of new factories — with 30% expected efficiency gains in factory planning.**

The twin also serves as a proving ground for Physical AI: autonomous systems like robots and self-driving cars are trained and validated in digital twins before real-world deployment.

### What Makes Digital Twins Possible

- **OpenUSD** — solves the data integration problem across CAD, BIM, IoT, reality capture
- **Generative AI** — natural language interface for querying industrial data; synthetic data generation
- **Computer Graphics** — physically accurate materials, lighting, physics simulation
- **Accelerated Computing** — NVIDIA GPUs for rendering and running physics/AI at industrial scale

### Industry Use Cases

- Factory layout optimization and robotics training
- Autonomous vehicle/robot testing and validation
- AI-enabled defect detection (AOI / optical inspection)
- Smart city urban planning and traffic simulation
- Climate simulation and energy efficiency modeling
- Data center and AI factory optimization

## Physical AI and NVIDIA Cosmos

**Physical AI** — any technology using AI to enable autonomous machines (humanoid robots, drones, self-driving cars) to perceive, reason, and act in the physical world.

### Why Physical AI Is Hard

Two fundamental problems:
1. **Real-world data is costly to capture** — instrumenting real environments, recording diverse edge cases, and annotating data at scale requires enormous resources
2. **Physical testing is dangerous and expensive** — testing an autonomous vehicle or robot in the real world risks damage, injury, and unpredictable outcomes

This is "**The Big Data Gap in Robotics**." NVIDIA's answer: convert the data problem into a compute problem using Simulation (NVIDIA Omniverse), World Foundation Models (NVIDIA Cosmos), and synthetic data.

### Physical AI Foundation Model

A Physical AI foundation model takes two streams of inputs:
- **Sensor Tokens** — tokenized sensor data (camera images, LiDAR, force/torque readings) from the robot's environment
- **Text Tokens** — natural language instructions ("Ask me or tell me to do something")

These are processed by the foundation model to produce **Action Tokens** — discrete representations of the actions the robot should take. The same model architecture deploys across Factories, Automotive, and Robotics applications.

### NVIDIA Cosmos Platform

Cosmos is NVIDIA's World Foundation Model development platform with three pillars:

| Component | Tools | Function |
|---|---|---|
| **Cosmos World Foundation Models (WFMs)** | Predict · Transfer · Reason | Generate and reason about world states |
| **Data Curation & Tokenization** | NeMo Curator · Cosmos Tokenizer | Prepare and encode training data |
| **Post-Training** | PyTorch | Fine-tune models for specific robots and tasks |

### Cosmos Predict — World Generation

Cosmos Predict is a generalist model for world generation. It takes one or more of:
- **Text prompt** — describe the scene in natural language
- **Start image + End image** — define the beginning and end of a sequence
- **Video** — provide an existing video clip

...and generates photorealistic video of the world, which serves as synthetic training data for Physical AI systems.

### Cosmos Transfer — Controllable Data Augmentation

Cosmos Transfer performs controllable data augmentation at scale. The pipeline:

1. **Input Video** — real or synthetic robot/driving video
2. **Compute Control** — extract multiple modality representations using computer vision tools:
   - GroundingDINO + SAM2 → **segmentation map** (colored regions per object)
   - DepthAnything v2 → **depth map**
   - Blur → **blurred reference**
   - Canny Edge Detector → **edge map**
3. **Control Modalities** — these four representations become the conditioning signal
4. **Cosmos Transfer** — generates a new output video matching the spatial structure of the input but with varied appearance, lighting, environments, or object properties
5. **Output Video** — augmented training data (e.g., same robot manipulation task in a different room, on a different table)

This lets you take a small set of real robot demonstrations and expand them into a large, diverse training dataset without additional real-world recording.

### Isaac GR00T N1.5 — Robot Foundation Model

Isaac GR00T N1.5 is NVIDIA's open humanoid robot foundation model. Architecture:

1. **Inputs:** sensor images + text instruction (e.g., "Pick up the industrial object and place in yellow bin")
2. **Sensor Tokens + Text Tokens** — tokenized multimodal representations
3. **Vision Language Model (System 2)** — slow, deliberate reasoning; interprets intent and scene
4. **Diffusion Transformer Model (System 1)** — fast, reactive; generates action tokens via diffusion
5. **Action Tokens** → robot motor commands for the humanoid body

Properties:
- **Open** — available on Hugging Face
- **Fully customizable** — post-train with real and synthetic data for your specific robot and task
- **Cross-embodiment** — post-train and deploy across multiple robot form factors

### End-to-End Physical AI Workflow

The full pipeline from data to deployment:

1. **Simulation** (NVIDIA Omniverse / Isaac Sim) — physics-accurate virtual environments with robot sensors
2. **Synthetic data generation** (Cosmos Predict + Cosmos Transfer) — generate diverse training video at scale
3. **Foundation model training** — train on synthetic + curated real data using NeMo Curator
4. **Isaac Lab** — GPU-accelerated reinforcement learning and imitation learning environment
5. **Sim-to-real transfer** — deploy trained policies to physical robots; validate in digital twins before real deployment

### Robot Architecture (Perception–Planning–Action)

A complete robot system has the following architecture:

**Perception Layer (red):**
- **Sensors** — cameras, LiDAR, IMU, force-torque sensors
- **Mapping Database** — persistent map of the environment
- **Localization** ↔ **Perception** — mutual feedback loop: localization uses perception results to refine position estimate; perception uses the map to constrain object detection

The perception layer's purpose: utilize sensors and mapping systems to assess the environment and determine position and state.

**Planning Layer (gray):**
- **Global Planning** — defines the mission and waypoints to reach a goal
- **Behavioral Planning** — determines which actions to take given the current scene
- **Local Planning** — generates specific trajectories for immediate tasks

Planning receives inputs from the full perception layer (Sensors, Mapping DB, Localization, Perception) and outputs to Control.

**Action Layer (purple):**
- **Control** — tracks trajectory states to execute movements
- **Actuation** — drives motors and effectors

**Simulation (green)** — sits alongside the action layer, enabling sim-to-real transfer and policy validation.

### Robot Learning Algorithms

Four learning paradigms used in robot training:

| Type | Description | Examples |
|---|---|---|
| **Supervised Learning** | Learning from labeled data | Classification, object recognition/detection, pose estimation |
| **Unsupervised Learning** | Learning patterns from unlabeled data | Clustering for environment mapping, anomaly detection |
| **Imitation Learning** | Learning by mimicking demonstrations | Teaching a robot assembly task by showing human operator demonstrations; locomotion |
| **Reinforcement Learning** | Learning through trial and error to maximize rewards | Grasping, locomotion, complex multi-step tasks |

### Robot Sensors (Isaac Sim)

Robots use diverse sensor modalities:
- **Cameras:** monocular, stereo, RGB-D, thermal, event-based
- **LiDAR:** 2D (flat plane), 3D (full sphere), solid-state (no moving parts)
- **Other:** ultrasonic, radar, GPS, IMU, wheel encoders, magnetic sensors, environmental (gas/humidity), touch/force

**URDF (Unified Robot Description Format)** — XML format for describing robot links, joints, geometry, and physical properties (mass, inertia).

## XR Integration

USDZ is the primary format for XR experiences — read-only, self-contained archives. Omniverse Kit supports XR profiles for Meta Quest, tablet AR, and VR via extension bundles:

```
"omni.kit.xr.core" = {}
"omni.kit.xr.profile.vr" = {}
"omni.kit.xr.profile.ar" = {}
```

## Related Topics

- [[3d-vision]] — 3D representations (NeRF, Gaussian Splatting) used in digital twin capture
- [[robot-learning]] — robot foundation models, imitation learning, diffusion policy
- [[generative-models]] — diffusion/world models (Cosmos) for synthetic data generation
- [[computer-vision]] — computer vision models trained and deployed in Omniverse environments
- [[gpu-cuda]] — accelerated computing required for Omniverse simulation at scale
