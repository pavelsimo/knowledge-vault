---
title: "Thread by @iced_coffee_dev"
source: "https://x.com/iced_coffee_dev/status/2021937953933865395"
author:
  - "[[@iced_coffee_dev]]"
published: 2026-02-12
created: 2026-04-06
description: "Trig shows up everywhere in gamedev, but SOHCAHTOA isn’t that intuitive. Let’s cover what sin/cos are in a way that’s easy to understand, w"
tags:
  - "clippings"
---
**Simon** @iced\_coffee\_dev [2026-02-12](https://x.com/iced_coffee_dev/status/2021937953933865395)

Trig shows up everywhere in gamedev, but SOHCAHTOA isn’t that intuitive.

Let’s cover what sin/cos are in a way that’s easy to understand, with some nice visual examples.

![[raw/00-clippings/images/81cdf1006799665c4a32fc4e7c55e54b_MD5.jpg]]

---

**Simon** @iced\_coffee\_dev [2026-02-12](https://x.com/iced_coffee_dev/status/2021937956010045684)

Let's start with the unit circle, that is, a circle with radius 1.

If you form a right angled triangle from the center to a point on the circle, you guarantee that the hypotenuse of the triangle has a length of 1.

We'll see why this is important next!

![[raw/00-clippings/images/769fe9e3700bad37bd5a007bf16dae55_MD5.jpg]]

---

**Simon** @iced\_coffee\_dev [2026-02-12](https://x.com/iced_coffee_dev/status/2021937958333665338)

We already know:

sin = opposite / hypotenuse

cos = adjacent / hypotenuse

On the unit circle, hypotenuse = 1, so:

sin(θ) = P.y

cos(θ) = P.x

(for point P on the circle)

![[raw/00-clippings/images/5967ded393532831c4fd2a9367c46069_MD5.jpg]]

---

**Simon** @iced\_coffee\_dev [2026-02-12](https://x.com/iced_coffee_dev/status/2021937960455913903)

sin and cos are actually the same wave: cos is just sin shifted by 90° (π/2)

So you can think of them as essentially the same, but starting at different points.

---

**Simon** @iced\_coffee\_dev [2026-02-12](https://x.com/iced_coffee_dev/status/2021937962452152359)

Building a normalized direction vector becomes trivial: (cosθ, sinθ).

---

**Simon** @iced\_coffee\_dev [2026-02-12](https://x.com/iced_coffee_dev/status/2021937964583202982)

And it’s easy to go the other way too. Given a direction vector d̂ = (x, y):

θ = atan2(y, x)

Note: atan2 takes (y, x), and it wraps at ±180° (±π).

![[raw/00-clippings/images/ea56112bb1c1c3d7b7b0a3e3c5ab9389_MD5.jpg]]