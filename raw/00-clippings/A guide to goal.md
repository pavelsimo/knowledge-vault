---
title: "A guide to /goal"
source: "https://x.com/dkundel/status/2062650378089594955"
author:
  - "[[@dkundel]]"
published: 2026-05-21
created: 2026-06-05
description: "We launched the goal mode (or /goal) as a way to help you have Codex drive towards a concrete outcome. When you set a goal Codex will contin..."
tags:
  - "clippings"
---
![[raw/00-clippings/images/243adeb59da5e2339768a25ed9a872e0_MD5.jpg]]

We launched the goal mode (or /goal) as a way to help you have Codex drive towards a concrete outcome. When you set a goal Codex will continue to work until the goal is achieved, whether that takes hours or days. Some people have used Codex to work on a single goal for **more than 120 hours**.

> May 21
> 
> /goal has graduated from an experiment—for tasks big and small, Codex gets your work done. Use goal mode in the Codex app, IDE Extension, or CLI to give Codex a specific milestone, and it will keep working until it gets there, even across hours or days. You can check in and

Goal mode is incredibly powerful, and there are a few things you can do to get the most out of it. Here are 7 things to keep in mind when you use /goal.

## 1\. Clear \*verifiable\* criteria

The prompt you define when you activate goal mode might act as your initial prompt but more importantly it will act as your exit criteria for the goal. Codex will check after a turn whether the goal has been achieved or not. As a result your goal prompt should not be overly long and focus on a clear criteria on when the goal has been achieved.

In most cases **a good goal contains a clear number\*** for the model to reach before the goal is considered complete. Good examples:

1. "Reduce the build and deployment time by 30%."
2. "Migrate this feature from TypeScript to Rust and reach 100% test parity."
3. "Improve application scaffolding to get the largest contentful paint in production to below 2.5s."

\*The prompt doesn’t always have to be a number but generally it helps with the next tips.

If you are unsure how to best define your goal or you want to work with Codex first to brainstorm the project you **don’t have to start a thread with goal mode**.

Codex can set a goal on its own so you can start a conversation and when you are ready for Codex to start the work you can **ask Codex to set the goal based on your conversation**.

You can also always edit the goal at any point in time by pressing the edit button in the Codex app or using /goal again in the CLI.

## 2\. Provide guidance if possible

Sending a prompt like "Reduce the build and deployment time by 30%" can be cool and even find some creative solutions. It could also send Codex down a wild goose chase if you have an idea where the issue might lie.

When possible **give Codex a starting point where to start working**, what tools it can use to achieve the goal, or any other pointers where Codex might go down the wrong path.

My colleague [@reach\_vb](https://x.com/@reach_vb) for example did this in one of his experiments by telling Codex it can use the Chrome browser to go into Google Colab and acceptable limitations like generating its own dataset when he had Codex train a model.

> May 22
> 
> Couple days back @swyx posted a challenge: code a ~10M transformer in JAX/Flax/Optax, run it in free Colab, and train it on addition w/ your agent! I gave Codex the screenshot + /goal. It controlled Colab through Chrome, used my signed-in session, handled runtime/editing

Similarly if you are looking to reduce build times and you know where the majority of the time is spent try to point Codex to that area first as part of your prompt.

Alternatively, you can even have Codex **do some initial research in plan mode** and have Codex create a plan as a file that it can use to document potential options. Then have your goal reference that plan.

## 3\. Make progress measurable

If your goal is ambitious or if there are various ways that Codex could get closer to the goal it’s important that you **give Codex tools to measure progress**.

In the case of some tasks this might just be a given like improving build times or increasing test coverage because Codex often already has the tools or naturally creates them.

For other goals it’s worth **brainstorming with Codex on what tools would be helpful** or hinting it towards ways to know how it is making progress. For example having tools to compute visual diffs between two screenshots or creating an eval suite for an agent that you are trying to tweak.

When I had Codex recreate some components from a video I had Codex create a tool for itself to be able to diff the screenshots and inspect the diffs. It chose to evolve the tool over time to have different diff modes.

![[raw/00-clippings/images/6511d18bf30882429cfce31c606a6144_MD5.jpg]]

A screenshot Codex generated to visually compare two frames

Depending on your task you will also want to consider if there are additional criteria you want to measure/check that might make Codex think the task was completed but that you’d consider incomplete. For example, implementing a UI by cropping the design inspiration and inlining it to be “pixel perfect” or getting to a 100% passable test rate by reducing test coverage.

## 4\. Create a realistic environment

To have Codex truly make progress towards the goal it needs to **operate in a realistic environment**. In practice that means that if you are trying to improve deployment times or latency issues it should have **access to deploy and test environments that mimic production**. So same stack, same flags, a similar database.

As an example, we were debugging some build and deployment time improvements for [developers.openai.com](http://developers.openai.com/). We were already using deploy previews so Codex was able to use those to deploy to and review the associated logs but our preview deployments had some build paths disabled compared to full production runs. So instead Codex had to do manual deployments to the same environments with similar production configurations to inspect the environment.

Similarly you can have Codex use [computer use](https://developers.openai.com/api/docs/guides/tools-computer-use) to test the actual application. To work on some performance improvements on iOS [@dimillian](https://x.com/@dimillian) even used a physical device for the most accurate environment.

> 19h
> 
> Today I have Codex running Codex Remote on my physical device, and recording various profiling traces about it, then doing my report of what are the biggest wins we can have. Looking at optimizing the thread view and there is a lot coming of optimizations coming to it.

## 5\. Be careful with visual goals

Giving Codex a visual goal like "Implement this UI 100% pixel perfect based on this image" is tempting but depending on the setup can also cause some trouble.

If you don’t give it the right guidance and constraints it might end up rabbit-holing on some issues ignoring the overall goal. For example, if the reference includes graphics that Codex is expected to generate whether it’s SVG icons or images it might get lost on getting those accurate rather than dissecting the problem appropriately.

Additionally, Codex will need tools to do the visual comparison correctly which means more image inputs and higher overall token usage without necessarily giving Codex an easy way to identify opportunities.

Instead images can often serve as helpful context to drive towards the goal but you should **find other ways for Codex to identify that the goal has been reached** such as feature checklists, specs to implement, adherence to the design system, etc.

## 6\. Keeping track of progress

If Codex ends up working for hours or days in the background (or even on another machine) it’s easy to lose track of how far Codex is or what work has happened. There are a few things I found helpful depending on the goal to keep up with it:

1. **Ask Codex to commit at meaningful steps and push to a draft PR**. This is helpful especially if you work on a website with preview deployments.
2. **Have Codex update an artifact for executives.** This can be an HTML file that you can keep open in the [in-app browser](https://developers.openai.com/codex/app/browser) or even deploy to your team using [Sites](https://developers.openai.com/codex/sites), an image of a rendered graph that tracks progress or even a plain markdown file.
3. **Instruct Codex to post updates.** You can also ask Codex as part of the goal to communicate major progress back to a Slack channel or other places where you want progress to be documented.
4. **Use other chats to ask for status updates.** If you just want a quick check in at the current state you can run /side to spin up a new side chat and ask questions there. Because it forks the current thread it has all the context until this point but is also short lived. The alternative in the Codex app is to ask Codex in a regular new chat to read the other goal thread and answer your questions. This can be especially powerful if you ask Codex to schedule an automation to regularly check in.

## 7\. Clean up and finalizing results

Great, the goal is finally achieved! Time to just [$yeet](https://chatgpt.com/plugins/share/f10638fad5924af28945c0d2457d8b2c) it to the team and call it a day?

Generally I found it helpful especially for optimization tasks for Codex to reflect on the work done and review it. You can start with a /review to run a [local code review](https://developers.openai.com/codex/app/review) but it can also be worth having Codex reflect more deeply on the different attempts it took to solve the goal and clean up accordingly.

Since Codex will continue to go until it reaches the goal it might have tried several things that did not work well enough or at all that might have remained in the changes.

## Time to goal your next task

The goal functionality in Codex is an incredibly powerful tool to solve some of the most meaningful challenges you encounter but providing the right environment and instructions will get you to your goal more efficiently.

**What have you used** **/goal** **for?**