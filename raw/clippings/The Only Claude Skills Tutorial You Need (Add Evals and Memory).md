---
title: "The Only Claude Skills Tutorial You Need (Add Evals and Memory)"
source: "https://www.youtube.com/watch?v=uT3EQPVIEb0"
author:
  - "[[Peter Yang]]"
published: 2026-06-03
created: 2026-06-05
description: "Today, I want to share 5 steps to build self-improving Claude Skills complete with evals and memory. I walk through building an /edit-post skill from scratch..."
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=uT3EQPVIEb0)

## Transcript

### Was eine KI-Fähigkeit ist und die 5 Schritte

**0:00** · Hey everyone. Today I am going to build an AI skill from scratch and share five advanced tips along the way that you won't find anywhere else. And that's because I've been completely AI skill build. It's just incredible to be able to encode my personal knowledge and tastes into a reusable skill that can help me save so much time every week.

**0:22** · And I promise you, if you build your own skills, it can help you save time, too.

**0:26** · All right, so let's do a quick recap first. What exactly is an AI skill?

**0:30** · Well, a skill is just a folder with instructions that AI can trigger for a given task. And why don't we build a skill to edit long form post and long form copy and we'll call it the edit post skill. And this is what the skill will look like by the end of this tutorial. So, it's going to have a bunch of files and it's going to be in a folder. And we're going to build a skill live by following these five steps. So first we are going to create the skill by using my best examples and personal context.

**0:58** · Then we are going to be explicit about when the skill should trigger by uploading the description of the skill. And then we are going to test the skill manually and build an eval so that it can actually check its own work and improve its own output without us even being there. And number four, we are going to build a memory MD. So the skill has memory of our past conversations and can actually improve itself over time.

**1:24** · And then finally, I'm going to show you a skill that can help you improve all of your skills by removing AI slop, making things more concise and clear and so on. All right, let's get into it. So this is clock code. I have an empty window right here and uh let's go ahead and paste our five steps here and give it some instructions. So I am doing a live tutorial to build an AI skill from scratch and I want you to work with me and follow these five steps but wait for my instructions.

### Schritt 1: Geben Sie der KI Ihren persönlichen Kontext und Beispiele

**1:56** · Now let's start with step number one which is create a skill using your best examples and personal context. All right so as I mentioned before I have a newsletter with different kinds of posts. I have these tutorial posts. I have opinion takes and a bunch of other content, right? And to prepare for this tutorial, what I've done is I made three text files with examples. So, here are some examples of my personal posts.

**2:21** · Here are some examples of my tutorial posts and some examples of my more product related posts where I break down AI products and other tools. Okay. So now let's go back to Claude and let's paste the three example files here and say I want to create an edit post scale that helps me edit a draft newsletter or any kind of long form post based on these examples.

**2:48** · Review the examples and ask me any questions and let's try to create a skill that's around one page. Okay, so that's pretty much it. That's the prompt that I typically start with to kick off building the skill. And the important thing to remember here is that to give it just as much examples and personal context as you can. Okay. So you see here that AI has read examples and it's found like dear subscribers opener hook the voice the short paragraphs and oneliners that I like and it's asking me a few questions now. So what should the skill do when you invoke it?

**3:19** · Edit a draft. That makes sense. How should it handle three post types? Let's say auto detect then confirm. And there we go.

**3:30** · And now because we've given examples, it should have enough to actually create a fairly good initial stab at a skill. So let's skip ahead and see what it comes up with. All right. So you can see here that it's created skill.md and it has a bunch of workflows. Detect the post type and then list the gaps and then rewrite it. It has post types with the links to the examples. It has a skeleton and the voice rules. So it's pretty good, right? It's pretty good initial first stab at the scale. And there's several pretty important lessons here.

**4:00** · So the first lesson is to always separate the skill.md with your personal context and examples. And this has a few advantages. Number one is that because we didn't just load all these examples into the actual skill.md. It doesn't have to read through our crazy examples each time. It can figure out from the draft post that we give it whether it's a tutorial post or a personal post and it can only load the relevant context.

**4:25** · Right. The second benefit is that if you ever share your skill.mmp with somebody like you don't have to actually include a bunch of personal information like everything in here is like generic and not so confidential to share but if you start sharing like all your example post and everything it might just be sharing a little bit too much right

**4:44** · okay and the third tip I want to share is that when you're giving AI examples be sure to give it at least a couple different examples right don't just give it one example otherwise it's going to overfitit to that single example and basically not give you the output that you actually want.

### Schritt 2: Bearbeiten Sie die Beschreibung, um die Fähigkeit zuverlässig auszulösen

**5:00** · Okay. So now let's move on to step two which is being explicit about when AI should trigger the skill. So go back to the skill here and you can see right here right in the description. So the way that skills work is that when you just ask AI random question in clock code or codeex or whatever app you use, it doesn't actually read the whole scale. It just reads like the name and the description. And based on description, it then decides whether to trigger the full skill or not.

**5:27** · So it's very important to be very explicit here about laying out exactly when you should use the skill. So here it has use when Peter paste a draft post or newsletter or asked to edit, title, or punch up a long form piece. I think this is pretty good, so I'll leave it alone right now.

**5:44** · But just make sure that you audit this section here because otherwise your skill will not reliably trigger. You can of course still trigger the scale manually with edit-post, but it just takes a little bit more work. So that's tip number two. Pretty straightforward. Now let's talk about tip number three, which is testing the skill manually and building evals so that it checks its own work. And this is a tip that I feel like other skill tutorials don't talk about, right? So let me go ahead and run the skill through a real post.

### Schritt 3: Erstellen Sie eine Evaluierungsschleife, damit die KI ihre Fehler selbst korrigiert

**6:15** · Let's say let's move on to step three. Here's a draft post to edit. Let's go ahead and paste the post right here. All right. This is going to be very meta because the post is basically about how to follow these five steps to create a scale. And now I'm using the skill to edit actual post.

**6:34** · And you notice here that it's detected that this is a tutorial style post, which is totally correct, right? And it's going to do a manual pass. Sponsor block is missing. No number preview up front. so on and so forth. And then it's going to create a draft right here.

**6:51** · Okay. So, it's a little bit hard to tell what it actually changed from the draft.

**6:57** · So, I think we should give some instructions of when you make edits, make sure to bode any changes you make.

**7:02** · And let's just take a quick look at the draft post. So, it looks like it's got watch now on YouTube, which is great. Uh I think yeah, this looks pretty good. A and normally I would take a much closer pass to this and make a bunch of more other suggestions, but why don't we just ask now to build evals for a skill. So what is an eval? First of all, an eval is asking AI to basically check its own work, right? And there's two types of evals. There's evals where you get AI to give it a score. So for example, how useful and practical is this post? Give it a score out of five and justify why.

**7:37** · And those evals, some people like them, but they actually aren't that good because um AI can't really tell a difference between a four out of five or a five out of five or a three out of five. It's going to make up, right?

**7:48** · So, a more straightforward eval is just to ask the AI to do a bunch of pass fail checks. Okay, so can you create up to 10 pass fail checks and document it in eval?

**8:03** · And let's put some checks in these categories. So, number one, the introduction. The introduction needs to catch the reader's attention. It needs to be crisp and concise. Tutorial-based introductions need to have a washdown YouTube link. The voice, the voice needs to sounds really authentic. It needs to not have any kind of AI slop like m dashes, a bunch of filler words like leverage and delve, and also AI slot patterns like this is not X, this is Y, or a bunch of really short sentences.

**8:33** · That's what AI likes to So, let's get rid of all that slop and let's check for that stuff. And substance is, can you make sure that there's actually practical insights here that people can put into practice right away? Can you make sure that the tone is helpful and genuine and authentic? All right. And is there a clear call to action at the end for the reader takes some sort of action with a list of steps? Okay. So, we just dictated all this. And by the way, to dictate all this stuff, I'm using this app called Whisper Flow, which I really love. and you can find a link to it in the video description.

**9:05** · All right, let's submit this and hopefully AI also uses our tutorial post examples and other post examples to come up with the evals.

**9:15** · So now let's skip ahead until it builds the evals MD so we can all take a look.

**9:19** · Okay, AI has created the evals MD and here we are. So is there an opening hook? Is there a crisp first two or three sentences? Is there a link to YouTube? No m dashes, no filler words, the AI slop stuff. And looks like it passed most of the eval except for these two. Now there's one very important instruction that we forgot to include.

**9:38** · So let me go ahead and tell AI now.

**9:41** · Include ink skill.md that when you run these evals, you should spin up a separate agent to run them. So there's a clean context window.

**9:50** · And if any of the evals fail, you should get the original agent to continue to edit the post until all the evals pass.

**9:58** · Okay, so now it's going to make sure that skill.md is aware of eval.

**10:03** · And basically now we are trying to set up a loop, right? Where you get one agent to edit our newsletter post or whatever long form you have. Then the AI will spin up a separate agent to run the evals here to check the post. And because it's a separate agent, it has a clean context window. It's not going to be biased by the previous results. And if anything fails, then it's going to get the original agent to do another edit pass until everything passes. And this is where the magic of building skills is and using evals, right?

**10:36** · Basically, it's going to keep iterating in a loop until everything passes and you as a human can just go get coffee or get lunch and have the AI do the work.

**10:46** · Okay? Now, of course, you still have to check the AI's results at the end, but I think building this kind of loop is so much more powerful than just building the skill and calling it a day. All right. Okay. So, it claims that it built the loop. Let's actually test it now by running the evals loop. And let's see if it actually does loop or not. So, here's the results. So, first it did one loop first and three out of the 10 evals failed. Right? There some hypotheticals in there. It's using some AI slot phrases.

**11:17** · It ran it again and then two failed. It ran a third time and two failed and it ran a fourth time and only one failed. And finally after five loops, it looks like everything is working. We got rid of all the m dashes, all the this is x not y slop and things look good. And it looks like there's some problems with our evals. So you have to be here to both make sure the evals are working correctly and that they're actually doing their job. But you can see this looping action, right?

**11:47** · It's doing a lot of work without us even being there. All right. Now, let's move on to step four, which is build a memory.md for the skill. So, it gets better over time. So, basically, the eval runs loops to improve the output from the skill, but we also want to improve the skill based on our conversations, right? So, let's say yes.

### Schritt 4: Fügen Sie Speicher hinzu, damit sich die Fähigkeit mit der Zeit selbst verbessert

**12:07** · Let's move on to step four. Build the md and list the lessons learned from our conversations so far. Okay, so this is the memory MD and it's basically like a reverse chronological order of summaries of past conversations that we had with AI while using the skill. So you see here that this is it for today. There's a bunch of stuff here and there's a little bit too much here. So I'm going to give it some more feedback. I'm going to say make sure whatever you include in memory MD doesn't overlap with eval.

**12:40** · Memory MD is for improving the skill itself. and try to capture each day in let's say just two or three brief sentences. You can add more if you want, but generally speaking, try to be concise.

**12:55** · Okay? Because what I don't want to do is have this memory be super long and then having Claude or AI get confused again.

**13:03** · Okay, this is the new memory MD is much shorter. Now, the key lesson was that we wanted to keep the grading agent and the edit agent separate. And yeah, so this is I would say super useful, but if we did this for real, I would give a bunch more feedback about the draft and it's going to remember a lot more things. And I think memory is actually optional, but I think it's useful when you can't find easy pass fail evals for feedback that you want to give.

**13:30** · Like for example, maybe you want to give a feedback to I don't know make the voice more authentic or something that's more vague and can't exactly have a pass fail eval. Okay. All right. So we covered four steps already and the last step is to build your own skill to build skills. So let's just uh do a hypothetical here. Let's say we were able to build a skill that builds skills for us based on our conversation here.

### Schritt 5: Erstellen Sie einen Fähigkeitseditor, um all Ihre Fähigkeiten zu verbessern

**13:59** · Don't build a skill. just outputting chat uh what your one pager or couple paragraph skill will look like and hopefully it actually uses the five steps that we covered to build a skill.

**14:10** · So let's take a look. All right, so here we have you build skills. Here's a target structure. You got to have context separate from the skill examples eval and memory and then follow these five steps. Right? All right. So it's as easy as that. But why do you need a skill to help you build skills? Look, the reality is that AI is doing a lot of the writing for us when building the skills. And if you don't pay attention, inevitably it's going to add a lot of copy and stuff to it and it's going to turn into just AI slop.

**14:37** · So you can basically tell it to build a skill to fix it own skills or what you can do is you can copy my skill builder skill that I have here. So skill. All right. Or Okay. So Okay. So you can just tell AI to build a skill based on your conversations building past skills like we did here. Or you can go ahead and copy my skill editor skill.

**15:06** · And the skill editor skill just has a little bit more information in it like preventing AI slop words and making sure that the skill itself is very concise and following some rules around progressive disclosure and so on so forth. Let me show you it in action. So apply scale editor to this edit post scale and let's see what kind of changes it makes. All right. So we ran scale editor scale on our own scale and we found that it is full of AI slop m dashes, right?

**15:38** · So it's going to get rid of all the m dashes. It's going to get rid of not y phrasing and it's going to fix a bunch of formatting. So overall, it looks like it just fixed a bunch of formatting, which is pretty good because it means that our original edit post skill is actually pretty sound. And yeah, that's pretty much it. You want to build a skill editor scale to periodically run to audit your skills or like to to tag when you're building new skills because it just helps you make everything more concise, right?

**16:08** · I don't really believe in building super long skills that humans don't bother to read. I really think like every skill needs to be reviewed by human eyes. and to make it actually good. All right, so let's recap. So here are the five steps again to build really great skills. Number one, create the skill with AI by giving it your personal context and your best-in-class examples of the output that you want. Number two, be explicit in the description of the skill about when AI should trigger. Say something like use when XYZ.

**16:39** · Just make it super explicit, right? Number three, test the skill mali a few times and give it feedback and then ask it in the same conversation to build an evals.md with a bunch of past fail checks on important things to do so that AI can actually check and improve its output without you even having to be there.

**17:02** · Number four, build a memory MD for the skill so that it actually improves over time. And finally, consider building your own skill to build skills or just copy my skill editor skill here. Now, uh quick plug, my skill editor skill, full disclaimer, is available to pay subscribers of my newsletter along with all the other great skills I have here.

**17:26** · Personal adviser, health coach, uh infographic designer, and more, right?

**17:32** · And I spent a lot of time making these skills great. They're all handcrafted.

**17:35** · They're all AI slot free. So check out behindthecraft.com if you want access to your skills. I'll include the link in the description too.

### Wo menschlicher Geschmack noch eine Rolle spielt

**17:44** · All right, one last thing as you think about building skills. Following these five steps is really important. But um the reality is that even with all these best practices, the skill can only produce output that is maybe 80 to 90% there. The difference between kind of AI slop and actually good output is you spend the last 10 20% reviewing AI's output and handcrafting it and making it even better with your human taste and judgment. Right?

**18:13** · I've tried to encode as much of my judgment and taste into skills as possible, but it still misses stuff. And the way that I actually write newsletter posts is similar to the way that people build days. I spent a lot of time up front creating the first draft and maybe dictating my ideas. I then get the AI to do the initial edit pass using something similar to the edit post scale and these best practices. And then the last 10 20% I've spent a lot of time just reading through it, make sure it makes sense, applying my own common sense before sharing it with you all.

**18:45** · So it's not AI slop. I promise you guys.

**18:50** · All right. So, if there's one takeaway from this video, take a look at at your past week. Figure out where you're spending a lot of time and build skills to streamline as much of this work as possible. And remember to build things like evals and memory for your skills so that they can actually improve by themselves and get better over time with your input. All right, so if you found this video useful, please like and subscribe to this channel and I'll see you next time.