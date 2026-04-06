# OpenUSD

OpenUSD (Universal Scene Description) is the scene description and composition system at the core of modern Omniverse workflows. It is not just a 3D file format: it is a layered data model for building, composing, querying, and exchanging complex scenes across tools while preserving hierarchy, metadata, overrides, and non-destructive collaboration.

## Source

- [[raw/05-omniverse/Omniverse.md|raw/05-omniverse/Omniverse.md]]
- [[raw/05-omniverse/01-create-usd-file.py|raw/05-omniverse/01-create-usd-file.py]]
- [[raw/05-omniverse/20-modifying-attributes.py|raw/05-omniverse/20-modifying-attributes.py]]
- [Introduction to USD](https://openusd.org/release/intro.html)
- [OpenUSD API](https://openusd.org/release/api/index.html)

## Core Mental Model

The key concept is the **stage**: the composed scenegraph you work with at runtime. A stage may be assembled from many layers and files, but applications traverse it as one coherent hierarchy of prims and properties.

```python
from pxr import Usd, UsdGeom

stage = Usd.Stage.CreateNew("assets/first_stage.usda")
UsdGeom.Cube.Define(stage, "/cube")
stage.Save()

stage = Usd.Stage.Open("assets/first_stage.usda")
for prim in stage.Traverse():
    print(prim)
```

![A USD stage is the composed runtime view built from one or more contributing layers.](../raw/05-omniverse/images/01-stage.png)

*That distinction matters because most real USD workflows are about composition, not isolated files.*

## Building Blocks

- **Prims:** the scenegraph nodes that represent geometry, transforms, lights, materials, scopes, and more.
- **Attributes:** typed values on prims, including time-sampled data for animation.
- **Relationships:** links between prims, used for bindings, collections, and non-destructive connectivity.
- **Schemas:** standard contracts that define what a prim is or what APIs apply to it.

Common file encodings:

| Extension | Use |
|---|---|
| `.usd` | general container, ASCII or binary |
| `.usda` | human-readable text |
| `.usdc` | compact binary crate format |
| `.usdz` | packaged distribution archive |

## Composition and Value Resolution

OpenUSD is designed around layered opinions:
- `def` defines a prim in a layer
- `over` overrides existing authored data
- `class` provides reusable inherited defaults

That lets multiple teams contribute to one asset or environment without destructive merges. The final value for a property comes from **value resolution**, which evaluates all applicable layers in priority order.

## Why It Became a Hub Format

The practical advantage of OpenUSD is ecosystem reach: it acts as shared 3D infrastructure across DCC tools, CAD/BIM pipelines, renderers, and simulation platforms.

![OpenUSD sits at the center of a wide ecosystem of content, simulation, and design tools.](../raw/05-omniverse/images/02-openusd-ecosystem.png)

*When many tools can exchange structured scene data instead of flattened exports, collaboration gets cheaper and less lossy.*

## Related Topics

- [[omniverse]] — Omniverse uses OpenUSD as its native scene layer
- [[digital-twins]] — digital twins depend on OpenUSD to unify many data sources
- [[3d-vision]] — 3D representations and scene structure intersect with USD workflows
- [[game-math]] — transforms, hierarchy, and spatial reasoning still rest on core geometry
