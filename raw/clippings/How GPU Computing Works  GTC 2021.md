---
title: "How GPU Computing Works | GTC 2021"
source: "https://www.youtube.com/watch?v=3l10o0DYJXg"
author:
  - "[[Dan the Man]]"
published: 2022-07-05
created: 2026-07-06
description: "www.nvidia.com/en-us/on-demand/session/gtcspring21-s31151/"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=3l10o0DYJXg)

www.nvidia.com/en-us/on-demand/session/gtcspring21-s31151/

## Transcript

**0:00** · i'm stephen jones um i'm one of the architects of cuda and so my my job is literally to think about how we program gpus um what programming languages need to look like what the what the hardware needs to look like to support those programming languages and so i spend a lot of my time really just thinking about how computing works i i've i've actually

**0:22** · um typically not really given it's not really a talk i've just drawn this on a whiteboard for intern pretty much every summer uh and i thought it might be interesting for for all of you at gtc to just sort of have a sketch out of how i perceive the gpu working and and the kind of constraints that the hardware imposes on how you program it you'd be you'll be very surprised to discover i think the the extent to which the the laws of

**0:48** · physics and the nature of the hardware are what govern all the way we program these machines so i named this talk how gpu computing works but you know i was thinking really i should be named why gpu computing works right because if you understand what's going on you'll be much much better at getting it to do what you want but then i thought that a bit more and i realized that actually the title should be in where's my data because ultimately

**1:13** · you'll discover that's the thing that counts right i'm going to tell you about how gpu computing works but you'll see it really comes down to the question of where's my data so i'm going to start with a statement that some of you might feel a bit contentious i'm going to claim that nobody cares about flops right flops is

**1:31** · a floating point operations per second it's the mathematical horsepower of the machine and so most people when they when they when they buy a machine how many flops does it have and and i'm telling you you really should not care that is not the question that matters well since i'm amending titles it's not the question that matters to almost all of us there's probably one or two people who care and there's one really really important algorithm which really really cares about flops and that's important and i'll get to that later but but honestly almost nobody really cares about flops

**2:03** · so why do i think nobody should care about flops well if you look at a modern cpu with this attached memory that memory can feed data to the cpu at around 200 gigabytes a second but the cpu can compute around 2 000 giga operations per second that's two teraflops these numbers are absolutely typical for you know a modern processor

**2:25** · so that 200 gigabytes per second of course is 25 giga doubles a second if you like because each double is 8 bytes and so my memory can provide 25 billion double precision values per second that's a lot but my cpu wants to consume 2 000 billion double sin values per

**2:44** · second right and the ratio of these two things is what's called the compute intensity of the device right it's the amount of work the device needs to be doing to account for the fact the memory can't feed it as fast as it needs to be found

**3:01** · in this example i need to do 80 operations just to break even right i need to do 80 operations on every single piece of data that i move otherwise i'm not keeping my processor busy and i should have bought a cheaper cpu right that's a pretty tall order 80

**3:16** · operations and not many algorithms which have that much to do on every piece of data in fact there's really only one extremely important one matrix multiplication and i'll get to that later so here's a quick table of a few different processes and and you can see everything runs in more or less the same space for compute intensity uh which is bad news for my program it's actually pretty interesting that it works this way um you know the

**3:40** · nvidia chip has way way way more flops but it also has much much higher memory bandwidth to balance it out that's not an accident you're always trying to keep your computer intensity as low as you can because honestly no algorithm can do 100 things per load or 134 things per load but the the dirty secret if you like of computing is that every single generation i can add flops faster than i can add memory bandwidth so that compute intensity number goes up

**4:08** · and so you were in a constant fight in in programming algorithmically to try and keep these new newer and newer chips busy they are monsters and they need more and more data and so a lot of what i'm going to tell you is about the challenge of this and how it's shaped and colored the way we program these machines

**4:26** · so the reason i don't think flops matter is honestly we've already got enough of them and and it's only getting worse if i can't keep my cpu busy i'm in what's called a memory bandwidth limited mode and honestly the vast majority of programs fall into this camp i i would guess you know at least three quarters more of all programs that i encounter are completely limited by memory bandwidth because 100 things per load is just hard

**4:54** · actually that's not even the whole story the thing we should be caring about i'm going to say is latency we should also be caring about bandwidth and of course about flops but let me tell you about latency for a moment so why should we care about latency well

**5:10** · let's look at the simplest operation in the world right ax plus y that's something that's called uh dax b if it's in double precision stacks b if it's in single precision um you see a lot of benchmarks about this and you should pretty much ignore them all uh this is a building block right it's very it's a very common very important instruction so much so the processes have this dedicated instruction called fma if you'd multiply add that does it in a single instruction so i can do all of

**5:35** · these things together and and notice i'm counting loads not stores because i don't care about stores because i don't wait for them this is the loads that i have to wait for counterbalance against the flops that i need to do to cover the amount of time that i spend loading it so latency let's look at a timeline right first i'm going to load x then loading y doesn't depend on x because you know alpha times x and plus y

**6:05** · so i'm also going to send a load request for y and then i'm going to wait a really long time until x counts back a really stupidly long time then it gets tricky two things kind of happen at once i immediately kick off the alpha times x multiplied because x is now there and i can start doing that work and so times x takes some amount of time

**6:26** · much much less than the latency and so by the time alpha times x is ready to be added to y or the y load has arrived the y load has effectively come in for free right i hit it behind the x followed by the alpha times x we call this pipelining it's where i've got extra memory operations underway but they're hidden by other useful work pipelining is really like the the key

**6:49** · fundamental of programming you may not think about it too much in programs that you write but the compiler is really just spending almost all of its effort pipelining things making sure that loads for example issued as early as possible so that they can be covered by as much other competition as possible the compiler moves tons of your code around for exactly this effect this

**7:10** · pipelining is the core of most program optimization and it's the core of the program optimization because memory is so important right and the problem here is that the memory latency is huge compared to the computer latency so why well physics right the speed of light is really really really fast but my computer clock is also really

**7:38** · really really fast so the single clock tick light travels only 10 centimeters that's four inches to americans but uh you know si units come on it's about time anyway so really the clock is going so fast that light doesn't travel very far electricity travels about a fifth as far as light when it's in silicon uh the physics is actually pretty complicated but this is kind of a decent rule of thumb that means in a single clock tick electricity just traveling 20

**8:07** · millimeters so if you think about the die size of a chip right i'm that's one or two clock ticks simply for electricity to go from one side of the chip to the other not even doing anything just just literally traveling as fast as it can in a straight line so when you start seeing

**8:24** · reports of processes with latencies of you know five or six or seven clock cycles of latency that is astonishing that is a point where the speed of electricity is competing with the speed of my computing so the laws of physics are getting in the way when i have to fetch stuff from memory my memory is five or ten clock ticks away and another five will tend to come back but actually the problem is not really the distance to my memory

**8:49** · the problem is actually all the transistors are in the way because the way that circuits circuits work is you're handing off signals from one bank of transistors to the next as you go through all of the logical operations inside your device right so they switch on and off the clock rate the electronics only advance as fast as the clock ticks so so speed of light is a factor but it's not the biggest factor really the the depth of my of my transistor pipelines is a bigger factor

**9:17** · so i'm spending a lot of time waiting for my data what does it mean right what let's we can do some calculations and see and see what this is costing us if you remember i paid too much for my cpu because i can't keep my cpu busy uh i've got too many flops and so i want my memory to be running flat out all the time right so i picked some numbers for the xeon 8280 uh i may

**9:39** · i pick them really just because latency numbers are available for it um it's got 131 gigabytes of memory and a latency of 89 nanoseconds it doesn't you'll see it doesn't really matter which specific chip we pick uh i'm so this is the top of the line of of that family of theons if i've got 89 nanoseconds and i can move 131 gigabytes per second that means i can move in one memory latency 11 659 bytes

**10:08** · pretty good however dax b loads just x and y that's two 8 byte values 16 bytes of data in that time for an overall efficiency of 0.14 that is not very good so even if i've got high bandwidth memory to fight my computer intensity i'm barely using any of it right i spent way too much money on both my cpu and now my nice high performance memory

**10:36** · so i can chart the latency for the set of processes that we're looking at and you can see that honestly all of them do terribly in fact the 0.14 of the 8280 is the best of the bunch right and this is because my program is what's called latency bound it's another form of memory limitation and it actually happens a lot more than you realize um you can see why i don't really care about flops at all because i've got i can't keep my bandwidth busy

**11:03** · let alone make my my flops busy the gpu interestingly does far far worse than the rest right and this is where the how the gpu programming works part comes in obviously i'm going to be elaborating on that a lot more but um let's just talk about from what i can do about this this problem right if i divide 11 659 by the 16 bytes i find i need to be doing 729 simultaneous iterations of daxp

**11:31** · to be able to make it worth the money i spent on my memory right so for that low memory efficiency i need 729 things at once first we can attack with concurrency concurrency is having a lot of things in flight at once right they don't have to be simultaneously simultaneous sorry they just haven't just just have to be happening independently compilers have an optimization called loop unrolling and that's where they

### LOOP UNROLLING

**11:54** · they find independent independent considerations uh and they're issued back to back all at once so there's all their own flag remember we loaded x and y back to back and we can do this many times by unrolling the loop it's limited fundamentally by how many operations the hardware can keep track of there's only so many things the hardware can can stage uh in a pipeline before it it just has to wait for things to come back it's going to track every single request right so note i'm also still calculating with just the one thread so even if i had 729

**12:26** · um things unrolled which basically never happens and i my processor could handle 729 outstanding loads by my thread i would then have to do 729 calculations at the end so so loop unrolling is good it gets me more pipelining but it's obviously limited by various other pieces of the architecture of the machine

### THE ONLY OPTION IS THREADS

**12:47** · so parallelism is stronger than concurrency right it means things happen at the same time things that are in parallel are simultaneous so while loop unrolling gave me lots of operations back to back parallelism literally issues one operation per thread simultaneously up to the limit of the hardware however many threads the hardware can handle right so in reality i can do

**13:09** · both loop unrolling and multi-threaded operations and that again allows me to use fewer threads but just just for the simple sake of this example let's just let's just look at the hardware limit on how many threads we can run so now i can add a few more rows to my table right i can look at how many threads do i need in an ideal world to

### COMPARISON OF DAXPY EFFICIENCY ON DIFFERENT CHIPS

**13:29** · cover the latency of my memory system it turns out i need a lot but this is where a really interesting difference emerges right the gpu has a much higher latency and a much higher bandwidth which means it needs approximately 40 times as many threads to cover it but it actually has a hundred times the number of threads the other processes right so the gpu actually does a lot better i have five five and a half times more threads than i need whereas the the cpus the additional cpus they're in sort of like 1.2 inch type range right this is the

**14:03** · most significant design point of the gpu if you remember only one thing from this whole whole talk remember this the gpu has a lot of threads far more than you need because it's designed for over subscription it's designed to have tons of threads working so that if someone waiting on memory there are plenty more left to be active the gpu is what's called a throughput machine you the designers of the gpu put all the resources into adding more threads instead of cutting latency

**14:33** · by contrast of the cpu it's a latency machine the expectation of the cpu is that a single thread is largely doing all the work it's expensive to switch out these threads from one to another it's a context switch so you only need just about enough threads to cover the latency so the cpu designer puts all their resources into cutting latency instead of adding threads they're two completely opposite

**14:57** · approaches to attacking the same latency problem and this is really the root of the fundamental difference between how the gpu runs work and how cpu runs work so finally after 30 slides i'm starting to tell you about the gpu um look i've only been talking about general process of things and that's that's because these are the challenges of physics right of electronics you can see from the previous slide that the gpu solves these same problems completely differently from the cpu but

**15:27** · memory is what matters all programming is about memory it's about memory bandwidth it's about memory latency it's about about where my data is in my memory but the gpu takes a very different approach and that is what this talk is all about that's that's why i'm telling you about how the gpu how vp programming works so here are the memory numbers right and the story here is cache

**15:53** · notice i've included the register file as one of the caches this is actually really a really important gpu detail the gpu excuse me the gpu uses a very large number of registers in each thread to keep live data around at a very low latency because it's got a long latency to each one of its different set its different caches compared to a cpu so it needs memory

**16:17** · immediately up close and it needs enough of it to be doing useful operations there's more than that when you issue a load operation you say x equals some pointer then the hardware needs a place to put it so i say load from memory into put the

**16:34** · result in my register so i can compute with it so the number of registers that i have directly relates to the number of memory operations i can be doing this means the gpu can maintain in principle 27 megabytes of outstanding load data right that's the number of of of um the number of total registers in the system that's 3.3 mega doubles if we

**16:58** · want to work in our double precision universe of outstanding load data that's humidor that's huge and it's very very different from the cpu the cpu uses registers so the gpu uses redis as a buffer to hide latency as well as a way to avoid latency by having its data close up so a large registered account is really fundamental to the way the gpu operates as well so you've been wondering why i've been talking about threads and bandwidth when cached the solution well this is why because threads is actually

**17:30** · the reason why we can get away with caches at different latencies so let's look at the bandwidth and latencies if i imagine gpu main memory that's that's the high bandwidth hbm memory if i imagine gpu main memory to be my unit of bandwidth right however fast that goes that's one

**17:50** · then my l2 cache is three times five three times the bandwidth and likewise my l1 cache which is uh also my shared memory i'll get to that in a minute is 13 times faster right so my bandwidth remember as my bandwidth goes up it's it's more easily able to satisfy my compute intensity so this is good i want to be running out of cash if i can be to satisfy my computer intensity at the same time if i look at my l1 cache the memory that is physically closest to me if that is a latency of one times my l2 cache is five

**18:22** · times longer and my main memory is 15 times longer than that right now compare this with the off chip bandwidth and latency and you'll see very rapidly why you really really want to run with all your data local on your gpu moving data across the pci bus is a it's the biggest bottleneck by far

**18:43** · so we can use all these bandwidths and all the latencies to see what the compute intensity is is like right what the compute intensity that's required to operate out of each layer of memory right my hbm that was my compute intensity of 100 that we looked at earlier my l2 cache has a compute intensity far better you know it's just 39 operations per load that are needed

**19:03** · and my r1 cache only 8 is a very achievable number this is this is why the l1 caching the shared memory and the gpu are so useful because i can start i can actually start having my data close enough that i can meaningfully do eight operations and start saturating my flops

**19:20** · right so i really want to be running out of cache if i can be at the same time i really really don't want to be running out of pcie right the band with the pcie is so bad and the latency is so horrible that you know i need to literally do an incredi an inconceivable number of operations nv link i've put in here it's not shown because it's the gpu gpu link but it's interesting that envy link is much closer to the main memory domain that is the pci domain this is why nvlink is a much much better interconnect between between chips and between gpus and then

**19:52** · the pci bus if we look at the required number of threads to hide this latency here's an interesting thing right you'd think that you would need fewer latest fewer threads because the latency has gone down but remember that bandwidth is also going up you need almost the exact same number of threads for my main memory as

**20:13** · i do for my l2 cache as i do for my l1 cache and this is no accident right if you think about it you want to be able to keep the entire memory system completely busy all the time right because my computer intensity is high and i need to feed the cause so if there were one part in this memory system that needed more threads than any

**20:32** · other i would find that that part was a bottleneck i would have to add more threads to satisfy that part and then i'd have too many for the other arrow too many threads for the for the other parts of my memory system it's the hardware designers intentionally balance things to make things evenly programmable across the whole device

**20:51** · so excuse me inside the inside inside hsm an sm is basically a processing call i've got 108 of them on the on the a100 gpu um an sm is basically a protein core and there's a lot going on in here but effectively the thing to keep in mind is it's running everything in groups of 32 threads called a warp and the warp is it's basically the vector width of the machine 32 threads in the walk and i run four of these at any time so at any given clock tick i've got four warps doing something

**21:23** · i've got 64 warps sitting around waiting we've got four of those 64 doing something the the gpu is built with all these sms and all these threads in each sm this is part of the whole strategy remember the gpu designers fight latency by adding threads rather than finding latency by cutting latency down

### THE GPU'S SECRET SAUCE: OVERSUBSCRIPTION

**21:45** · so i can have a lot more threads alive than running at any time 2048 in any given sm but only 128 of them running at a time right this is the idea i was talking about that the gpu was oversubscribed so when some threads are off waiting for a read latency other threads have presumably received their response and are ready to go this is the entire secret to how the gpu works it can switch between warps

**22:11** · instantly within a single clock cycle so there's no contact switch overhead at all right it can literally run threads back to back that means it's very important to have way more threads alive than the system can run at any time because this is how you compensate for the latency it's literally the opposite of the cpu where you never want to work subscribing your threads excuse me the gpu is a throughput machine

### THROUGHPUT VS. LATENCY

**22:38** · so let's talk about throughput versus latency i've been saying those words a lot let me explain them to you for a moment so so i live in san francisco and i work in santa clara um so so yes my commute sucks and and also yes there is literally a permanent traffic jam just north of san mateo so i have two choices of getting to work i can take my car which takes 45 minutes or i can take the train which takes 73 minutes my car is optimized for latency

**23:05** · while the train is a throughput machine i'll show you how that works the problem with taking the car is it does one thing as fast as possible but it doesn't really help anybody else it's fast it's not very efficient it only carries a handful of people and it goes from one place to another

**23:25** · train on the other hand there's a lot of people it stops a lot of places so people all along the line are helped they can have a lot of trains along the route so another thing about latency systems is that if they get oversubscribed they're horrible everything downs to a hole right if i've got too many cars on

**23:43** · the road nobody's going anywhere the train is full you just wait for the next one and while you're late you're not going to be three hours late because there's always another train coming so the gpu is a throughput machine it's designed for way more work than it can run on time and so just like if your trains aren't full you're not making the best use of the train system that's true for the gpu as well right so throughput systems want

**24:06** · deep queues of workers waiting to go the train company intentionally keeps you waiting on the platform because if it comes to a station and nobody's on the platform the train isn't full and they're wasting their money right the gpu just like the train needs to be kept busy the cpu is a latency

**24:23** · machine switching threads is expensive so you want one thread to run as fast as possible but if things get congested everything stalls right so the aim is to do everything as quickly as possible then get out of the way for the next thing i want my car on the road getting to work off the road because the road has a limited number of cars that it can be running so just to recap we've got all these threads to solve our latency problem and

**24:48** · that's great i've sold our latency problem we're now up against banner everything is set up as a throughput system so i'm always oversubscribed and being oversubscribed means i always have work to do while my memory is being fetched so now i have to think about asynchrony the most important thing to remember is the cpu and the gpu are independent processors that means that they can work on different things at the same time and they should work on different things at the same time if you make your cpu stop while the gpu is running you make the gpu stop while the cpu is running it's like everyone having to get off the train at every station and wait for the

**25:18** · next train and then get back on right you might as well only have one processor so asynchrony nobody stops the cpu would issue work to the gpu and that it carries on doing its own thing while the gpu does its thing you only wait for the end result

**25:36** · to stretch the analogy for a moment probably a little bit too far if you want to move a lot of things at once you want a lot of lanes like this road on the right your traffic moves asynchronously nothing gets blocked by what's ahead because you've got enough flow uh to be fair the road on the right stands no chance of being blocked at all if you're synchronous you've only got one lane of traffic everybody waits for the slowest thing everybody waits for everybody else so asynchronous is really important in being able to achieve the throughput that we're looking for

**26:05** · so in the real world it's actually rare that you find work where each element is completely independent from the others dax p is one such example these are called element-wise algorithms and only the simplest algorithms tend to work this way most algorithms require at least one or more surrounding elements like convolution for example that brings in all of its neighbors some algorithms like the fourier transform require every element to interact with every other one these are called all to all algorithms and each of these behave pretty differently

**26:37** · okay so let me show you how parallelism works on the gpu how how we're going to get the throughput that we need so let's say i've trained an ai to recognize cats on the internet so so here's a picture of the cat i'm going to overlay the cat with a grid and that grid is going to create many blocks of work i'm going to work separately on each block right the blocks are independent from each other they're working on a different piece of the image and there are loads and loads of blocks so the gpu is over subscribed with them so remember

**27:07** · remember that over subscription is what we want for efficient execution and peak memory use so each block comprises many threads working together so that those threads can share data and achieve a joint task all the threads in the block are running simultaneously in parallel right so now i have my hierarchy i've got the total work on the left that is broken down through a grid into blocks which provide the over subscription the gpu needs and then i've got blocks of a smaller number of local threads all of which are working together on a task

**27:39** · so now i've trained an ai to process the image for me those threads work together they they work on their their tile their block and remember each block is running independently all of their own pace and eventually my whole image is going to be done and my internet will be one picture safer so work runs on the gpu is a grid of all the work to be done that's broken down into blocks of threads right each block has parallel threads and threads which are guaranteed to be running at the same time so they can share data

### CUDA'S HIERARCHICAL EXECUTION MODEL

**28:08** · but all blocks are scheduled independently in over subscription mode this gets me the best of both worlds right it gets me the the throughput that i need to keep the machine busy but it also allows some number of threads to interact together with each other this is the essence of gpu programming is to break your problem

**28:26** · down into blocks of things where cooperating threads will work together on it but each of the blocks are relatively independent so at this point we've beaten latency right our latency is covered by over by oversubscription remember i said latency was really the thing you should care about all of this loads of threads over subscription programming models of grids and blocks and threads running in my blocks all of that is really fundamentally to fight latency and we've done it and we've won and we

### BEATING COMPUTE INTENSITY IS ALL ABOUT SCALING

**28:55** · are now back to being limited by bandwidth which in turn brings us back to compute intensity and flops right we need to boost our the amount of work that our algorithms are doing and and that's just simply hard to do

**29:11** · right now i've got a lot of threads i've got 5.6 times more threads than i need according to that table and and so the question is if i throw threads of the problem what does that do and it comes down to algorithmic algorithmic complexity and that is if i increase the

**29:27** · size of my problem the number of things i'm working on and i can do that because i got a lot of threads how many more operations do i need to do so for the element-wise thing for example for each each time i add a thread i'm loading a new element of data but i'm only doing one more operation so i'm adding one thread loading one piece of data doing one more calculation

**29:47** · nothing is actually changing my adding threads does not make my my required number of flops go up at all my arithmetic intensity of the algorithm is flat even something like a like a 2d like a like a convolution or 3d my data now when i grow my square

**30:06** · it scales as n squared but my compute is also scaling as n squared so again the the the algorithmic complexity of these things is is not there the arithmetic intensity scales as well one and again there's no amount of growing

**30:21** · data on a convolution that is going to fight out fight against this computer intensity that my machine requires now all to all starts to get much more interesting right there i have every time i double my number of threads i quadruple the amount of compute i need because all are talking to all suddenly i'm in a much better place suddenly my rf mechanic my arithmetic intensity of my algorithm is scaling up

**30:47** · linearly as the number of threads increases i've got a lot of threads i can throw them at it that boosts the number of flops that are required and suddenly i can start challenging this computer intensity number so this brings us finally to matrix

**31:04** · multiplication as i was saying this is the one algorithm which we really really care about but which actually can find this compute intensity you probably already know what multi-matrix multiplication is but i'm not going to show you what it is i'm going to show you what the machine thinks it is right in the simplest case i multiply every row of green by every column of blue and i get every dot of

**31:27** · white i'll show you how this works so first we extract the row and the column that we want we've loaded five green values and we've loaded five blue values then we multiply each element with its partner and we add the result together with its partners to get the final value so here's the point right remember how i was telling you about dax b how it's got this fused multiply add there's this fma

**31:51** · remember i said it's such an important function that most processors have their own instruction especially for it this is why it's really important it is a fundamental operation in so many mathematical mathematical algorithms so my matrix multiply is a big complex thing but it's built up of tons and tons and tons of these stack speeds

**32:11** · and this repeats over and over for each output value right notice how the green row isn't changing right there is an example of me reusing what i loaded many many times for this matrix 25 times for every green dot loaded i've just worked with this one row and i've done 25 calculations with it that is some serious compute intensity if my matrix were 10 by 10 i would be reusing this at the rate of 100 operations per load which is the compute intensity that i want remember so

**32:43** · my as my matrix grows i dramatically improve my ability to start getting or keeping my flops busy so matrix multiplication has an arithmetic intensity which increases as the cube of the matrix size that's that's the nature of the the matrix multiplication algorithm right at the same time my number of data loads goes up as the square as my matrix gets bigger and as n gets larger i have n squared things that i'm loading so my my arithmetic intensity scaling my algorithmic complexity is order n

### ARITHMETIC INTENSITY OF MATRIX MULTIPLICATION

### ALGORITHMIC EFFICIENCY OF MMA

**33:18** · so here is my plot of how the required compute intensity increases with matrix size right as my matrix goes from size 1 to size 64. it's a straight line because an order n scale means it increases monotonically as n increases so as i make my matrix bigger i need commensurately more more compute intensity to be able to be able to service that now i can plot the line that shows what the compute intensity is for a single precision floating point on the gpu

**33:45** · so then the jeep the ampere a100 gpu can do about 19 and a half teraflops of of gpu computing and this works out to an a compute intensity of 50.

**33:57** · right the crossing point tells us the control point has it tells us that once the matrix size reaches 50 we're fetching all the data that we need to keep the flop for compute flops busy is by affecting all that they can handle so this is the largest matrix i can do efficiently right above this size of matrix my memory is now idle more than the compute course right you want your machine ideally to be balanced you want to keep everything running at 100 that's really the point of the throughput machine so the sweet spot is the crossing point on that line

**34:29** · so if i plot double precision you can see here it's higher because um on the a100 we have double precision tensor chords which give you more flops for thread right tensor cores are i'll get into them in a moment so you can see that on this chart right i maxed out the single but i'm not maxed out on double right so we can zoom out a little bit on this map i put a green arrow down the bottom so you can see the n equals 64 span and

**34:52** · we're zooming right out so that that previous graph is just that lower left corner right there so larger matrices you can see the matrix intersects at around about 100 compute intensity so a 100 square matrix is going to be maxing out my double precision and of course as my matrix size gets bigger my memory gets in fact more and more idle because i'm spending more and more time computing instead so i really am fighting for this balance point here

**35:22** · so now we can bring in the tensor cores right the tensor cores are custom hardware units built into the sm functioning very much like an arithmetic unit like a multiplier an ad but they do an entire matrix operation a matrix multiply operation in one go that means they have a ton of flops packed into a single step right fma did

**35:43** · two it was a fuse multiply add it did two flops for every instruction these tensor cores do way more flops than that for every instruction and you can see this yellow line the compute intensity for the tensorflow 32 the 32-bit tensor core is right up there at 400 because i've just got that many flops so i'm going to need a ton of memory to fit this to service this and so my matrix size that i need to begin

**36:08** · saturating that is is 400 my matrix is much much much bigger and so this is this tension that i've got right i want more flops because i want to go faster but more flops require a bigger problem size otherwise my memory system is a bottleneck and bigger problem sizes aren't always possible so adding more flops on its own i just run out of room

**36:30** · i can't i think 400 square matrix is a very large matrix i really want my flops but i want them with smaller matrices right i want to have my cake and i want to eat it and this is where cash comes in okay so let's let's look at the bandwidth and the latencies again you saw this table before and now we can look at it for what the tensor core compute intensity is what is the compute intensity that's needed i drew that line at 400 in the previous slide for the tensor core that is what it needs to operate out of out of main memory hbm

**36:58** · memory if i'm operating out of l2 cache my compute intensity is only 156 and i'd always see the shared memory which is much smaller it's only 32 right so i clearly clearly need to be working with cash to get my my tensor cores efficient

**37:14** · at smaller matrix sizes in fact i can plot this and you can really start to see why data location matters right the smallest matrix i can efficiently do is 400 square when my data is in my main memory but it's only around 150 when it's in the l2 cache and my smallest matrix is 32 and it's living in shared memory right suddenly i can handle small matrices because i've taken care of where my data is

**37:42** · which was really the title i wanted for this talk so what have we seen today we've seen we've seen that flops don't matter but bandwidth does because of compute intensity and then we learn that bandwidth doesn't really matter as much as latency because latency is long and to fix latency i need a lot of threads and the gp architecture is built with

**38:04** · this lots of threads in mind and with oversubscription to hide the latency we learned that i have a measurable commute and we learned that the gpu is a throughput machine which needs over subscription instead of being a latency machine which has a fixed amount of work

**38:19** · in spite of all those threads sometimes they still need to work together right not everything is element-wise and so the gpu runs threads is a hierarchy right a big grid of work broken up into blocks which run in throughput mode and then threads in the block can work together and cooperate on some operation so with latency beaten we then turned and looked at how the compute intensity of heavy lifting algorithms like matrix multiplier finally begins to balance

**38:45** · compute against bandwidth and the way to get high efficiency on small compute intensive pieces of work is really to play the cash hierarchy game i can beat latency with threads and i can beat bandwidth with locality and then i can get all the flops even from the tensor cores

**39:04** · which brings me back to my original title right where's my data because my ability to max out the efficiency of all the components in my system my threads my memory my compute is contingent on where the data is to begin with right low compute intensity asks less of me because i can you i can get away with fewer threads to hide the latency and i have more bandwidth to feed the flops but everything really depends on data even my ability to use those flops depends on where my data is

**39:32** · and that's what i got for you thank you very much