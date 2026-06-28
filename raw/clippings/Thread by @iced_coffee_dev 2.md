---
title: "Thread by @iced_coffee_dev"
source: "https://x.com/iced_coffee_dev/status/2041164774319292615"
author:
  - "[[@iced_coffee_dev]]"
published: 2026-04-06
created: 2026-04-06
description: "I was just explaining the dot product to my son today! It's used everywhere in games, often with unit vectors to determine how aligned they"
tags:
  - "clippings"
---
**Simon** @iced\_coffee\_dev [2026-04-06](https://x.com/iced_coffee_dev/status/2041164774319292615)

I was just explaining the dot product to my son today! It's used everywhere in games, often with unit vectors to determine how aligned they are.

But if it’s never really clicked for you, this thread is full of visual examples.

![[raw/00-clippings/images/9c853dae0b4e33d6b58e3810b43907ab_MD5.jpg]]

---

**Simon** @iced\_coffee\_dev [2026-04-06](https://x.com/iced_coffee_dev/status/2041164776504480145)

The unit circle is a great starting point, because for a unit vector â with angle θ, cos(θ) is just â.x

Calculating the dot product of â and (1, 0):

dot(â, x̂) = â.x = cos(θ)

![[raw/00-clippings/images/300b330b532c02a5ca517a8c2212d09d_MD5.jpg]]

---

**Simon** @iced\_coffee\_dev [2026-04-06](https://x.com/iced_coffee_dev/status/2041164779214057941)

For any two unit vectors, imagine rotating the whole space so one lines up with the +x direction.

That rotation doesn’t change the angle between them, so we can visually confirm:

dot(â, b̂) = cos(θ)

---

**Simon** @iced\_coffee\_dev [2026-04-06](https://x.com/iced_coffee_dev/status/2041164781399290003)

If the vectors are normalized, the dot product is the signed length of the projection of one vector onto the other:

dot(â, b̂) = cos(θ)

So you get:

• 1 when they’re aligned

• 0 when they’re orthogonal

• -1 when they’re opposite

We'll see why this is useful in the examples.

---

**Simon** @iced\_coffee\_dev [2026-04-06](https://x.com/iced_coffee_dev/status/2041164783886475344)

If b is normalized (b̂), but a isn’t, the dot product becomes the signed shadow length of a onto b̂:

dot(a, b̂) = |a| cos(θ)

We'll see why this is useful in the examples.

---

**Simon** @iced\_coffee\_dev [2026-04-06](https://x.com/iced_coffee_dev/status/2041164786147156163)

Now that we’ve kinda built some intuition, what can you use it for?

Field-of-view checks are dead easy:

dot(fwd̂, toTarget̂) > cos(fov/2)