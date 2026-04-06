# 3D Vision

3D vision deals with representing, understanding, and generating 3D geometry and scenes. Unlike 2D images (a grid of pixels), 3D data comes in many representations — point clouds, meshes, voxels, and neural implicit functions. This field is critical for robotics, autonomous driving, AR/VR (Omniverse, XR), and 3D content creation.

## Source

- `raw/03-stanford-cs231n/Stanford CS231N.md`

## Shape Representation Considerations

Any 3D shape representation must address five concerns:
1. **Storage** — how is it stored in computer memory?
2. **Creation** — what input metaphors/interfaces allow authoring new shapes?
3. **Operations** — what editing operations are natural? (simplification, smoothing, filtering, repairing)
4. **Rendering** — how does it render? (rasterization, ray tracing, neural rendering)
5. **Animation** — can it be animated? How?

## Shape Representations

There are two broad families: **explicit** (the surface is directly represented) and **implicit** (the surface is defined as the level-set of a function).

### Explicit Representations

Easy to sample points on the surface; harder to test if a point is inside or outside.

#### Point Clouds
- A set of 3D points (x, y, z) sampled from a surface
- No connectivity information
- Captured by depth cameras, LiDAR, Structure-from-Motion

**Key properties a network must respect:**
- **Point permutation invariance:** order of points should not matter
- **Sampling invariance:** different scans give different point densities but represent the same object

**PointNet** — first deep network to operate directly on point clouds:
- Applies shared MLP to each point independently
- Global max-pooling aggregates all points into one descriptor
- Achieves permutation invariance by design

Paper: [PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation](https://arxiv.org/pdf/1612.00593)

**Graph Neural Networks on Point Clouds:**
Dynamic edge convolution builds a graph between nearby points and applies graph convolution — captures local structure better than PointNet.

Paper: [Dynamic Graph CNN for Learning on Point Clouds](https://arxiv.org/pdf/1801.07829)

#### Polygon Meshes
- Vertices + edges + faces (triangles/quads)
- Used in 3D modeling (Blender, Maya), game engines, rendering
- Operations:
  - **Subdivision:** increase resolution by splitting faces
  - **Simplification:** reduce polygon count while preserving shape
  - **Regularization:** ensure face quality (no degenerate triangles)

#### Parametric Representations
- Surfaces defined by mathematical parameters (u, v) coordinates
- **Parametric curves:** Bezier curves, B-splines, NURBS
- **Example:** a torus is defined analytically as `f(u,v) = ((2 + cos u)cos v, (2 + cos u)sin v, sin u)` — a smooth closed surface with no polygon mesh needed. Sampling is easy (just plug in u,v values); testing inside/outside requires solving the equation.

### Implicit Representations

Easy to test inside/outside; harder to sample points on the surface.

#### Occupancy Networks
Learn a function f(x, z) → [0, 1] that outputs "is this 3D point x inside the object?"
Paper: [Occupancy Networks: Learning 3D Reconstruction in Function Space](https://arxiv.org/pdf/1812.03828)

#### Signed Distance Functions (SDF)
Learn a function f(x) → ℝ that outputs the signed distance to the nearest surface (negative inside, positive outside, zero on surface).
Paper: [DeepSDF: Learning Continuous Signed Distance Functions for Shape Representation](https://arxiv.org/pdf/1901.05103)

#### Level Sets
The surface is the zero-level-set of a scalar field.

#### Distance Functions
Scenes defined purely by distance function composition:
- Reference: [scene of pure distance functions (iquilezles)](https://iquilezles.org/articles/raymarchingdf/)

#### Constructive Solid Geometry (CSG)
Combine primitive shapes using boolean operations (union, intersection, difference).

### Voxel Grids
- 3D analog of pixels: regular cubic grid
- Memory scales as O(N³) — expensive at high resolution
- **OctNet:** uses an octree structure to allocate more resolution near surfaces, saving memory
  - Paper: [OctNet: Learning Deep 3D Representations at High Resolutions](https://arxiv.org/pdf/1611.05009)

## Neural Radiance Fields (NeRF)

NeRF represents a 3D scene as a continuous function:

```
(x, y, z, θ, φ) → (RGB color, density σ)
```

Where (x, y, z) is a 3D point and (θ, φ) is viewing direction.

**Rendering:** shoot camera rays into the scene → sample N points along each ray → query the network for (color, density) at each point → integrate via volume rendering to get pixel color.

**Training:** minimize the difference between rendered images and real training photos.

NeRF memorizes a specific scene (not a general model). Limitations: slow rendering, per-scene optimization.

Paper: [NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis](https://arxiv.org/pdf/2003.08934)

## 3D Gaussian Splatting

Represents a scene as a set of **3D Gaussian blobs** (soft 3D pixels) instead of a neural network:

Each Gaussian has:
- Position (x, y, z)
- Size + shape (anisotropic covariance matrix)
- Color (RGB)
- Opacity (α)
- View-dependent shading

**Rendering:** project ("splat") Gaussians onto the 2D screen → blend via GPU rasterization → **real-time rendering**.

**Training:** start from a Structure-from-Motion point cloud → initialize one Gaussian per point → optimize all parameters via differentiable rendering.

**Advantages over NeRF:**
- Real-time rendering (NeRF: seconds per frame)
- Faster training
- Easier to edit and compress

Paper: [3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://arxiv.org/pdf/2308.04079)

## Representing Element Structure

Complex objects benefit from structured representations that capture part hierarchy and relationships:

| Representation | Properties | Tradeoffs |
|---|---|---|
| **Segmented Geometry** | Object split into labeled parts (e.g., chair seat, legs, back) | Simple to construct; integrity of atomic elements not guaranteed by construction |
| **Part Sets** | Unordered collection of geometry pieces | Flexible; no relationship structure |
| **Relationship Graphs** | Nodes = parts, edges = spatial relationships | Captures spatial constraints |
| **Hierarchies** | Tree structure (e.g., base → seat → legs) | Models natural parent-child structure |
| **Hierarchical Graphs** | Tree + lateral relationships per level | Models both hierarchical and lateral; difficult to annotate |
| **Programs** | Code that generates the shape (circle, line, draw commands) | Subsumes all other representations; expresses degrees of freedom; hardest to get training data |

Programs are the most expressive — they can generate any other representation — but require collecting data in program form, which is expensive.

## 3D Datasets

| Dataset | Content | Scale |
|---------|---------|-------|
| [Princeton Shape Benchmark](https://shape.cs.princeton.edu/benchmark/) | 3D CAD models in 182 categories (sunflower, chair, person, shuttle, hand, piano, car, dog) | 1,814 models |
| [ShapeNet](https://arxiv.org/pdf/1512.03012) | 3D CAD models | 55 categories |
| [Objaverse](https://arxiv.org/pdf/2212.08051) | Annotated 3D objects | 800K objects |
| [Objaverse-XL](https://arxiv.org/pdf/2307.05663) | 3D objects | 10M+ objects |
| [CO3D](https://arxiv.org/pdf/2109.00512) | Real-world object scans | Common objects |
| [ScanNet](https://arxiv.org/pdf/1702.04405) | Indoor 3D scenes (RGB-D) | ~1500 scans |
| [ScanNet++](https://arxiv.org/pdf/2308.11417) | High-fidelity indoor scenes | Detailed |

## AI Tasks on 3D Data

- 3D object classification (ShapeNet models)
- 3D semantic segmentation (label each point)
- 3D object detection (bounding boxes in 3D)
- 3D reconstruction (from images or depth)
- Novel view synthesis (NeRF, Gaussian Splatting)
- Multi-view reconstruction

### Multi-view CNN
Render a 3D shape from multiple viewpoints → classify each 2D view with a CNN → aggregate predictions.

Paper: [Multi-view Convolutional Neural Networks for 3D Shape Recognition](https://arxiv.org/pdf/1505.00880)

### AtlasNet
Represent surfaces as multiple learned parametric patches — smoother than point clouds.
Paper: [AtlasNet: A Papier-Mâché Approach to Learning 3D Surface Generation](https://arxiv.org/pdf/1802.05384)

## Connection to Pavel's Interests

- **Omniverse:** NVIDIA Omniverse uses USD + 3D Gaussian Splatting for real-time scene representation
- **Robotics / LeRobot:** 3D perception is fundamental — robots need spatial understanding
- **XR:** AR/VR requires real-time 3D scene reconstruction and rendering

## Related Topics

- [[computer-vision]] — 2D vision foundation for 3D understanding
- [[attention-transformers]] — ViT and transformers applied to 3D point clouds
- [[generative-models]] — NeRF as a neural implicit model; 3D-GANs for 3D shape generation
- [[robot-learning]] — robots need 3D scene understanding for manipulation
- [[convolutional-neural-networks]] — multi-view 3D approaches use 2D CNNs
