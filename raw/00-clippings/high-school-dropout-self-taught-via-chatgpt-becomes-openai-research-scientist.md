---
title: "High School Dropout Self-Taught via ChatGPT Becomes OpenAI Research Scientist"
source: "https://x.com/dotey/status/2023905572035158295"
author:
  - "[[@dotey]]"
published: 2026-02-18
created: 2026-04-06
description: "Gabriel Petersson is a research scientist on the OpenAI Sora team, working on video generation models. In a role that typically requires a PhD, he has no high school diploma, no college degree — he taught himself math and machine learning using ChatGPT."
tags:
  - "clippings"
---
Gabriel Petersson is a research scientist on the OpenAI Sora team, working on video generation models. In a role that typically requires a PhD, he has **no high school diploma, no college degree** — he taught himself math and machine learning using ChatGPT.

![[raw/00-clippings/images/fe7f660335b502146af808665bcde823_MD5.jpg]]

High School Dropout to OpenAI Researcher - Gabriel Petersson Interview (Extraordinary) [https://www.youtube.com/watch?v=vq5WhoPCWQ8](https://www.youtube.com/watch?v=vq5WhoPCWQ8)

He was born in a small town called Vaggeryd in central Sweden. He **dropped out at 17** to join a startup, became a temporary CTO of Sweden's largest cloud kitchen at 19, then worked as an engineer at Dataland and Midjourney, before **joining OpenAI in December 2024**. He holds an O-1 extraordinary ability visa — one of the supporting materials was a collection of his technical answers on Stack Overflow.

In the Extraordinary podcast, he and host Sigil Wen discussed the full arc of his journey: how he dropped out, how he self-taught, how he uses AI for research, how he finds work, and how he thinks about education. The following is a summary of that conversation.

## Key Takeaways

- **Top-down learning**: The traditional path to learning diffusion models starts with calculus and linear algebra — at least six years before touching real models. Gabriel used ChatGPT to learn top-down and recursively, building a core understanding of diffusion models in three days.
- **Daily life on the Sora team**: Watch generated videos, find problems, change model architecture or data, train, review results, repeat. Heavy use of AI throughout, but "I'm not vibe coding — I have very strong opinions about my code."
- **Demo-based job hunting**: Build something a person can understand in 3 seconds, go directly to decision-makers, bypass the hiring process. "Companies just want to make money. If you prove you can help them make money and you can write code, they'll hire you." A working demo beats degrees, internships, and extracurriculars.
- **Critique of academia**: Universities no longer monopolize foundational knowledge. Professors defend the old system because their status is threatened. But he also acknowledges college is "a lot of fun" and still a reasonable choice for less driven individuals.

## [1] "I've Got a Big Party Tonight — Can I Come Tomorrow?" "No."

Gabriel's dropout story involved no deep deliberation.

His cousin called one day saying he'd met someone — "super smart" — who wanted to build a startup around e-commerce product recommendation systems. The guy was in Singapore doing research. "We're starting today. Come to Stockholm."

Gabriel was 17 and living in rural Sweden. His answer: "Bro, I've got a big party tonight — can I come tomorrow?" His cousin said no. So he took the next bus to Stockholm and **never went back to high school**.

That company became [Depict.ai](https://depict.ai/) — later admitted to Y Combinator (S20 batch) — building AI-powered product recommendations for e-commerce sites. The team was all 17–18 year-olds; researcher Oliver Edholm was 16. [Note: Depict.ai later raised a $17M Series A led by Tiger Global, with clients including Office Depot and Staples.]

No one knew how to run a startup. No one knew how to sell. Gabriel started with cold emails — poor results. He tried cold calls — slightly better, but limited, given he was an 18-year-old non-technical person.

He came up with a different approach: scrape a target company's website in advance, train a new product recommendation system on it, and **print the results on A3 sheets** — the client's current recommendations on the left, his on the right. He made hundreds of these, packed them into a large folder, and walked straight into companies' offices.

> "Hey, can I speak with whoever's in charge of e-commerce?" Then he'd pull out the comparison. Clients were always surprised. "You did all of this? How? That's so cool."

But clients would immediately ask: how long to go live? What are the unknowns? Gabriel was ready. He carried a script that could be pasted directly into a client's browser console to switch the product recommendation system on the spot — with built-in A/B testing that automatically tracked revenue from each version. **He could close deals on the first visit.**

At the time he was sleeping in his cousin's "dorm" — not a real dorm, but a small apartment in Sweden only available to enrolled students. He wasn't a student, so he had to improvise whenever paperwork was required. The bed was a sofa cushion he'd found in a common room.

> "The room was disgusting, but it worked."

Sigil asked how he kept going. Most people would have quit and gone back to school.

Gabriel said:

> "I've always had a distorted perception of reality. I was 100% certain this would make me a billionaire. 100%. Not a shred of doubt in the world."

He worked through the night, night after night, running sales calls across Stockholm. In his mind, nothing else mattered.

## [2] "I Always Thought I Was Too Dumb"

Gabriel couldn't write code when he dropped out.

His introduction to programming came from his cousin. At 13, the cousin showed him Java and he built a rudimentary Pokémon turn-based game. Later he did some Python on Udemy and made a duck-dodge-bullets game. He also tried Andrew Ng's machine learning course. [Note: Andrew Ng is a Stanford professor whose Coursera ML course is one of the most popular AI introductory courses in the world.]

His summary of that period:

> "I always felt like I was too dumb. I just couldn't do these things."

He actually learned to code at Depict.ai — because the company needed to survive and he was forced to solve real problems: building recommendation systems, writing web scrapers, doing client integrations, setting up A/B tests.

He believes **having real problems actually makes learning much easier**. "People always say, how do you learn things without going to school? It's actually easier the other way around. You have a real problem you can break into steps: I need to integrate a recommendation system into this e-commerce site, so I need to learn how to select page elements, how to inject content… then go step by step, check Stack Overflow, ask friends."

The key ingredient is pressure. "If someone tells me, learn this thing, you have unlimited time, and you won't make money from it — I will never learn it. Absolutely impossible."

## [3] Top-Down Learning — Three Days vs. Six Years

Gabriel believes the fastest way to learn something is **"top-down"**: start with a real problem, read everything you need to solve it, discover sub-problems, read those, and recursively drill down to the core.

![[raw/00-clippings/images/fa2da09dc9666ca0dc8c94af5c31b5d0_MD5.jpg]]

But schools teach the exact opposite. Want to learn machine learning? Forget touching ML — spend the first four years on math: calculus, linear algebra, matrix decomposition… then simple statistical learning methods like linear regression. It's a long time before you get to production-grade machine learning.

Why does school use bottom-up? Because it scales. Step one is always this, step two is always that — no need for one-on-one tutoring. But the efficiency is terrible.

> "Now with ChatGPT, all of this has changed. Universities no longer monopolize foundational knowledge. You can get any foundational knowledge from ChatGPT."

He then said something that sparked widespread debate: "I genuinely can't take seriously any university that doesn't incorporate large language models into their curriculum."

Sigil pressed: exactly how did you use AI to self-teach math and machine learning to the level needed to work at OpenAI?

Gabriel walked through how he learned diffusion models. [Note: Diffusion models are the dominant technology behind image and video generation — they work by progressively adding noise to data and then learning to reverse that process. Stable Diffusion and Sora are both based on this family of architectures.]

**Step 1**: Ask ChatGPT: what are the most fundamental concepts in video and image AI models? ChatGPT starts talking about autoencoders, diffusion models. "Sounds interesting — this is what everyone's talking about."

**Step 2**: Ask it to write complete code for a diffusion model. The code appears — completely incomprehensible. Then debug it with the AI, get it running. In the process, start building intuition.

**Step 3**: Start asking line-by-line. For example, there's a ResNet block in the code that performs a bunch of transformations, plus a residual connection that lets data flow through in a specific way to make the model easier to train. At first Gabriel had no idea what was happening.

He kept asking. ChatGPT explained that gradients can flow through these pathways, and without the residual connection, gradients get blocked at certain points. He kept asking until he truly understood.

Then he told the AI: here's my understanding of this concept — is it completely correct?

He also shared some prompting techniques. For example, "explain it like I'm 12" — the AI uses everyday analogies. "Imagine you're in a bookstore, and embedding vectors are like different books…" — connecting AI concepts to the real world.

Gabriel summarized this process as **"recursive gap filling."** There are two core skills: first, **perceiving what you don't understand** — "wait, do I actually understand this part?" That's actually hard and requires deliberate practice. Second, **knowing when you truly get it** — that "oh, it clicked" moment.

> "Chase those clicks. Make them happen as frequently as possible. That's your objective function."

He compared the two paths:

> "Top-down: three days to learn diffusion models. Bottom-up? Six years before you even get there."

![[raw/00-clippings/images/27f17c0325f9555dee74916969bfe231_MD5.jpg]]

And in those six years you're doing Calculus 1, Calculus 2, linear algebra, intro to machine learning… Plus — six years ago, how would you have even known you wanted to study diffusion models? That's the real problem with university. You spend three years before discovering whether you actually like the direction you chose.

Gabriel also emphasized limits. He said academics "have done incredible work, have done research that is tremendously important to the world, and I absolutely do not look down on these people. The only thing I look down on are the concepts that come packaged with the old way of thinking."

## [4] Daily Life on the Sora Team

Sigil asked how he uses ChatGPT at OpenAI to build world-class video models.

Gabriel said many people ask him this, imagining his work is somehow special. It's actually quite direct.

> "You watch videos, find something that doesn't look right. Then you go change the model architecture, or change the data. Train the model, look at the results, stare at the videos for a while. 'These videos are better, great, this goes into main.' Then loop. What's the next thing to fix? What's the next thing to try?"

[Note: Sora is OpenAI's video generation model. Sora 2 was released in late 2024, and Gabriel is listed as a research contributor to that version.]

AI's role in this process: dump the entire codebase into the AI, ask it for 10 improvement suggestions, get paper recommendations, and use it to help discuss approaches with colleagues.

His paper-reading method is also distinctive. He doesn't read papers word for word — he asks the AI: compared to existing methods, what specifically does this paper do differently? Give me a list, as specific as possible. Most papers can be dropped after reading the summary; only the ones he decides to implement get a deeper read. And "deeper read" might just mean when he hits a bug.

His typical approach is to have the AI implement the paper's method directly into his codebase, then copy it in.

> "But I read the code carefully. I'm not vibe coding — I have very strong opinions about my code."

Sigil pressed on this distinction. Gabriel said what he wants is to **"take shortcuts to understand all the fundamentals"** — not "take shortcuts to skip understanding."

> "People's first instinct is always: you just want to cut corners, you don't want to really understand, you want to use AI to fake it. I do want shortcuts, but my shortcuts are to understand all the fundamentals. That's a very important distinction."

He says he asks the AI a hundred questions a day. He'll write code, throw it in: is this good? Are there bugs? How can I write this more simply? "Sometimes it says everything looks fine, but sometimes it says 'you have a bug here' or 'you could simplify this.' You're constantly learning."

He also noted that human opinions remain very valuable, especially for judgment calls. "AI training data comes from all the opinions on the internet — sometimes the opinions are strange. Working with the best people is still very important. But AI can give you 95% now."

## [5] From Stockholm to San Francisco — The Contract Strategy and the Stack Overflow Visa

After leaving Depict.ai, Gabriel always knew he wanted to keep working at startups, with San Francisco as the goal.

His strategy was **only taking contract work to stay mobile**. "The biggest mistake people make early in their careers is staying at the same company too long."

Every time he joined a company, the first thing he did was "interview the people interviewing you." Do you do code reviews? Will you actually review my code and tell me what I did wrong? He deliberately sought out teams with extremely high code standards.

While at Dataland, he worked with an engineer who loved teaching and demanded perfect code. This person would leave hundreds of comments on every PR.

> Gabriel would call him and say: that review was great, let's go through every comment together. He'd probe the first principles behind every suggestion.

He says becoming a good engineer is very hard — it requires understanding a huge number of first principles and building intuition. "Once you know them they're simple, but learning them can be really hard. Having someone just tell you, and being good at absorbing it — that's a massive advantage."

And now, AI can provide that kind of feedback at any company, at any time. "It can be 4am and you're still coding, and you can still ask the AI why this decision is better."

The road to America wasn't smooth. He initially started a J-1 visa (similar to an internship visa) at Dataland, because everyone thought O-1 was impossible. [Note: The O-1 visa is a US non-immigrant visa for foreign nationals with extraordinary ability in sciences, arts, education, business, or athletics — sometimes called the "Einstein visa."]

After a company change, he decided to leave. He spent a few months in San Francisco on an ESTA tourist visa, meeting people. Then he joined Midjourney. [Note: At Midjourney, Gabriel built a high-performance web image grid, internal hyperparameter tuning tools, and a dataset explorer.]

During his time at Midjourney, he started thinking O-1 might actually be viable — and discovered there were many "creative paths" to applying for one.

For example, he used his **technical answers on Stack Overflow** to satisfy the "academic publication" standard. His posts had millions of views, came with a rigorous peer-review mechanism (the voting system removes incorrect content), and had helped a huge number of developers.

> His cousin had once told him he was "wasting time answering Stack Overflow questions." Gabriel said: "You don't know — maybe it'll be useful someday." It was.

![[raw/00-clippings/images/14260d535a30743ea0879119e961924d_MD5.jpg]]

## [6] How to Get a Job Without a Degree — The Demo Methodology

Sigil asked: if you're a nobody from the middle of nowhere, how do you show important people your value?

Gabriel's answer: **build a demo.**

But he immediately added that the hard part of a good demo isn't technical. "A lot of people think demos are hard to build because the technology is hard or they don't have enough skills. That's not it. You don't need much programming knowledge to build a really cool demo."

The hard parts are two things: **letting someone understand what they're looking at in 3 seconds**, and **letting someone understand you're a good engineer in 3 seconds**. "You get one shot — out of 100 applicants, someone clicks your link. Three seconds."

Then he compressed all job-hunting advice into one sentence:

> "Companies just want to make money. If you prove you can help them make money and you can write code, they'll hire you."

What about traditional job-hunting advice? Degrees, internships, extracurriculars, debate championships?

"An interviewer asks what you've done, and you say 'I optimized a process and improved efficiency by 30%.' OK, I still don't know if you can do this job. You went to Harvard and got good grades? Still don't know. You're a debate champion? Still don't know."

He said these things are valued solely because no one can directly prove they can do the work. **Since you can't see what someone's actually capable of, you fall back on degrees, résumés, and awards — indirect proxies to guess whether someone is any good.**

![[raw/00-clippings/images/a6221ac4f28cb0c50e0e9d03358524d3_MD5.jpg]]

Then he made an interesting observation: who relies most on these indirect proxies?

CEOs never care. They just want to make money. You say "I can help you make money" and they say "great, here's a task." **The further you are from the CEO, the more they care** — because their incentives have shifted. It's not about making the best decision; it's about not making a mistake.

> "How does a hiring manager ensure they don't make a mistake? Hire someone from a top school. If that person performs poorly, 'Can you blame me? They went to a top school.'"

His advice: **bypass people without incentives.** Don't go to hiring managers — they're often not even technical and can't assess your quality. Go directly to tech events, talk to founders, show them what you've built, then offer: "Want to try working together for a week for free?"

"100% of people will say yes. They have nothing to invest — they just get to see if you're any good."

> "After your first real job, no one will ever look at your degree again. You have actual things you've built — what's a degree for at that point?"

He added that this advice is for people who truly want to go all-in on their careers. He would also tell friends to go to college — it's a lot of fun, you make friends, you even learn things, just not efficiently. "You still get those things, just less efficiently."

## [7] Why Professors Are So Angry

Sigil pulled up a few of Gabriel's posts on X for him to expand on.

One said: "Universities no longer monopolize foundational knowledge. Here's how I, as a high school dropout, used ChatGPT to learn the core intuition behind diffusion models."

Another was sharper: "I'm currently doing a job that traditionally requires a PhD, with zero prior machine learning or math experience, entirely via ChatGPT. I'm not sure what more evidence is needed to show that ChatGPT has reached PhD level."

Gabriel explained why academia reacts so strongly. "If you're a professor who has spent your whole life telling people why going to university matters, and someone suddenly says you don't need to — the smartest people, if they start self-teaching, won't go to university anymore, and the professor's status diminishes. **Their identity is threatened.**"

> "People spent 10 years doing something, and then a high school dropout shows up, learns it in a few days, and gets the job. That hurts. When I write things like this, it's going to hurt some people's feelings. Honestly, that's somewhat the point — because these people are preventing others from entering the fields they want to enter."

Sigil used the analogy that university in many ways resembles "adult daycare." Gabriel added that in Sweden especially, university is free and comes with a stipend. "Someone tells you 'here's free money, you can keep delaying your decisions.' And there are whole programs where you don't have to decide anything — you can wander around for five more years."

> "People love to delay decisions. Because making a choice feels like permanently deciding what you're going to do with your life. It's not, but it feels that way."

He also gave an example: someone spends five years studying law then pivots to marketing — higher salary, happier. And people around them say "didn't you just waste five years?" "That question is strange to me. This person upgraded both their life satisfaction and their salary. How is that a waste?"

## [8] 70% of People Are in Permanent, Mild Suffering

Sigil asked: what advice do you have for people who don't know what they want to do?

Gabriel said he's seen too many people in this situation, and he's been there himself. From late elementary school onwards: "I wanted to make money, I wanted to succeed, but I wasn't sure what that meant because I hadn't seen anything — I didn't even know what a startup was."

So you go online and search "how to make money," do surveys for a few cents, and think "oh my god I'm making money online." No one tells you where to start. Adults just say "go to university, check back in eight years."

His advice: **do real work as fast as possible.** There are millions of startups in the world willing to accept free labor. Go on LinkedIn, find founders in stealth mode, message everyone: "I want to try working with you for a weekend, zero commitment, I'll do anything."

"Every single thing I've done in my life that wasn't moving toward gaining real experience — like reading textbooks in middle and high school, building good habits, waking up early to run, feeling super productive — all of it was meaningless. If you're not simultaneously doing something that actually matters, those are all zeros."

Then he unpacked that viral X post:

> "70% of people are in permanent, mild suffering because they're allergic to any difficult decision, and whenever 'do nothing' is an option, they choose it."

He gave a specific example. He has a friend in Sweden making 50% above average salary — a comfortable life. Gabriel spent a year convincing him to apply for jobs in San Francisco. "Your salary could be 10x, you'd work with better people, build products that actually get used."

The friend always found reasons not to. The brain automatically blocks you from thinking about it — applying for a job is too painful: prepping for interviews, risk of rejection, negotiating an offer, telling your current boss you're leaving.

In the end Gabriel directly introduced him to a company. "Once the interview starts it gets easy — the company pulls you forward." The friend got an offer. **His salary went up 10x.**

"He lost the equivalent of buying an apartment in Sweden by procrastinating on something that simple."

On taking advice, Gabriel has a framework. He almost never listens to advice — only a handful of people make the cut, most importantly his cousin.

> "Opinions almost always follow incentives. Someone who spent five years in university and never seriously thought about their career — ask them what you should do, and of course they'll tell you to spend five years in university. They mean well, but their advice is completely meaningless. They've only taken one path, never compared it to anything else, and psychologically can't allow themselves to admit they might have taken the long way around."

On parents, Gabriel's experience is unusual. His parents sit at the extreme low end of the spectrum of projecting themselves onto their children. Their only academic expectation was a passing grade. Gabriel was angry about that when he was young — he felt they weren't pushing him. Later he realized this "low expectation" gave him complete freedom to experiment.

He's observed the other extreme: parents projecting their own unfulfilled dreams onto children. "You're going to be a doctor, a lawyer — that was my dream and it should be yours." These parents genuinely believe they're acting in the child's interest, but it's often self-driven. "I want my child to do this so I can brag to the neighbors."

## [9] Why Come to San Francisco

Gabriel attributes San Francisco's pull to **talent density and capital flow**. "Your first week here, your worldview changes. 'My god, I didn't know there were so many people in the world who care about what I'm doing, and they're all in the same room right now.'"

He compared it to motivational videos. "This is real motivation. Not someone standing on a stage saying things that sound nice. This is real — people who think like you, do what you do, work as hard, care as much. They're not nine-to-five."

He made a bold estimate: "San Francisco alone probably outproduces all of Europe. The capital in San Francisco alone probably exceeds all of Europe combined. Apple, Google, OpenAI, Anthropic — all headquartered here."

Advice for those wanting to come: **get good first.** "You need to demonstrate enormous value, because the company has to handle your visa process — that's extra hassle for them. They'd naturally prefer to just hire a local. But truly excellent software engineers globally are extremely scarce, and doubling the number of excellent engineers in America still wouldn't be enough."

Near the end of the conversation, Gabriel shared a retrospective insight. Growing up in a small Swedish town, one of the biggest obstacles was feeling like he wasn't smart enough. "You see people building rockets, doing incredible things, and you think there's no way you could do that. But people underestimate what they can do way too easily."

He said that just the people listening to this podcast are probably already in the top 1%. "Most people don't have the initiative to spend an hour listening to a podcast to improve themselves. You're already in the top 1% — and the top 1% means you're among the people at the world's top 200 startups. Just keep going."

Sigil's closing words: "You might be one of the best people in the world at using AI to learn." Gabriel smiled: "I hope more people can do it better than me, so I can learn from them."

---

## Q&A

**Q: What is Gabriel's core learning method?**
A: "Recursive gap filling." Start from a real problem, use AI to ask layer by layer, and whenever you hit something you don't understand, keep digging deeper until you truly get it. The core skills are identifying your own knowledge blind spots, and recognizing when you've actually "clicked."

**Q: How do you get a good job without a degree?**
A: Build a demo that lets someone understand your abilities within 3 seconds, go directly to founders or decision-makers to show it, and offer to work for free for a week. Bypass hiring managers — their incentive is to avoid mistakes, not to find the best person.

**Q: How did he get a US visa?**
A: He built enough industry influence while at Midjourney, then applied for an O-1 extraordinary ability visa. He used his high-quality technical answers on Stack Overflow as a substitute for the traditional "academic publication" standard.

**Q: What does he specifically do at OpenAI?**
A: Research scientist on the Sora team. Daily work involves observing video generation results, modifying model architecture or training data, training the model, evaluating results — on repeat. Heavy AI assistance, but insists on understanding every line of code.

**Q: Does he think university is completely useless?**
A: No. He sees university as a fun experience where you make friends and learn things. But the teaching approach is inefficient, and universities no longer have a monopoly on access to foundational knowledge. For people with strong career ambitions, he recommends getting into real work as fast as possible.

---

Source: Extraordinary podcast, Gabriel Petersson interview

[https://www.youtube.com/watch?v=vq5WhoPCWQ8](https://www.youtube.com/watch?v=vq5WhoPCWQ8)
