---
title: "What is a \"Shader\"?"
source: "https://x.com/TheMirzaBeig/status/2011360316920078644"
author:
  - "[[@TheMirzaBeig]]"
published: 2024-09-10
created: 2026-04-06
description: "On the underlying logic and structure of computation, and reality.Shader: a *type* of computer program (set of instructions), for GPUs.Shade..."
tags:
  - "clippings"
---
On the underlying logic and structure of computation, and reality.

**Shader:** a \*type\* of **computer** **program** (set of instructions), for **GPUs**.

- Shade-er; that which **shades**. Shaders were originally about variance of light/dark over some geometric surface (and mostly, still are).
- **\-- Example:** shading the surface of a 3D sphere, lit from some direction.

> [https://mirzabeig.notion.site/learn-shaders](https://mirzabeig.notion.site/learn-shaders)

> Sep 10, 2024
> 
> Paopu fruit w/ realtime shaders. > from Kingdom Hearts. I'm not sure how this \[fictional\] thing would taste or what would happen after. Maybe you think you can 'glide' off the balcony like Sora.

**What they’re used for:** as programs that run on GPUs, shaders handle tasks requiring high-performance, parallel computation → processing lots of data at the same time \[via relatively more simple operations\], rather than in sequence -- and mostly in relation to visual/graphics rendering (generic use is possible).

- Originally specific to graphics-oriented tasks, the parallel architecture is useful for other things → [generic simultaneous data processing (GPGPU).](https://x.com/TheMirzaBeig/status/1777471553539633218)

While CPUs excel at complex, branching/sprawling sequential tasks, GPUs are optimized for bulk-processing entire frames of data. Shaders allow you to program what exactly this processing is for every point of data, via a description of the operations at that stage of processing (the programmed instruction set).

> Dec 19, 2024
> 
> To this day, I rarely use VFX Graph. Shuriken is my go-to for 'traditional' VFX. VFX Graph is it's own thing, +it's unique. Shuriken is typically ruled out @ big numbers and GPGPU, but even then it can be a very handy tool. Example: 'Star Ocean', I made this ~6yrs ago!

> Apr 7, 2023
> 
> float2 n,q,u=float2(i.uv-.5); float d = dot(u,u),s=9,t=\_Time.y,o,j; for (float2x2 m=RM2D(5);j++<16;) { u = mul(m,u);n = mul(m,n); q = u\*s+t\*4+sin(t\*4-d\*6)\*0.8+j+n; o += dot(cos(q)/s, float2(2,2)); n -= sin(q); s \*= 1.2; } return o; #Unity3D #GLSL #VFXFriday

👆 In these examples, I am using a mix of different types of shaders. Different (sub-)types of shaders are used for different types of data.

- **Pixel shader**: operates per-pixel, as data.
- **Vertex shader:** operate per-vertex, as data.

> May 17, 2023
> 
> I should make a pro version with more features, although it's already easy to modify to get all kinds of effects.

One of the most popular methods of rendering 3D computer graphics is via [polygonal modelling](https://en.wikipedia.org/wiki/Polygonal_modeling), which represents any objects of visual shape as a mesh.

- Points, connected by lines--the enclosed area can be shaded/coloured-in.

'Pixel' shaders are the most common type of shader.

- They shade some surface, per-pixel.

> Mar 18, 2025
> 
> Unexpected- the hologram shader has procedural intersection particles, so enabling the wireframe shell creates: COSMIC SPACE DEER.

👆 The deer mesh vertices/points are processed by a vertex shader (program) which transforms and configures the data of underlying geometry (of things to be rendered/simulated/displayed), while the pixel shader does the -actual- shading/colouring of geometry/surface after. GPUs have stages of data processing, where the vertex stage is before the surface shading stage.

After all, you minimally need a triangle for there to be a **polygonal** surface.

- 3x points, connected, bounding/defining some surface area. Even quadr-angles (rectangles, squares) can be decomposed into two tri-angles.

![[raw/00-clippings/images/8be73bab53974918980e4fdaddac5adc_MD5.png]]

Hint: it's -not- a square.

With more data points, we can (re-)present [a complex form, like a deer](https://x.com/TheMirzaBeig/status/1901248692738232515). Each vertex is essentially just a point (in our case, in 3D space, XYZ).

It's a fancy version of connecting dots in some order, then colouring in the area of the enclosed surface -- ultimately as a triangle → which is the most simple geometric surface primitive (some area/face, enclosed by 3x connected points).

- Pure points and lines do not have surfaces, they are conceptual.

In the example below, the vertices of the water (the mesh, triangles) are handled by a vertex shader (operating on the vertex points, as data), while the pixel shader handles 'shading' (colouring) in the surface (area) between the points

> Jan 15
> 
> Shader Graph + HLSL water. Bedtime experimenting. ~100 lines of code. Default plane, +2 tiling and scrolling normal maps, depth blending, distortion, colours. Auto-tiling -> instant ocean. #unity3d #gamedev

So that, you see a shaded (filled-in, coloured) mesh (made of vertices, triangles).

The water pixel shader renders the surface of the plane as if whatever is behind is submerged under water. It's using data and information from a some setup that simulates an eye or camera 'seeing' with perspective vision, rendering.

> Jan 6
> 
> Cosmic water, gyrating particles + grid warp.

👆 You can see the animation of the vertex mesh/grid (by a vertex shader).

Interactive media is interactive simulation of data. Data, that is subject to re-arrangement, and processing -- circumstantial to some agent input/play.

- Evolving, informing, changing values

> Nov 28, 2021
> 
> JUICE! JUICE! JUICE! Added SFX + VFX for various actions, synced haptics, screenshake, and more! There's an underlying event system/pattern that makes it easy to hook up all kinds of effects. #gamedev #indiedev #unity3d #madewithunity #vfx #screenshotsaturday #gamedevs

👆 Every projectile is a point particle, some tracked position in space.

Each is simulated using math/logic, processing the point (position) representing the projectile as a 'physics'-based, logical identity. Some number of times per second, there is a new frame of data: results of the prior frame's operations.

Given that there are not that many bullets (a few dozen, not thousands or more), the CPU is perfectly capable of handling/processing the projectiles in a loop.

- Every 'tick' (frame update, rate), every projectile has its position-state iterated over via physics/math operations that change it over time.

> Jun 4, 2023
> 
> #unity3d #realtimevfx #gamedev #indiedev #vfx

If I did have thousands or more projectiles, then it could lag the CPU; stalling to complete the massively-iterating loop + calculations for each one before moving on to other items, all within a single frame update for the game, never mind 60x ticks per second. In such a case, parallel processing could be considered. Since each projectile is agnostic to others, it would not be an issue to simply update them simultaneously. We don't need to know anything about other projectiles to update any one of them (similar to colour pixels as data).

- Thus, it's possible to process them simultaneously, rather than in sequence, even with CPUs. But- CPUs are not as good at parallel processing as GPUs.

Below, the points of the tessellated (sub-divided, high-resolution mesh) and individual surface particles are updated by parallel GPU operations/processing.

> Jan 11
> 
> Sub-surface wave motion, gyrating particles.

> Jan 12
> 
> Galaxy Water, for Unity 6 (URP). Released, on GitHub. Enjoy! Open source, FREE (+for commercial use). https://github.com/MirzaBeig/Galaxy-Water… #gamedev #indiedev #unity3d #vfx

👆 With some more work: the final result - with all components and parts.

Can a CPU do (process/calculate) practically everything the GPU can? **Yes.** Is it going to be better at it, or about the same in all cases? **No.**

If some contemporary CPU can multi-process hundreds of thousands of data points without dropping the FPS below 60fps, a GPU may be able to handle millions more, still. The downside is that GPUs are slower per-processing.

So, do you want a sports car calculating advanced, branching logic? Or, do you want a mega bus handling loads of data, via simpler operations?

- It's not that case one renders the other unnecessary or redundant.

Pixel shaders are also known as 'fragment' shaders, and vice-versa. They mean and refer to the exact same type of shader, which operates per some irreducible, 'minimum unit of colour' as a data point, [conceptually atomic](https://x.com/TheMirzaBeig/status/1955981782521708598) for some purpose.

As such, you control the appearance, down to the smallest 'bit' of colour. You can get creative, producing stylized outputs, variations, and remixes:

> Nov 22, 2024
> 
> Another year! My experience so far... 11 years of #Unity3D. 13 years of #RealtimeVFX. 14 years of #GameDev. 16+ years of programming, #Photoshop (Graphics Design), #AfterEffects (Motion Graphics), and audio production. Through the years: HTML 4, ActionScript 2/3, PS, Vegas,

> Aug 29, 2024
> 
> Colourful sketch/drawn energy shader. The outlines resemble the from 'Wish' (2023). This is all from various configs of the same shader-- Featuring multiple 'layers' (of hulls), so I can mix the results of various parameters realtime in #Unity3D. #gamedev #realtimevfx

The output of this type of shader is a 4D colour value: > 🟥 red, 🟩 green, 🟦 blue, and 🔳 alpha (RGB, and A).

'Fragment' is technically more accurate if you understand the nuances.

- Microsoft's HLSL uses the term 'pixel shader', while GLSL uses the term 'fragment shader'.

\-- It simply means the output of this type of shader is \[merely\] a contribution towards the actual final colour of some point of colour data (aka: some 'pixel'), and doesn't \*necessarily\* decide it exactly (though, it may).

Note the layers and overlap, with some transparent blending:

> Jan 10, 2025
> 
> Everything you see: from the particles, trails, outlines, fire, energy field, flamethrower, etc... is ONE shader (for Unity's URP) - and it's available now.

There's no such typical thing as 'alpha' for hardware screen pixels, but that alpha channel value may be used to blend several layers of transparent surfaces as represented by the software-digital simulation, computer program.

\[**IMAGE:** lit 3D sphere, or Unity + Shader Graph, and/or HLSL...\]

Shaders are typically written in **GLSL**, and **HLSL** (programming languages).

- **GLSL** \= OpenGL \['GL' = graphics library\] shading language. **HLSL** \= \[Microsoft's\] high-level shading language.

Both are C-like (C is a programming language for CPUs). Being similar, if you know either GLSL or HLSL, then you know the other for many practical cases.

If you know C/C++, you're likely already GLSL/HLSL adept, though you may still need to (re-)orient yourself to parallel spatial-visual thinking, and computation.

- If you speak Urdu, you speak Hindi. If you speak Hindi, you speak Urdu. > **Meaning:** there are differences, but relatively few \[to each other\].

**Language:** a system of communication, information exchange. **System:** some network of relationships/correlations, by function.

If you [copy-paste the code below and run/compile it on ShaderToy](https://www.shadertoy.com/new), it will set the output viewport to solid red. Entirely, and fully red:

```glsl
// A complete, basic/minimal shader (function).
// It sets the 'r' (red) value of the output to 1.0.

void mainImage(out vec4 outputPixelColour, in vec2 inputPixelCoordinate)
{
    outputPixelColour.r = 1.0;
}
```

![[raw/00-clippings/images/ac7af0c7645b5d61f2f79f1f01c72049_MD5.jpg]]

The code runs for every pixel of the output viewport on the left.

\> that is 630 x 354 (223,020) places on \*my\* screen, computing.

Try setting the value of 'r' to 0.5 -> half the intensity, brightness.

Now, try 🔴 outputPixelColour.r = fract(iTime);

- iTime -> time in seconds since execution of the shader program. -- it is some variable simply available to you when you use ShaderToy.
- [fract](https://registry.khronos.org/OpenGL-Refpages/gl4/html/fract.xhtml) -> a built-in GLSL function that returns only the fractional (decimal) part of some input value. It essentially removes the integer/whole part.

So that, fract(**3**.145967) would return a value of **0**.145967. > the result is a continuously looping value between 0.0 and 1.0 exactly.

<video preload="auto" tabindex="-1" playsinline="" aria-label="Embedded video" poster="https://pbs.twimg.com/tweet_video_thumb/G_GyA41WMAAPqxB.jpg" src="https://video.twimg.com/tweet_video/G_GyA41WMAAPqxB.mp4" type="video/mp4" style="width: 100%; height: 100%; position: absolute; background-color: black; top: 0%; left: 0%; transform: rotate(0deg) scale(1.005);"></video>

![[raw/00-clippings/images/f7ac8d734b8bd2440d78bf54dfdc3d41_MD5.jpg]]

GIF

A ~5.0s, black -> red GPU animation \[1800 x 1013 pixels\].

Note: decimal part of the timer correlates to the 'shading' (colour).

You can also develop/program shaders visually, using node-based editors, tools, and workflows. This has advantages and disadvantages: shaders are inherently visual, and much of what you do may be simple operations (actual, basic math).

- Addition, subtraction, multiplication, division, exponentials...

Authoring and editing shaders with nodes is intuitive (more so than for 'regular' programming), but severely limiting for complex effects, logic, and operations.

\[**IMAGE:** visual shader tool(s) SG, ASE, Blender?\]

> Dec 15, 2025
> 
> Basic 2D outline Shader Graph for Unity. #unity3d #gamedev #indiedev

What you can write in a few lines of code may require some obtuse visual circuitry. Fortunately, there are hybrid systems which allow you to create arbitrary nodes with your own code, bringing the actual best of both.

> Jan 7, 2025
> 
> Procedural smoke/fire/wave offset Shader Graph. Nodes + custom function code for Unity. Give it a hand-drawn or animated style by posterizing the phase (time) input: see for more.

> Jan 7, 2025
> 
> For the hardcore, node-only enthusiasts.

**GPU (Graphics Processing Unit):** the part of your computer designed for spatial-visual, and rendering tasks, which benefit from [parallelized architecture](https://en.wikipedia.org/wiki/Parallel_computing).

Even before programmable GPUs, the parallel architecture uniquely accelerated, 'solved' the computation necessary for every place (pixel) on your screen.

**Computer:** that which computes, processes data -- determining by calculation. **Program:** any set of instruction (direction, order), to be processed/executed/run.

A computer program 'function' is any purpose/task-related set of instructions, which (in most programming languages) you can define as a separate body.

- Just as your eyes, ears, tongue, heart, and brain all serve various functions -- you can define in computer programming some separate block of coding.

> Jul 26, 2022
> 
> #UnityTips: Nesting Coroutines : You can wait on the return of any number of coroutines \*within\* a coroutine. It's a -SIMPLE & CLEAN- way to chain multiple self-contained functions. Especially useful for proc. animation and state transitions (ex: for AI). #unity3d #gamedev

**Graphics:** visual images, related to observation/interaction via eyes.

- Circumstantial to sight/seeing, via our 'natural' → biological optical sensors.
- **Natural:** whatever is not 'artificial' → not the result of human design.

('natural' seems to refer to what exists via apparently self-sufficient, objective, independent -> design, invention, creation, function, purpose, and reason.)

**Biology:** the science(s) of living organisms, \[locally\] self-sustaining, naturally animated machines (\*not\* of human origin, will, design, or creation).

- We have models of understanding about such things, as per biology.
- Our methodological studies and investigations into bodily life, systems.

Programming languages are systems of communication with programmable computers. You are able to order/arrange/queue/list a series or set of logical operations/instructions, via some grammar/syntax/structure which delineates what is and is not valid instruction, as per the language's rules.

- You communicate the configuration of processing and calculations. (and **all** \[digital, or otherwise\] operations concern values, data).

> Apr 10, 2024
> 
> Update for the artificial life (boids) repo. Agents steer in a sea of reactive 'bioluminescent' particles. Groups of boids form sub-flocks, which generate force fields proportional to their mass. Bigger swarms -> larger force field radius and push. (still working on source

**Data:** any differentiated/discerned state, to the smallest possible 'bit'.

- **Binary:** where a bit is either '0', or '1'.
- True, or false. [Waves, and fluctuations...](https://x.com/TheMirzaBeig/status/2010541712457031925)

> Mar 13, 2024
> 
> I've open-sourced my interactive GPU wave sim on GitHub. If I have time I'll come up with some more interesting examples. https://github.com/MirzaBeig/Wave-Simulator… Shader Graph used for rendering, so you can easily preview the output and see how channels are mapped. #unity3d #gamedev

**Information:** that which informs (instances fact); delineates, shapes, forms.

- **Inform:** tell, mean, convey \[some fact, truth, state, reality\].
- Inform-ation is \[fact, truth, state, reality\] which is told, meant, conveyed.

> Jul 4, 2025
> 
> ~Colour Palette from Texture~ -- Extracting colour information from an image: Downsample and/or quantize to reduce noise and increase performance. You can get a roughly approximated palette from this step alone. Hash/key pixels by their quantized integer colour

Thus, all data is information, and all information is (made up of, and from-) data.

- Data is some atomic element of information, some distinct fact-state. -- atoms -> molecules, letters -> words -> sentences, etc...
- It is altogether some conceptual atom, or unit that is a state.

We are able to identify some logical universe, some intelligible reality. > Apparently made up of processed states/particles, understood as 'data'.

- Contingent states, elements; subject to conditioning ('laws', 'forces').

Atomic values of being, composed specifically into more complex things.

- So that: we observe functional states, systems, relations, direction, order.

> Jun 20, 2025
> 
> Grid-emit module for Unity's particle system. #unity3d #gamedev

> Jan 5, 2025
> 
> An advantage to using particle systems is that you can control the spawning and behaviours for things like butterflies (and fish, birds...) easily. Vertex streams allow for properties to be read/used in the shader. Example: Random offsets for flapping wings, per-butterfly.

**CPU (Central Processing Unit):** the part of your computer designed to be the main processor, essential to its overall fundamental operation, and what it is → a computer that processes, calculates, accounts, executes.

**Processor:** a \[hardware\] 'processor' is the electronic component in a computer that executes instructions, which are reducible to arrangements and sequences of meaningful binary data (1s and 0s), corresponding to on/off electrical signals within the processor's circuitry, representing meaningful logical operations.

- It does work. It's a digital, conceptual machine, circumstantial to the physical. > Some digital world/space, fully circumstantial to minds \[for values, data\].

Where, 'hardware' is any physical construct of some design; tools, machinery.

> Aug 13, 2023
> 
> Unity's Job system allows compute/shader-like operations on an array of data, like particles. ALL on the CPU (i9 13900KF). Here I'm tile-warping (looping) 100,000 rain particles inside a volume that also applies a smoothed-out distance field for colour and scale

Different types of processors, such as CPUs and GPUs, are designed with various architectures (the structure and design of a system’s components) that make them more (or less) suitable for specific tasks, purposes.

- GPUs in particular excel at **parallel** **processing**, where the same set of logical instructions (some programming, about operations of data), are executed with input/incoming/streaming data as variables, parameters.
- Useful for rendering graphics (computer-processed visuals, drawings, images) on modern displays, as the calculations required to colour, or 'shade' each pixel on the screen can be handled simultaneously.

💡 **Why this is important:** Consider that for display resolutions ranging from full HD 1920x1080 monitors to a typical ‘4k’ (UHD 3840 x 2160) screen, that’s **2-8 million** pixels (aka places on your screen that need rendering calculations).

In realtime 3D apps like video games, this involves the processing of geometry (shapes, subject to dimensions and bounds, context), dynamic lighting, and many other things at 30 - 60 (frames) per second, or **more.**

> Oct 28, 2023
> 
> Stylized particles to match my trail shader. Textureless, these particles are rendered entirely using SDF math and quantized animation + motion. #screenshotsaturday #unity3d #vfx #gamedev

The paradigm of shaders and parallel processing is that the operations are executed/run for every point/element/atom of data simultaneously.

- Some data value, or bit of information is generated, and/or transformed.

Whether that is many points and vertices, or some frame of pixels and colours:

> Jan 10
> 
> Cosmic waters, but only the particles...

**Pixel:** the smallest possible unit of shading, or colour \[as a state, data\].

Your screen is made up of physical pixels -> some programmable/addressable light-emitting matrix, typically as RGB (red, green, blue) modulation, values.

- You can set the colour of individual pixels on your screen, ~exactly.

> Jan 29, 2025
> 
> Some technical insight into CRTs: CRT monitors are analogue displays and unlike the case with real pixels, there's no discrete or logical circuitry (addressable matrix) behind the coloured 'subpixels' - they are a passive component of the machine. This also means the

**Light:** visible radiation, as 'excitation' of the electromagnetic field/volume.

- Radiating amplitudes of the field, with some frequency. \*\*Light -is- the electromagnetic field, excited and perturbed -- like waves of water.

\*\* Though, this is only -a- model of understanding about the mechanisms of the universe. It is not necessarily exact, as a future explanation may be sufficiently and similarly useful (at least, contextually).

> Jul 16, 2025
> 
> memorize this for GLASS~ TransformDirection\_WorldToViewSpace( refract(cameraToVertexDir, vertexNormal, 1.0 / 1.54)); You're calculating the refraction offset vector based on the incident angle (from the incoming ray to the surface, which is camera -> the vertex or

It may also be useful to mention **sound** (because of related concepts): which is audible radiation, as excitation of physical pressure waves (air, water, wood...).

- We need 'eyes' to perceive light, and 'ears' to perceive sound → some instruments/tools designed for the corresponding data type/form/medium.

> Jan 27, 2021
> 
> Immersion and presence SKYROCKET with realtime GI and physics-based sound propagation (play w/ audio) in #Unity3D. #GameDev

**Eyes, Cameras:** some hardware that is able to 'see'. > Perceive, observe, intake, pre-process, funnel) visual images.

- Both natural biological eyes and artificial technological cameras share similar concepts and features in their design and make-up. They are both circumstantial to a shared, objective universe/reality (to either), where that's how things work and are. So, to create anything like eyes and cameras (and for similar purposes), you will end up creating something exactly like them.
- \-- Sensors, photoreceptors, lenses, etc.

**Image:** any frame/window of data, typically understood to be visual. Related to the word, **"texture"**: an image of some variance, 'shading'.

- Visual → relating to **vision:** eyes, seeing, light-based perception.

<video preload="none" tabindex="-1" playsinline="" aria-label="Embedded video" poster="https://pbs.twimg.com/amplify_video_thumb/2013589134309203968/img/FalFB2cKrCiWeQEA.jpg" style="width: 100%; height: 100%; position: absolute; background-color: black; top: 0%; left: 0%; transform: rotate(0deg) scale(1.005);"><source type="video/mp4" src="blob:https://x.com/20dfc376-4000-4e73-a2ec-6567927b740b"></video>

![[raw/00-clippings/images/baba46c0649e1b575f522ac8e335597f_MD5.jpg]]

An image, made of discrete points/samples of data.

Depth, distance to surfaces encoded as red-green colour.

**Photons:** the minimal data of light, as atoms are the data of matter.

- You may think of pixels as 'digital photons' (or conceptual atoms, of colour).

> Jul 16, 2024
> 
> Light Caustics: These prismatic visuals form when light folds and crosses itself, redirected by surfaces and changes in transmission. By simulating light as photons and rays, we can render caustics as refraction-projected particles. #unity3d #gamedev #realtimevfx

**Colour:** perceptual label, referring to the -experience- of observing and recognizing wavelengths of light as \[for example--\] red, blue, and green...

A 64 x 64 pixel resolution image is 4,096 pixels in total. > 64 pixels in width (x-axis), 64 pixels in height (y-axis).

A 128 x 128 pixel resolution image is 16,384 pixels (4 x 4,096).

**If:** you double the resolution from 64^2 to 128^2, **then:** that's 4x the number of pixels -> **square-cube law.**

- By 1024 x 1024, we have **over 1 million pixels; units of -possible- colours.**

(thus,) -- **Colours** and **pixels** are the atomics of visual rendering.

**Consider the image below--**

![[raw/00-clippings/images/e989134bce87e8ada17d86af95832be4_MD5.png]]

Literal pixel art, a simple outdoor scene.

\-- 64 x 64px, scaled to 1024 x 1024.

It is some frame of discrete data, (rather than continuous function/values). Literally, individual units of separate, distinct colours, which are the pixels.

- 64 x 64 pixels, with an actual data resolution of 1024 x 1024. > there are 16 actual texture pixels in each cell (1024 / 64).
- It is 'realized', sampled, observed, interacted-with.

I had created this image as a block of 64 x 64 pixels, then expanded it 16x to 1024 so that I could draw some visible/visual grid → to explain visual concepts.

- This makes the image \*appear\* to be made of 64 x 64 blocks.
- The actual resolution of data for the texture is 1024^2, and there are 16px blocks of the same colour, as if they were discrete units (of data points).

It is some 'texture', because there is variation over the data frame.

<video preload="none" tabindex="-1" playsinline="" aria-label="Embedded video" poster="https://pbs.twimg.com/amplify_video_thumb/2013590576667496449/img/Q4SrLRuEMHRKsvXC.jpg" style="width: 100%; height: 100%; position: absolute; background-color: black; top: 0%; left: 0%; transform: rotate(0deg) scale(1.005);"><source type="video/mp4" src="blob:https://x.com/d620e7c7-da0e-4a5c-a745-a507343034b2"></video>

![[raw/00-clippings/images/474550114571457b2a048cbb8c91effd_MD5.jpg]]

Zooming into the 1024 x 1024 image (of 64 x 64 colour blocks).

\> each pseudo-pixel block is \*actually\* 16 x 16px (of one colour).

![[raw/00-clippings/images/1004d463c6a72e0b5b691a9c921d5330_MD5.png]]

10 x 8 close-up of the individual units/blocks/pixels/data of colour.

You are able to differentiate \*composite\* information from data:

\> red fruit, green tree, and blue sky -- shaded, coloured.

\-- You isolate the red apples/fruits 🍎, from the backdrop of the green tree 🌳 bush/leaves, which is itself differentiated from the sky, which has the sun ☀️, causing the tree to be lit directionally 🔦, casting a shadow over the green field/land/ground 🌅. **You are able to discern all of this** **inform-ation.**

- [I like to use emojis](https://www.reddit.com/r/Unity3D/comments/1lzik96/comment/n35zyc1/) | useful for organization, rapid identification/tracking. > Be prepared to see more of them, where/when deemed appropriate :)

> Dec 30, 2025
> 
> Simple 2D outline shader for Unity 6, URP: I've made the repository + source public. Do whatever you'd like with it! > https://github.com/MirzaBeig/2D-Outlines… #gamedev #indiedev #unity3d

Our perception, knowing, understanding, is circumstantial/subjective. Just as LLMs must be trained, guided, aligned to interpret, understand.

- It is altogether some objective reality, to a circumstantial self.

We begin with **nothing** (circumstantial to a mind-scenario).

- A **point** is some existence, presence, value, data, atom.
- A **line** is some correlation, connection, path.
- A **triangle** is the first complete shape, surface. > 3 points, connected by lines → area, bounds.

Each vertex is essentially just a point (in our case, in 3D space, XYZ). If we connect the points with lines, we observer some bounded, enclosed form:

> Jun 19, 2024
> 
> ~5 years later, I've written a #Unity3D tutorial. Particle Plexus, Part 3 (Triangles) is now ready! Read it here (w/source code): https://mirzabeig.substack.com/p/unity-tutorial-particle-plexus-part-3… #indiedev #gamedev #realtimevfx

You only know what is real, that is your **experience**. If: you are not the certain experience of self-sufficiency, then: you are subject to some objective reality.

What \*is\* certain: there exists some altogether intelligible reality, universe. What \*is not\* certain: the exact mechanisms, operations of the universe.

Yet, we've found many uses about those mechanisms. We describe them via models of understanding, [circumstantial to our scientific investigations.](https://x.com/TheMirzaBeig/status/2006948835793195381)

> Dec 31, 2025
> 
> Interactive gravitational lensing, w/ 4D space-time recording.

> Dec 22, 2025
> 
> Gravitational field layers/fabric visualization.

We find that our (which I say, assuming by my own-) experience of reality is that we are subject to some stream of data frames (facts, which are- as per our experience of them), by which we may intend and act. It is informing to us.

Bits of information, subject to some **underlying** **qualifiers, objective to us. >** Else, our experience of identification of a triangle is entirely self-sufficient.

- Is your knowledge of triangles without any context, beyond your own self?

Our experience of knowing, understanding: -- is points and lines. A network.

Facts, and correlations. Things, and relationships.

> Nov 23, 2025
> 
> I've been using #Unity3D for 12 years. I'm using Blender's GeoNodes for a procedural mesh that's realtime-animated with a custom shader in Unity. ---(reminiscing, reflection follows)-- At some point, you realize it's 'all' states, relationships, and data/information.

\[models of-\] Understanding, and intention/intending thereby. > We intend by information and desires/wants/feelings/needs.

And we apparently inhabit this data-processing (of some bit-rate, and throughput), sensory machine-body made up of highly specific, functional units that we correlate about. It's as if we're tethered to it, while it functions. We're thus situated within some animated universe, where \[sign\]als (having direction, fluctuation) are propagating data, which we described as waves and particles.

> Jul 30, 2025
> 
> Photon -> caustics projection. Gathers energy from the refracted rays. (caustics are the folding, overlap, concentration, and dispersion of light energy/radiation - and that's what is happening here, based on the actual wave simulation) #unity3d #gamedev #realtimevfx

**Signal:** a sign, some minimum direction that may even be considered.

**Frequency:** is is the repetition of the sign\[al\], > the periodicity of differentiation, fluctuation, state.

**Amplitude:** is the intensity, strength of it.

The fluctuation of night and day is a literal signal, of some frequency, and clear amplitude as a fact which we experience (that it is observed, alternating).

A lamp is a source of light. Light data is radiation of the electromagnetic field; it is some amplitude of that field as a generated signal, and interacts with the universe, being modulated. Our bodies, being some situated intake of this data, have various organs to decode the most subtle fluctuations/data about the universe, in specific formats and channels: seeing, hearing, smelling, and so on.

Light sources are additive, and emit various frequencies, creating a signal.

> Jul 20, 2025
> 
> Seamless 360° \[no-scope\] monkey caustics.

> Jan 17
> 
> Late night natural waves experiment. Two additive layers of Gerstner/Trochoidal waves. The start of an ocean shader? #unity3d #gamedev

What we perceive as "white" is the sum of various frequencies, while "black" is perceived absence of amplitude - relative to some range of frequencies [our bodies are naturally equipped to monitor/receive/read/intake.](https://x.com/TheMirzaBeig/status/1986324673764671613)

If we subtract from this signal the higher range, we get 🔴 ("red"). If we subtract from the lower range we get 🔵 ("blue"). Subtracting from the lower and higher ranges, but leaving some middle range, we get 🟢 ("green").

> Jul 26, 2025
> 
> Unity stained glass caustics test.

Where some data is modified, such as pure light being negatively imprinted, and distorted by other 'things' (discrete presences, of features and qualities).

- Example: materials absorb and reflect energy.

So for light, we eventually receive some frame/image of differentiation.

Within some texture, we may identify data and information.

- Even if it's tactile, like pressing your hands against a flat surface, with a coin. You can feel the impression of the coin as some frame of differentiated data.
- Or, you could see it, distinct from what is is contextual to.

You can convey some environment, rendering what is visual as auditory.

\-- You can **re-format, re-mix reality**.

Same facts/data and information, rendered and presented in different ways.

> Jul 28, 2024
> 
> This roughly simulates PS1-style rendering. Something about this aesthetic makes me want to make a little retro-game, pushed further \[creatively\] with modern rendering/shaders/lighting. https://x.com/TheMirzaBeig/status/1462518400954032129…

> Jul 30, 2024
> 
> Lit realtime caustics.

> Aug 15, 2024
> 
> Excellent question. \[\] And you mostly answered it! Anyone up for some useful knowledge? HRTF = Head-Related Transfer Function. Your head is a filter for sound, including the shape of your ears. (your entire form , actually...) It's why you sound different when you

Just as well, there exists that which is naturally beyond our perception, out of range in some way. Data and information about it is typically invisible to us.

Of both sound and light — and who knows what else? 🔊👀

- Hence, we map infra-red and ultra-violet into range to be able to see that 'light' beyond our natural visual senses. We could also just look at the underlying data, numbers, values -- or even hear it, if dictated/audible.
- They all represent the same reality, in different ways/formats we do not experience (or are even particularly aware of, in many cases).

🔴 → the lowest frequencies of electromagnetic radiation \[of visible range\].

- It is some amplitude, excitation of that field as a 'medium' that apparently propagates. Our eyes have many individual photo-receptor units (bio-cells) that are sensitive to different ranges of frequencies of EM radiation:
- 🔴🟢🔵 -- which we perceive and label, as minds experiencing colour.

🟡🟢 → somewhere in the middle of the range of human-visible frequencies. 🔵🟣 → among the highest frequencies of EM signals we can naturally see.

> Mar 25, 2021
> 
> I can sample the precalculated ("baked") lighting in the scene. Using the luminance of the pixel/colour I sample below the character with a raycast, I adjust the opacity of the shadow "realistically" so it's more visible near lit areas, but fades near dark. #Unity3D #GameDev #VFX

If we want to naturally perceive some vision about that which is below-red (infra) or extreme-violet (ultra), we need to re-map the data/signals, bringing them into some actual visible range, **for \*****our\*** **eyes, seeing, and vision.**

Below, we find a visual binary, where each data is a 'bit' (white, or black).

- 1.0, or 0.0.

![[raw/00-clippings/images/d32137bd887169b49f935d5cffe3f464_MD5.png]]

While this image is of a much greater data resolution,

there are exactly only two 'points' of colour, shading.

If our frame were only white, or black, then there would be nothing to distinguish. No black from white, or vice-versa -- within the same frame.

If you were to view the above image with a perfectly white or black background, one side may 'disappear', as it camouflages against some context.

![[raw/00-clippings/images/3bf73bedca6d0f5d790b48bfc9ce8d45_MD5.png]]

Ignoring text/lines, this is an example of minimal distinction.

\-- two discrete/separate "pixels" \[white, black\], data/contrast.

Had it been some frame without any distinction \*even possible\*, there would be no-thing except as reference to some objective context: such as a fully black image, embedded on some website, itself on Earth, the Solar System...

- Else, how would you call it 'black'? There would be no logical identity even possible to discern, without distinguishing some features/qualities.
- 100% congenitally blind humans have no concept of "black", or "white".

![[raw/00-clippings/images/05c99228141636ef334373e470387dfa_MD5.png]]

Close-up of the 'K' in "Black", made up of many pixels/states/bits.

A literal 2-pixel image, frame of data -- with exactly and only two actual points of data, colour, differentiation, states) can be used for the binary white/black texture. However, to render complex logical, multi-feature/point identities like text data/information, we need more pixels and more complex discerning.

It is the same case for both:

\- points as **position data** (vertices, data as some point state in space), - and points as **visual data** (pixels, data as some shaded/colour contrast).

> Aug 17, 2024
> 
> A recurring critique I am receiving is that this doesn't exactly match the output of the #PS1 console. I've further added these very retro visuals: - Pseudo-volumetric, procedural cone spotlights. - 100% HLSL caustics, fog, water, and soft particles. - Configurable

> Dec 19, 2021
> 
> Testing distance-based wave tessellation on a simple water shader in Unity. Lit, fully tileable, and features depth fog + blur. No textures, all on the GPU. #unity3d #madewithunity #gamedev #gamedevelopment #gameart #indiedev #shader #vfx

You cannot define 'true' nothing, except by absence of all \[even\] possible being. Yet -- [such a total nothing is always imagined contextual to something](https://www.reddit.com/r/Metaphysics/comments/1pk0s93/what_is_nothing/). It is not possible as a state of being, because some existence is definitively self-sufficient.

- Some altogether objective, independent reality.

Since we're laying down our foundations, I'll even define 'art':

> Jan 11
> 
> Some post-processing, and now it's my banner. It's funny how this started. On a whim at night, inspired by re-post of a similar effect in Blender, by @80Level. Tomorrow (-ish), it goes on GitHub.

> Aug 27, 2024
> 
> 1 week later: Tech-art is a nice 'break' from the dredge of typical (non-artistic) programming work. Here's how my 'shield bubble' turned out! (see for progress shots) #unity3d #realtimevfx #gamedev

**Art:** synthesis, remixing, combination of data states to produce novel content for some aesthetic (design appreciation, beauty), evocative, or emotive purpose.

✨ Shaders and programming are \[about, related to-\] **technical art**.

- A fusion of the domains of arts/aesthetic, and the underlying sciences/technology.

<video preload="auto" tabindex="-1" playsinline="" aria-label="Embedded video" poster="https://pbs.twimg.com/tweet_video_thumb/G_JWHcgWgAADm2x.jpg" src="https://video.twimg.com/tweet_video/G_JWHcgWgAADm2x.mp4" type="video/mp4" style="width: 100%; height: 100%; position: absolute; background-color: black; top: 0%; left: 0%; transform: rotate(0deg) scale(1.005);"></video>

![[raw/00-clippings/images/0ee0567b6841628ecf2d3fc510b2b7b7_MD5.jpg]]

GIF

Particles physics, shaders, traditional hand-drawn art, etc.

It concerns a wider, more cross-domain body of knowledge and understanding than just the traditional artistic and technical aspects -> \*greater than the sum.

- \* If you're able to flow between the domains, realizing how they correlate.

**Welcome to the exciting world of simulations and interactive media!** 🎉

> Aug 23, 2024
> 
> This is going well. It's just missing some caustics!

> Aug 5, 2024
> 
> I made this water shader~ Technical art, 'deep' game development, etc. You learn so much about the mechanics of the world in a very real, applied sense. All that theoretical math is put to work, and you can actually see the results (+everything in between). I love it.

## ⚠️ UNDER \*HEAVY\* CONSTRUCTION.

## Learn:

\[started, above\] Definitions, concepts and overview.

\- Basic structure, syntax. - "Hello, world!" shader(s).

\-- Colour, UV, textures, time. - 1D, 2D, 3D... math, rotation.

\--- All of the above can be **one page/resource/article.**

**Easy access, referencing, and starting for beginners.**

One shader, to teach you all. > Water.

\[Glass could work, too?\]

**Basics:**

\- Colour, alpha. - Texture scrolling.

\- Shader Graph, +HLSL.

**Intermediate:**

\- Depth masks.

\- Normal scrolling. - Distortion, refraction. - Vertex wave animation.

\- Edge + wave foam, patterns. - SG lighting (avoid even NdotL).

**Bonus (~importance):**

\- Depth caustics. - Planar reflections. - Buoyancy. - Depth blur. - Volumetrics. - Styling, creative. - Particles.