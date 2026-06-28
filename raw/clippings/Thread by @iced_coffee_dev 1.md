---
title: "Thread by @iced_coffee_dev"
source: "https://x.com/iced_coffee_dev/status/2008978710549155976"
author:
  - "[[@iced_coffee_dev]]"
published: 2026-01-07
created: 2026-04-06
description: "The dot product is used everywhere in games, often with unit vectors to determine how aligned they are. But if it’s never really clicked fo"
tags:
  - "clippings"
---
**Simon** @iced\_coffee\_dev [2026-01-07](https://x.com/iced_coffee_dev/status/2008978710549155976)

The dot product is used everywhere in games, often with unit vectors to determine how aligned they are.

But if it’s never really clicked for you, this thread is full of visual examples.

![[raw/00-clippings/images/e38f7858b9adbcfb2a859a98b248d5f7_MD5.jpg]]

---

**Simon** @iced\_coffee\_dev [2026-01-07](https://x.com/iced_coffee_dev/status/2008978716253462862)

The unit circle is a great starting point, because for a unit vector â with angle θ, cos(θ) is just â.x

Calculating the dot product of â and (1, 0):

dot(â, x̂) = â.x = cos(θ)

![[raw/00-clippings/images/b5a9fa231fa8c99df8948428cf42883c_MD5.jpg]]

---

**Simon** @iced\_coffee\_dev [2026-01-07](https://x.com/iced_coffee_dev/status/2008978767902109864)

For any two unit vectors, imagine rotating the whole space so one lines up with the +x direction.

That rotation doesn’t change the angle between them, so we can visually confirm:

dot(â, b̂) = cos(θ)

---

**Simon** @iced\_coffee\_dev [2026-01-07](https://x.com/iced_coffee_dev/status/2008978769990787241)

If the vectors are normalized, the dot product is the signed length of the projection of one vector onto the other:

dot(â, b̂) = cos(θ)

So you get:

• 1 when they’re aligned

• 0 when they’re orthogonal

• -1 when they’re opposite

We'll see why this is useful in the examples.

---

**Simon** @iced\_coffee\_dev [2026-01-07](https://x.com/iced_coffee_dev/status/2008978772058357793)

If b is normalized (b̂), but a isn’t, the dot product becomes the signed shadow length of a onto b̂:

dot(a, b̂) = |a| cos(θ)

We'll see why this is useful in the examples.

---

**Simon** @iced\_coffee\_dev [2026-01-07](https://x.com/iced_coffee_dev/status/2008978773648265525)

Now that we’ve kinda built some intuition, what can you use it for?

Field-of-view checks are dead easy:

dot(fwd̂, toTarget̂) > cos(fov/2)