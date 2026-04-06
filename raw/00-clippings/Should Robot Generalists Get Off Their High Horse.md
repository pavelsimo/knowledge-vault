---
title: "Should Robot Generalists Get Off Their High Horse?"
source: "https://x.com/AnneliesGamble/status/2033954294614098160"
author:
  - "[[@AnneliesGamble]]"
published: 2026-03-17
created: 2026-04-06
description: "A conversation with @Ken_Goldberg, professor of Robotics and Automation at UC BerkeleyThe dream in robotics is a robot that can do everythin..."
tags:
  - "clippings"
---
A conversation with [@Ken\_Goldberg](https://x.com/@Ken_Goldberg), professor of Robotics and Automation at UC Berkeley

The dream in robotics is a robot that can do everything a human can do. And that “generalist robotics” dream shapes much of the field today.

Many companies are pursuing a generalist approach, with the implicit belief that if you gather enough multimodal data, train on enough tasks, and scale the model far enough, generality will emerge.

But that has not really panned out in production. For example, [researchers at Stanford and Google DeepMind](https://arxiv.org/pdf/2503.01238) recently ran 1,600+ real-world robot trials across 14 axes of generalization and found that state-of-the-art generalist manipulation policies still struggle with small perturbations, from a changed camera angle to a rephrased instruction or shifts in object properties. The gap between promising research results and real-world deployability remains large.

Generality may come eventually, but it’s unlikely to be the near-term commercial unlock.

I sat down with Ken Goldberg, professor of Robotics and Automation at UC Berkeley, to talk about this tension and how we can bridge the gap. “I do think we’ll get to full generality at a certain point,” Ken told me, “but I don’t think that’s going to happen in the next few years.”

## Generalist Dream vs. Specialist Reality

The questions we ask in research are different from the questions that matter in a commercial environment.

In research, the focus is often on generalization: Can the system handle more scenarios? Can it adapt across environments? Can it learn broad capabilities from diverse data?

In a commercial context, the questions are much more concrete: Does it work? Does it keep working? What is the throughput? What is the uptime? Does it integrate into an existing workflow? Does it save money?

“You never think about uptime when you’re doing research, but if the robot is going down even once a week, your customers are going to give you a lot of grief and maybe walk away.” Ken said.

That is one of the central divides in robotics right now. Academic and frontier-model discussions are often driven by the pursuit of generality. Buyers are evaluating against an entirely different standard.

“It can be the most advanced technology on the planet, but if it’s not doing something really useful and reliable, customers aren’t going to want it.”

## What “Good Old-Fashioned Engineering” Means

This is where Ken’s notion of “good old-fashioned engineering” comes in. If the goal is to make robots actually work in production, then why not use every available tool, including those that have been used for decades, to improve reliability?

There is a common attitude that thinks it’s “cheating” to include mathematical functions like inverse kinematics or low-pass filters into a robot system. Their aspiration is to build systems that infer everything end-to-end, rather than building on well-established engineering.

“The generalists don’t want to use any tools that we know work in specialist scenarios. There’s a “purist” attitude that can be very dogmatic.”

But in production, that framing is counterproductive. “This kind of purism in the academic setting does push science forward,” Ken said, “but it also can be to the detriment of actually getting systems to work.”

Ken talks a lot about “good old-fashioned engineering,” (GOFE, which rhymes with Sophie) which basically means using whatever tools are available to make the system work reliably in the real world. If you know the height of the table, why not add a rule so the gripper never dips below that threshold and crashes? If you know something about the geometry of the workspace or the boundaries of the environment, why ignore that?

“GOFE is viewed as a crutch, something you’re encouraged to stay away from at all costs. But GOFE can be extremely helpful to get robots to work reliably in real environments so they can collect data,” Ken told me.

In practice, many of the best robotics companies are probably already doing exactly this. “They are quietly inserting GOFE into their systems. They are constraining environments, adding fallback logic, layering software, and shaping the workflow around the model.”

They’re just not always talking about it.

“I wish the field were more flexible about how to get real systems to work reliably. GOFE isn’t cheating. It can be extremely helpful to move systems toward generality. If you make it more explicit, then you have many more options.”

## The Opportunities

The assumption has been: just collect data on everything out there and throw it all together, and it will suddenly start to become general. That has not panned out, and that’s not what customers are looking for.

Even if generalist systems improve, most customers aren’t looking for a robot that might eventually do many things. As I wrote about [here](https://anneliesgamble.substack.com/p/rebuilding-the-middle-of-american), many want a robot that can at least do one thing really well, over and over again. “Most successes in robotics require 99.99% uptime,” [@samanfarid](https://x.com/@samanfarid), CEO of Formic, told me. “Most people underestimate how hard that bar is to hit.” Not to mention, real deployments are also incredibly complex, as I wrote about [here](https://anneliesgamble.substack.com/p/the-deployment-gap-in-industrial).

That’s why the best near-term opportunities are probably in specialist systems. “I’m very excited about accelerating the process to get robots to reliably perform specialized tasks,” Ken said. “These systems don’t require full general intelligence. They require bounded generality inside a specific workflow. A robot may just need to sort packages, or complete one assembly step. In many cases, that is enough to create value.”

GOFE can help get the first system working. And it often determines whether the second and third deployments get easier, or whether the company ends up rebuilding everything customer by customer.

As Ken explained, “You get it into production, and then you start selling systems and collecting more data. You’re collecting data around functionality, not generality. Once you’ve collected a large dataset for a specialized robot, you can use that to learn adjacent skills.”

In other words, the path is to start with a specialized use case, get into production, start a data avalanche, and expand outward from there.

## Don’t Expect Miracles

If the goal is to move robotics into production, the near-term opportunities aren’t about building pure generalizable robots. They’re about leveraging GOFE to build systems that customers can actually trust.

“It’s time for the community to come off its high horse a little bit,” Ken told me towards the end of our conversation. “Let’s use GOFE when helpful to get robots into production.”

The dream of general robotics is still alive. And I’m sure one day we will get there.

But in the meantime, Ken emphasizes the importance of getting things to work reliably in production: “Building great technology is one thing. Finding how to please customers is the next big step.”

Author’s note: An LLM was used for light copy editing only (spelling, grammar, and clarity). Content, meaning, tone, and structure remain unchanged.