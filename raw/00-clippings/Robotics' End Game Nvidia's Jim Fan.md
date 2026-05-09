---
title: "Robotics' End Game: Nvidia's Jim Fan"
source: "https://www.youtube.com/watch?v=3Y8aq_ofEVs"
author:
  - "[[Sequoia Capital]]"
published: 2026-04-30
created: 2026-05-08
description: "Jim Fan, who leads the embodied autonomous research group at Nvidia, returns to AI Ascent to argue that robotics is entering its end game — and that the play..."
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=3Y8aq_ofEVs)

## Transcript

### Einleitung

**0:02** · And up first, I'm delighted to introduce my friend Jim Fan.

**0:06** · Uh Jim leads the embodied autonomous research uh group at Nvidia, otherwise known as Nvidia robotics.

**0:12** · Um I think that robot robots are just one of the most thrilling things that's going to happen. Uh a car basically is a big robot, but I'm excited for robots can go beep boop and lift things for us.

**0:22** · And so, Jim was Jim was a standout at last year's I I sent, and we're delighted to have you back.

**0:28** · Thanks \[applause\] everyone. Thanks.

### Die Entstehungsgeschichte von DGX One

**0:30** · So, it was a summer day in 2016.

**0:32** · Actually, right in this office that we're sitting, \[snorts\] there's a guy in shiny leather jacket, you know, big biceps, hurling this large metal tray.

**0:43** · And on this large piece of metal, he wrote, "To Elon and the Open AI team, to the future of computing and humanity, I present you the world's first DGX-1."

**0:55** · So, that was the first time I met Jensen.

**0:57** · And as any good intern would do, I rushed to getting line to sign my name on it.

**1:03** · So, can you spot it, my name?

**1:05** · It's here. And can you spot another?

**1:08** · That's Andre, right there.

**1:10** · So, Andre, we're going to the Computer History Museum.

**1:13** · I feel like a dinosaur.

**1:16** · You know, back then, I had no clue what I was signing up for.

**1:21** · And then, no one can describe what happened next better than Ilya himself.

**1:26** · If you believe in deep learning, deep learning will believe in you.

**1:31** · And oh boy, did deep learning believe in all of us big time.

**1:36** · Three step functions, 6 years.

**1:39** · That's how all it took to bring us here today.

### Die große Parallele

**1:42** · The first tick, GPT-3, pre-training.

**1:46** · Next token prediction is really about learning the rules of grammar, the shape of language. It's about simulating how thoughts and code and strings in general should unfold.

**1:57** · 2022, InstructGPT, supervised fine-tuning, aligning the simulation to do useful work.

**2:05** · 01, reasoning, using reinforcement learning to surpass imitation learning, and finally, auto research, accelerating the whole loop beyond what's humanly possible.

**2:17** · So, as Andre said, all the labs are getting to the final boss fight.

**2:22** · So, for LLMs, they're in the thick of the end game.

**2:27** · And honestly, I'm very jealous.

**2:29** · Look at how happy Andre was, big smile on his on his face. The LLM folks are having the party of their lifetime.

**2:37** · They're speedrunning AGI on mystical creatures literally called methos.

**2:43** · So, why can't robotics get a piece of fun?

**2:47** · So, as any self-respecting scientist would do, I copy homework and I give it a new name.

**2:53** · I call it the great parallel.

**2:56** · So, instead of simulating strings, can we simulate next physical world state?

**3:02** · And then we can align through action fine-tuning onto a thin slice of that simulation that matters for real robots.

**3:09** · And we let reinforcement learning carry the last mile.

**3:14** · And that's it.

**3:16** · The great parallel, copying the LLM success. If you can't beat them, join them.

**3:20** · So, please join me in a new episode, robotics, the end game.

**3:26** · I'm sorry, I just couldn't resist. Nano bananas too good. Thanks, Demis.

### Robotics Endgame Setup

**3:31** · So, how do we play the end game? It boils down to two things, model strategy and data strategy.

**3:37** · Let's look at the model first.

### Warum VLA nicht ausreicht

**3:39** · The last 3 years were dominated by VOAs or vision language action models, and models like Pi and Groot fall in this category.

**3:49** · So, we assume that the pre-training is done by a VOA, and we simply graph an action head on top of it.

**3:56** · But really, if you think about these models, they're LVAs because the most amount of parameters are dedicated to language. So, language is first first-class citizen, followed by vision and action.

**4:08** · And by design, VOAs are great at encoding knowledge and nouns, but not so much at physics and verbs. It's kind of head heavy in the wrong places.

**4:18** · This is my favorite example from the original VOA paper.

**4:22** · Move the Coke can to a picture of Taylor Swift. Yes, it has not seen Taylor Swift before. Yes, it's able to generalize, but this is not quite the pre-training ability that we're looking for.

### Videoweltmodelle

**4:32** · So, what's the second pre-training paradigm?

**4:35** · And I always thought that it would be something glorious.

**4:39** · Unfortunate, it turns out that this is AI video slop that we call.

**4:45** · You know, I can watch these um cats playing banjo on security cam all day.

**4:48** · It's peak internet.

**4:51** · But really, look at this. No one can take this seriously \[laughter\] until we realize that these video models are learning to simulate next world state internally.

**5:03** · So, these are some rollouts from VEO-3.

**5:06** · You can see that the models, they pick up gravity, buoyancy, lighting, reflection, refraction, all by themselves. None of this is coded in.

**5:15** · Physics emerge by predicting the next blob of pixels at scale.

**5:21** · And even visual planning emerges.

**5:23** · Look at how VEO solves these mazes.

**5:27** · It solves them by running simulation forward in pixel space.

**5:32** · And draw attention to the lower right corner here. This is my favorite example. Let's watch, and you blink if you miss how VEO-3 solves this one.

**5:41** · \[laughter\] It's super smart. You know, VEO-3 figures out that if you're not looking, geometry is optional. I call this physics slop.

**5:53** · So, how do we make these world models useful?

**5:56** · Well, we do action fine-tuning. We align the superposition of all possible future states, and \[snorts\] collapse that onto a thin slice that matters for real robots.

### DreamZero World Action

**6:09** · Introducing Dream Zero.

**6:12** · It's a new type of policy model that dreams a couple seconds into the future and acts accordingly. And you know that motor actions, they're high-dimensional continuous signals. So, that looks just like pixels. We can render it at the same time as we render the videos. So, Dream Zero Zero jointly decodes the next world states and next actions. And as a result, it's able to zero-shot solve tasks and verbs that it has never seen in training.

**6:44** · And as the robot executes, we can visualize what it's dreaming about. And the correlation is very tight. If the video prediction works, the action works. If the video hallucinates, the action fails. So, once again, vision and action are now first-class citizens. And we have a lot of fun with Dream Zero. So, we just roll the robot around um in our lab, and then type random things into the prompt box.

**7:08** · And of course, Dream Zero is not going to get all of these tasks 100% robust, but it's kind of like GPT-2. It's trying to get the shape of the motion correct in every case. So, Dream Zero is our first step towards open-ended open vocabulary prompting for robotics. And we \[snorts\] call this new type of model world action models or WAM. So, let's all take a moment of silence for our dear friend VOAs.

**7:37** · They've served us well. Rest in peace. Long live world action models.

**7:43** · \[clears throat\] And next, data strategy.

### Skalierung der Datenerfassung

**7:46** · This is Nvidia's chief scientist, Bill Dally, operating teleoperation inside our lab. And given his salary, I think this is by far the most expensive teleop trajectory ever collected in our data set. The past 3 years have been dominated by teleoperation. It's the golden era. All right, VR headsets, extremely optimized latency for streaming, and these complex rigs that look like medieval torture devices. You know, so much investment in industry, so much pain and suffering.

**8:21** · And yet, for teleop, it's upper bounded by 24 hours per robot per day, the fundamental physical limit. And actually, who am I kidding? It's more like 3 hours per robot per day, and only when the robot god is merciful because they throw all tantrums all the time.

**8:37** · So, how can we do better?

**8:39** · Well, how about this?

**8:41** · You just wear the robot hand on your own hand. So, this is called UMI or universal manipulation interface, and it's a deceptively simple idea. You wear the robot actuator on your hand and directly collect the data as humans, while getting the rest of the robot body out of the loop. Yet, I would say UMI is perhaps one of the greatest papers ever written in robotics data, and it spawned two unicorn startups.

**9:09** · On the left hand side is Genesis, improving this design so you can wear the gripper here. And then on the right hand side, Sunday made these three-finger data gloves. So, last year, we took it one step further. We designed this exoskeleton that has a one-to-one mapping with five-finger dexterous robot hands, and we call it Dex UMI. Let's look at it in action. On the left, the human directly collecting data always is fastest.

**9:35** · On the right, look at how difficult teleop is. All right, the human operator, here one of our most skilled PhDs, he has to align very carefully, right? And then it's super slow. Also, the success rate is very low as well. And in the middle, you just exoskeleton and you collect data directly. And we train a robot policy on this data.

**9:58** · So here what you see is a fully autonomous robot of a policy that's trained on zero teleoperation data. So we're able to break the curse of 24 hours per robot per day and see how happy these robots are because they no longer need to be in the loop for data collection.

**10:16** · So is this the answer? Have we solved scaling for robotics?

**10:21** · Anyone driving Tesla or Waymo here?

**10:23** · Anyone?

**10:24** · Right?

**10:25** · You know, when you're driving, you're actually contributing to the biggest physical data flywheel. And the beauty is you don't even feel it during FSD because the data upload is an ambient process. Yet wearing these Umi or data wearables is still cumbersome, right? It's intrusive. It's not as seamless as just driving to work. So we need an FSD equivalent.

**10:52** · The data collection needs to get out of the way, fade into the background so we can capture the full glory of human dexterity across all walks of lives, across all labors of economic value. So we're going all in on human egocentric videos that come with these detailed annotations like hand position tracking and dense language annotations.

### EgoScale und Skalierungsgesetze

**11:17** · Introducing Ego-Scale.

**11:20** · Where 99.9% of the training that goes into this is based on human egocentric videos. And the result is an end-to-end policy that maps directly from the camera pixels here to 22 degrees of freedom high dexterity robot hands. What you see here is fully autonomous. We pretrain Ego-Scale on 21K hours of in-the-wild egocentric human data with zero robot data whatsoever. And during pretraining we predict these hand joints and wrist poses.

**11:53** · Then action fine-tuning, we collect only 50 hours of high precision mocap data gloves and 4 hours of teleop. That's 4 hours of teleop. Less than 0.1% of our training mix. And with this Ego-Scale is able to generalize to these very dexterous tasks like sorting card or manipulating syringe. Right? Over transferring the liquid. You know, someday we might have robot nurses at home. Might as well try this.

**12:24** · And for these tasks it takes only one shot demonstration at test time to learn different shirt folding strategies. And perhaps the most fascinating finding from the paper is that we discovered this neural scaling law for dexterity. It's a very clean relationship between the amount of hours we put into pretraining and the optimal validation loss. In fact, it's a clean log-linear mathematical equation. Six years after the original neural scaling law for language models.

**12:58** · So if we put all of these data strategies on this chart, X axis is alignment to the robot hardware, Y axis is scalability, this is what it looks like. Teleop, the least scalable. Data wearables, you can go up to hundreds of thousands of hours. And egocentric video, if we're able to spin the FSD flywheel, easily 10 million hours in the next year or so.

**13:22** · And if we draw a line here, everything to the left of this line is a new paradigm, sensorized human data. So let me make a few predictions. In the next year or two, we'll see teleop dropping and dropping to almost negligible amount. And then there will be an ensemble of data wearables custom designed for different hardware and use cases. And finally, the main diet for robotics will be egocentric videos.

**13:49** · So, a moment of silence for our dear friend teleop. You have served us well. Rest in peace. Long live sensorized human data.

**13:58** · Are we done with the data strategy yet?

**14:01** · Did you notice I put two rings on data strategy?

**14:04** · What's the outer ring here?

**14:06** · All the LM frontier labs have spent significant budget now on acquiring millions of coding environments to do reinforcement learning. So robotics is the same. We're in urgent need to scale up environments. And of course, you can always do reinforcement learning directly on the real robot. So in our lab, we use RL to push certain tasks to almost 100% success rate so you can do these continuous execution for hours on end.

**14:35** · You know, it's kind of therapeutic to see these robots assembling GPUs just by themselves. Or as a wise man would say, good boy, this task has been approved by my boss. Yet we can't get \[snorts\] to 1 million environments because that would require 1 million robots if you do it the previous way. So we need a better way.

**14:55** · Here, let's say you take an iPhone picture and you can pass this through this 3D world scan pipeline to extract all the objects and then automatically synthesize them again inside a classical physics simulator. So all these objects are actually interactive after the scan. And then you can augment this infinitely in simulation with variations that we call digital cousins. So now iPhone basically become a pocket world scanner in this process that we call real-to-sim-to-real.

**15:29** · And in this way we have a scalable way to port the physical world into the digital world.

**15:35** · But still this method relies on a classical graphics engine. Can we do better?

### DreamDojo und die Roadmap

**15:41** · Introducing Dream Dojo.

**15:44** · So it's our spin on video world model and turning them into full-fledged neural simulators. Dream Dojo takes as input these continuous action signals and outputs the next RGB frames as well as sensor states in real time. Not a single pixel you see here is real. And Dream Dojo is able to capture and learn the mechanics of different robots through a purely data-driven approach. There is no physics equation, no graphics engine involved in this process.

**16:16** · So the new post-training paradigm for robotics is a massively parallel RL system that runs on a few real robot stations, a bunch of graphics cores running world scans, and heavy inference compute running world models. Or as this equation goes, compute now equals environment now equals data. Or as a wise man would say, the more you buy, the more you save. And this message has been approved by my boss.

**16:47** · So that's it. Putting it together, the great parallel that robotics will follow. And it's happening as we speak. And we're looking at the beginning of the end game.

**16:59** · You guys play the video game Civilization?

**17:03** · Still my favorite.

**17:05** · I like to think of my research as unlocking game achievements on this civilizational technology tree.

**17:12** · \[clears throat\] And there are three more achievements to unlock for robotics and then we're done. I can retire and I can't wait for that. The first is passing the physical Turing test. Across a wide range of activities, you cannot tell the difference between a human doing a task or robot doing it. Maybe not drunk humans, but you know. Physical Turing test is about unit energy in and unit labor out.

**17:43** · And just by judging at the sexy pose of this robot, I think the work is cut out for us. So maybe it's two to three years away. And next, physical API. You have a whole fleet of robots and they can be configured just like any other software using APIs and command lines, orchestrated someday by Opus 9.0. And if we have this physical API, we'll be able to realize lights-out factories. Those are essentially printers of atoms.

**18:11** · They take as input design in markdown files and then output fully assembled products, completely autonomous. Or these wet labs that automate scientific discoveries in chemistry biology and medicine. And the final stop, physical auto research. When the robots start to design, improve, and build the next iteration of themselves far beyond what's humanly possible.

**18:40** · So you might ask, is this too science fiction? Like are we going to see this in our lifetime?

**18:46** · Well, it took the AI community 14 years to go from the first forward pass of AlexNet in 2012, a model that barely recognized cat versus dog, to AI ascent today, 2026, where we talk about agentic auto research.

**19:04** · And let's just add another 14 years. How about that?

**19:08** · 2026 is right in the middle of 2012 and 2040. And technology does not advance linearly, it advances exponentially. So \[snorts\] I can say with 95% certainty that we'll get to the end of the end game, the end of the technology tree, by 2040. And we'll still be all We'll still be young. If you believe in robotics, robotics will believe in you.

**19:38** · And to all of us here, sitting here, I think our generation was born too late to explore the Earth and too early to explore the stars, but we are born just in time to solve robotics.

**19:53** · Thank you.

**19:54** · \[applause\] \[applause\]