

https://www.youtube.com/watch?v=NgWujOrCZFo&list=PLkDaE6sCZn6GMoA0wbpJLi3t34Gd8l0aK&index=1

![](images/Pasted%20image%2020260227110646.png)

- Concept Drift (different light conditions, ...)
- Data Drift

![](images/Pasted%20image%2020260227110914.png)

![](images/Pasted%20image%2020260227111224.png)
![](images/Pasted%20image%2020260227111231.png)![](images/Pasted%20image%2020260227111300.png)
![](images/Pasted%20image%2020260227111549.png)![](images/Pasted%20image%2020260227111733.png)
![](images/Pasted%20image%2020260227111922.png)![](images/Pasted%20image%2020260227112248.png)![](images/Pasted%20image%2020260227112431.png)
![](images/Pasted%20image%2020260227112650.png)

### Data Drift (The "x" changes)

**Data Drift** is all about the input data changing. The rules are the same, but the stuff you are feeding the AI looks or sounds different than what it's used to.

- **The Speech Example:** Imagine you trained your speech recognition AI using super crisp audio from fancy recording studios 🎧 (your training set).
    
- **The Drift:** Suddenly, your real-world users are talking into cheap phone microphones while walking down a windy street 🌬️📱.
    
- **The Result:** The language hasn't changed, but the actual audio data (the **x**) is noisier and different. The data drifted!

### 🤯 Concept Drift (The "x $\rightarrow$ y" changes)

**Concept Drift** is when the _meaning_ or the _rules of the game_ change. The mapping from the input (**x**) to the correct output (**y**) isn't the same anymore.

- **The Speech Example:** Think about slang! Ten years ago, if the AI heard "That is sick!" (**x**), the correct translation/meaning (**y**) was "That person has an illness" 🤒.
    
- **The Drift:** Today, a teenager says "That is sick!" (**x**) and they actually mean "That is awesome!" 😎🔥.
    
- **The Result:** The input word is exactly the same, but the correct output has completely shifted. The concept drifted!
### 🐢 Gradual Change vs. ⚡ Sudden Shock

As your notes point out on the right side, these drifts don't always happen at the same speed!

- **Gradual Change:** Language naturally evolving over time, or people slowly upgrading to better microphones over a few years.
    
- **Sudden Shock:** A massive, overnight disruption. Think about how the word "Zoom" went from meaning "to go fast" 🏎️ to "a video meeting" 💻 practically overnight in 2020!

![](images/Pasted%20image%2020260227112907.png)


![](images/Pasted%20image%2020260227112945.png) 
![](images/Pasted%20image%2020260227113052.png)![](images/Pasted%20image%2020260227113530.png)![](images/Pasted%20image%2020260227113633.png)![](images/Pasted%20image%2020260227114658.png)![](images/Pasted%20image%2020260227114749.png)![](images/Pasted%20image%2020260227114840.png)

### 📱 What is a Canary Deployment?

In software and machine learning, a Canary Deployment is a super cautious way to release a new update or a new AI model.

Instead of flipping a switch and giving the new version to 100% of your users all at once (which is risky!), you do this:

- **The Tiny Test Group:** You roll the new update out to a very small fraction of your traffic—like just **5%** of users.
    
- **Watch and Learn:** You monitor that 5% closely. Are there bugs? Is the AI making weird mistakes? Is the app crashing? 🕵️‍♂️
    
- **Ramp up or Roll back:** If everything looks great with the 5%, you slowly give it to 10%, then 20%, until everyone has it. If it fails, you immediately pull it back. The beauty is that you only annoyed 5% of your users instead of breaking the app for everyone! 🙌
    

### ⛏️🐦 Where does the name come from?

The name actually comes from a very real, historical practice: **"The canary in a coal mine."**

Back in the day, coal miners faced a huge danger from toxic gases like carbon monoxide, which are invisible and odorless. To stay safe, miners would carry a small, caged canary bird down into the mine tunnels with them.

Canaries are much more sensitive to toxic gases than humans. If there was a gas leak, the canary would unfortunately faint or pass away long before the humans were in danger. The bird was an **early warning system** 🚨. If the canary stopped singing, the miners knew they had to evacuate immediately.

In tech, we aren't harming any birds! But that small 5% of user traffic acts as your "canary." If the new software update is "toxic" (full of bugs), your 5% canary will "faint" (generate error alerts), giving you an early warning to stop the release before the rest of your users are affected.

![](images/Pasted%20image%2020260227115016.png)![](images/Pasted%20image%2020260227115220.png)![](images/Pasted%20image%2020260227115403.png)![](images/Pasted%20image%2020260227115435.png)
![](images/Pasted%20image%2020260227120702.png)![](images/Pasted%20image%2020260227121007.png)

Here is what you would want to track to make sure your computer vision AI is healthy and running smoothly:

### 💻 Software Metrics (The Engine)

These are all about how your servers and hardware are handling the heavy lifting of processing images.

- **Latency (Inference Time):** How many milliseconds does it take YOLO to process _one_ single image? (Crucial if the conveyor belt is moving fast! 🏎️)
    
- **Throughput (FPS):** Frames Per Second. How many total images can your system handle in a second?
    
- **GPU/Compute Usage:** Is your graphics card maxed out at 100%? 🌡️
    
- **Memory & Server Load:** Standard health checks so your system doesn't crash mid-shift.
    

### 📥 Input Metrics (The "x" - Watching for Data Drift)

These track the actual pictures coming out of the factory cameras. If these change, your model might get confused!

- **Average Image Brightness:** Did a lightbulb burn out on the factory floor? If the images suddenly get dark, the AI might miss a scratch. 💡
    
- **Image Blurriness/Sharpness:** Did the camera get bumped out of focus, or is the lens dirty? 🔍
    
- **Resolution/Image Size:** Did someone accidentally change the camera settings from 4K down to 1080p?
    
- **Color Distribution:** Did the factory switch from making blue phones to red phones? 📱
    

### 📤 Output Metrics (The Predictions - Watching the AI's Behavior)

These track what YOLO is actually spitting out. If these numbers look weird, your model might be broken or encountering Concept Drift.

- **Average Confidence Score:** YOLO gives a % of how sure it is (e.g., "I am 95% sure this is a scratch"). If your average confidence drops from 95% to 40%, the model is struggling! 🤔
    
- **Number of Bounding Boxes per Image:** If the AI usually finds 0 or 1 defects per phone, but suddenly starts drawing 50 bounding boxes on every image, it's hallucinating. 📦
    
- **Null Predictions (Pass Rate):** The # of times it returns _zero_ defects. If your factory usually has a 99% pass rate and it suddenly drops to 50%, either the machines are broken or the AI is wrong. 📉
    
- **Human Override Rate:** How often does a human QA worker have to press a button saying "No, AI, you were wrong, that's just a speck of dust, not a scratch"? 🧑‍🔧

![](images/Pasted%20image%2020260227121101.png)
![](images/Pasted%20image%2020260227121821.png)
![](images/Pasted%20image%2020260227121913.png)
![](images/Pasted%20image%2020260227122038.png)
![](images/Pasted%20image%2020260227122540.png)

![](images/Pasted%20image%2020260227122627.png)
![](images/Pasted%20image%2020260227122722.png)
![](images/Pasted%20image%2020260227122739.png)![](images/Pasted%20image%2020260227122816.png)
![](images/Pasted%20image%2020260227123131.png)![](images/Pasted%20image%2020260227123431.png)![](images/Pasted%20image%2020260227123702.png)

![](images/Pasted%20image%2020260227213816.png)![](images/Pasted%20image%2020260227213858.png)
![](images/Pasted%20image%2020260227213950.png)
![](images/Pasted%20image%2020260227214233.png)
![](images/Pasted%20image%2020260227214332.png)![](images/Pasted%20image%2020260227214421.png)
![](images/Pasted%20image%2020260227214545.png)
![](images/Pasted%20image%2020260227214715.png)
![](images/Pasted%20image%2020260227214902.png)
![](images/Pasted%20image%2020260227215104.png)![](images/Pasted%20image%2020260228144706.png)

The handwritten blue numbers on the far right are where the real decision-making happens! To find the **overall impact** on your entire system, you multiply the **Gap to HLP** by the **% of data**.

Let's look at why this math changes everything:

- **The Trap (Car Noise):** At first glance, you might think, "Oh no! Car Noise has a massive 4% gap compared to humans, we must fix that immediately!" But look at the math: $4\% \times 4\% = 0.16\%$. Because Car Noise only makes up 4% of your total data, completely fixing it will barely move the needle on your overall system performance.
    
- **The Dead End (Low Bandwidth):** The AI is at 70%, and humans are at 70%. The gap is 0%. No matter how hard you work on this, you will get a 0% overall improvement. Skip it! 🛑
    
- **The Winners (Clean Speech & People Noise):** Even though the gaps are smaller (1% and 2%), these situations happen _so often_ (60% and 30% of the time) that fixing them will give your whole system a solid **0.6% boost**. 🏆


📱 Scratched Screen AI: Prioritization Matrix

| **Defect Type (Tag)**    | **AI Accuracy** | **Human Level Performance (HLP)** | **Gap to HLP** | **% of Factory Data** | **Overall Impact (Gap x %)** |
| ------------------------ | --------------- | --------------------------------- | -------------- | --------------------- | ---------------------------- |
| **Clean Lighting** 💡    | 96%             | 99%                               | 3%             | 70%                   | **2.1%** 🏆                  |
| **Glare / Reflection** ✨ | 80%             | 90%                               | 10%            | 15%                   | **1.5%**                     |
| **Dust Specks** 🧹       | 75%             | 95%                               | 20%            | 5%                    | **1.0%**                     |
| **Blurry Camera** 🌫️    | 60%             | 60%                               | 0%             | 10%                   | **0%** 🛑                    |
![](images/Pasted%20image%2020260228145807.png)![](images/Pasted%20image%2020260228145959.png)
![](images/Pasted%20image%2020260228150210.png)
![](images/Pasted%20image%2020260228150943.png)
### 🧠 The 2-Step "Cheat Code"

Instead of trying to memorize the whole acronym, read it **backwards**.

**1. Look at the second word (Positive/Negative):** This is _only_ what the AI predicted.
- **Positive:** The AI yelled, "I found it!" (e.g., "I found a scratch!").
- **Negative:** The AI said, "Nothing to see here." (e.g., "The screen is clean.").

**2. Look at the first word (True/False):** This is reality checking the AI. Was the AI right?
- **True:** Good job, AI! You were right.
- **False:** Bad AI! You were wrong.
### 🏭 Let's use our Factory Phone AI!

Let's pretend $y=1$ (Positive) means "Defective/Scratched" and $y=0$ (Negative) means "Clean/Perfect".

- **TP (True Positive = 68):** AI yelled "Scratch!" (Positive). It was right (True). _We successfully caught a broken phone!_
- **TN (True Negative = 905):** AI said "Clean." (Negative). It was right (True). _A perfect phone safely passed through._
- **FP (False Positive = 9):** AI yelled "Scratch!" (Positive). It was wrong (False). _False alarm! The AI threw away a perfectly good phone._
- **FN (False Negative = 18):** AI said "Clean." (Negative). It was wrong (False). _Oops! A scratched phone slipped past the AI and got mailed to a customer._
    
---

### 🎯 Precision vs. Recall (The Math)

Now let's look at the formulas in your image. They measure two different ways your AI can fail.

**Precision (The "Crying Wolf" Metric)**
- **Question:** Out of all the times the AI _claimed_ to find a scratch, how often was it actually right?
    
- **Formula (Green Circle):** Precision = $\frac{TP}{TP+FP}$
    
- **The Math:** $\frac{68}{68+9} = 88.3\%$. When your AI flags a phone, you can trust it **88.3%** of the time.
    

**Recall (The "Catch 'Em All" Metric)**
- **Question:** Out of all the _real_ scratched phones in the factory, how many did the AI successfully find?
    
- **Formula (Blue Circle):** Recall = $\frac{TP}{TP+FN}$
    
- **The Math:** $\frac{68}{68+18} = 79.1\%$. Your AI successfully caught **79.1%** of the broken phones, but unfortunately, 18 of them slipped through.
- 

![](images/Pasted%20image%2020260228152616.png)


so... why high recall is prefer in manufacturing?
### ⚖️ The Cost of Being Wrong

To understand why factories love High Recall, we have to look at how much money the AI's mistakes cost the business.

**Scenario A: The False Positive (FP) - "The False Alarm"**
- **What happens:** The AI yells "Scratch!" but the phone is actually perfectly clean.
- **The Cost:** A human worker on the factory floor has to pick up the phone, look at it for 5 seconds, realize the AI is wrong, and put it in the "Good" pile.
- **Business Impact:** You wasted 5 seconds of an employee's time. Very cheap! 💸
    

**Scenario B: The False Negative (FN) - "The Missed Defect"**

- **What happens:** The AI says "Clean!" but the phone actually has a massive scratch on the screen.
    
- **The Cost:** The broken phone gets put in a box, shipped across the world, and sold to a customer. The angry customer leaves a 1-star review, demands a refund, and you have to pay for return shipping.
    
- **Business Impact:** Brand damage, lost customers, and high shipping costs. Very expensive! 📉😭
    
### 🎣 Why High Recall is the Winner

Remember our cheat code for **Recall**: It is the "Catch 'Em All" metric.

Because missing a broken phone (False Negative) is incredibly expensive, factories will intentionally tune their AI to be **paranoid**. They want the AI to flag _anything_ that even looks slightly like a scratch.

- **High Recall means:** "We caught 99.9% of the broken phones!" (Almost zero False Negatives).
    
- **The Trade-off (Lower Precision):** Because the AI is paranoid, it will create more False Positives (crying wolf over dust specks). But the factory owners are happy to pay a human to double-check those false alarms, as long as no broken phones make it to the customer! 🛡️
    

So, in the manufacturing world: **It's better to be safe (High Recall) than sorry!**

![](images/Pasted%20image%2020260228153952.png)
### 🕵️‍♂️ Breaking Down the Factory's Day:

- **TP (99) - The Saves:** The AI successfully caught 99 broken phones before they were shipped. High fives all around! 🙌
    
- **FN (1) - The Nightmare:** The AI missed _one_ broken phone. It got shipped to a customer. (But hey, 1 is way better than 18 like in your original notes!).
    
- **TN (750) - The Smooth Sailing:** 750 perfect phones sailed right through the system without an issue.
    
- **FP (150) - The Annoyance:** The AI cried wolf 150 times! It flagged 150 perfectly good phones because it thought a speck of dust was a scratch. A human worker had to spend a few minutes checking these. 🧑‍🔧
- 
![](images/Pasted%20image%2020260228152709.png)![](images/Pasted%20image%2020260228152824.png)

![](images/Pasted%20image%2020260228154354.png)![](images/Pasted%20image%2020260228162011.png)
![](images/Pasted%20image%2020260228162526.png)
![](images/Pasted%20image%2020260228184049.png)![](images/Pasted%20image%2020260301211843.png)
