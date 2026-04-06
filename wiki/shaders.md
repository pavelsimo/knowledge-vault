# Shaders and GPU Programming

A shader is a type of computer program — a set of instructions — that runs on the GPU. Originally named for "shading," shaders controlled variance of light and dark over geometric surfaces. Today they are the core building block of real-time graphics, responsible for every pixel on screen in a game or 3D application.

## Source

- `raw/00-clippings/What is a Shader.md`

## What a Shader Is

Shaders run on the GPU's massively parallel architecture. Where a CPU excels at complex, branching sequential tasks, the GPU is optimized for bulk-processing enormous quantities of data simultaneously via relatively simple operations.

**The sports car vs mega bus analogy:** a CPU is a sports car — fast for advanced branching logic on a small number of items. A GPU is a mega bus — slower per-item, but handles millions of items at once. A contemporary CPU might multi-process hundreds of thousands of data points within a 60fps frame; a GPU handles millions more.

This parallel architecture makes shaders ideal for:
- Coloring every pixel on a 1080p frame (2.07 million pixels) simultaneously
- Updating every particle in a 100,000-particle system in parallel
- Processing vertex positions for complex geometry in one pass

## The Two Core Shader Types

### Vertex Shader

Operates on each **vertex** (point) in a mesh. Handles:
- Transforming vertex positions from 3D world space to 2D screen space
- Passing data (normals, UVs, colors) to the pixel shader stage

A triangle has exactly 3 vertices — 3 yellow-circle points at the corners of the triangle mesh. Those 3 points are the inputs to the vertex shader. Every polygon in a 3D scene is ultimately decomposed into triangles, because the triangle is the simplest primitive with a surface area (3 connected points define a plane; 2 points only define a line).

### Pixel Shader (Fragment Shader)

Operates on each **pixel** (or fragment) of a rendered surface. Produces:
- An RGBA output: Red, Green, Blue, Alpha (4D color value)
- This color contribution is blended into the final framebuffer

The fragment is technically a contribution toward the final pixel color, not always the final color itself (transparent surfaces overlap and blend). HLSL (Microsoft) uses the term "pixel shader"; GLSL (OpenGL) uses "fragment shader" — they refer to the same thing.

The GPU processes pipeline:
```
Geometry → Vertex Shader → Rasterization → Pixel/Fragment Shader → Output
```

The vertex stage runs first (transforms geometry), the pixel stage runs second (colors surfaces).

## How Pixels Are Represented

A pixel is the minimum unit of color on a display — conceptually atomic. Each pixel stores a color value. In the simplest case this is binary: white pixels (all 1s) and black pixels (all 0s). In a color display, each pixel stores red, green, blue, and alpha channel values.

When zoomed in, a pixel-art tree sits in the center of a photorealistic blurred background — this is what happens when a pixel shader renders at low resolution on purpose, sampling colors at a grid of discrete positions rather than continuously. The hard color boundaries are the visible pixel grid.

A zoomed view of letter rendering shows anti-aliasing: the sharp white/black boundary softens to gray intermediate pixels along diagonal edges, reducing the "staircase" artifact (aliasing) that occurs when continuous curves are sampled on a discrete pixel grid.

## Shader Languages

| Language | Full Name | Used With |
|---|---|---|
| **GLSL** | OpenGL Shading Language | OpenGL, WebGL, Vulkan |
| **HLSL** | High-Level Shading Language | DirectX (Microsoft), Unity |
| **WGSL** | WebGPU Shading Language | WebGPU (browser) |
| **MSL** | Metal Shading Language | Apple Metal |

GLSL and HLSL are both C-like. If you know either one, adapting to the other is straightforward — the syntax differences are relatively few. Prior C/C++ knowledge transfers directly; the main adjustment is learning to think in parallel spatial-visual terms rather than sequential imperative terms.

**Minimal GLSL fragment shader** (sets every pixel to solid red):
```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // RGBA: red=1, green=0, blue=0, alpha=1
}
```

## GPU Parallelism vs CPU Sequential Processing

Consider thousands of projectiles in a game:
- **CPU approach:** iterate over every projectile in a loop — one at a time. With dozens of projectiles, fine. With 100,000, each frame's loop stalls all other CPU work at 60Hz.
- **GPU approach:** each projectile is independent of every other projectile (its physics update doesn't depend on other projectiles). Update them **all simultaneously** — one GPU thread per projectile. No ordering dependencies = perfect GPU workload.

This generalizes to pixel shaders: computing the color of pixel (100, 200) doesn't depend on computing the color of pixel (101, 200). The entire framebuffer can be computed in parallel, which is why shaders make 3D rendering fast.

The same insight explains why deep learning runs on GPUs — matrix multiplications have the same structure: each output element can be computed independently from scratch given the inputs.

## Real-Time VFX and Shader Techniques

Common shader techniques in game development:

| Technique | Description |
|---|---|
| **Lit surface shading** | Phong/PBR model: diffuse + specular + ambient based on light direction and surface normal |
| **Vertex displacement** | Animate mesh vertices (water waves, cloth, terrain) via vertex shader |
| **Normal mapping** | Fake high-frequency surface detail with a normal map texture, no extra geometry |
| **Depth blending** | Water edge softness: fade opacity based on depth buffer comparison |
| **Alpha blending** | Transparent surfaces accumulate contributions from multiple overlapping layers |
| **Procedural textures** | Generate patterns mathematically (noise, gradients, fractals) rather than from textures |
| **Post-processing** | Full-screen quad + pixel shader for color grading, bloom, chromatic aberration, etc. |

**Shader Graph** (Unity) and **Material Editor** (Unreal) provide node-based visual shader authoring on top of HLSL, removing the need to write raw shading code for common effects.

## GPGPU: General-Purpose GPU Computing

Because GPUs are powerful parallel processors, their use expanded beyond graphics:
- **Deep learning** — matrix multiplications in neural networks
- **Physics simulation** — particle systems, fluid dynamics
- **Scientific computing** — weather modeling, molecular dynamics
- **Cryptocurrency mining** — hash computation

CUDA (NVIDIA) and OpenCL / SYCL are the primary GPGPU programming APIs. Compute shaders (in GLSL/HLSL) provide GPGPU capabilities within the graphics pipeline without switching APIs.

## Related Topics

- [[gpu-cuda]] — GPU architecture, CUDA kernels, VRAM math
- [[computer-vision]] — GPU-accelerated image processing uses shader-like parallel kernels
- [[generative-models]] — diffusion model inference runs as GPU kernels; output rendered with shaders
- [[3d-vision]] — NeRF and Gaussian Splatting use custom rendering shaders
