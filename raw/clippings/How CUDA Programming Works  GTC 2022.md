---
title: "How CUDA Programming Works | GTC 2022"
source: "https://www.youtube.com/watch?v=n6M8R8-PlnE"
author:
  - "[[Dan the Man]]"
published: 2022-07-05
created: 2026-07-06
description: "www.nvidia.com/en-us/on-demand/session/gtcspring22-s41487/"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=n6M8R8-PlnE)

www.nvidia.com/en-us/on-demand/session/gtcspring22-s41487/

## Transcript

### Intro

**0:01** · hi i'm stephen jones and i'm one of the architects of cuda i've been working on the kuda programming model and gpu computing since scotch 2008 and one of the best things about this job is that code is really a co-design between hardware and software right since cuda is the way you program the gpu directly it's vital that we give access to every

**0:22** · last bit of performance that's available but at the same time we're incredibly aware that programming a massively parallel machine is complex so the single most important priority for me is always programmability there's an interesting tension there and one of the ways that that comes out is that there are key performance elements which you need to take into account even while the bulk of your program can be pretty naive c plus plus um i'm not going to teach you cuda today there's not enough time for that but i'll teach you a few things that i

**0:50** · think are vital to think about when you're programming the gpu i think the the most important thing when doing any engineering is to have an accurate mental model of the system that you're using and for a clear mental model i really think the best way to understand the how of something is to know why it's that way so this this talk is really about why kuder is the way that it is not just how so that's a good question why is kuda the way it is

### SO WHY IS CUDA THE WAY IT IS?

**1:21** · physics right it's the way it is because of the laws of physics quite literally so what do i mean by that well if you're using a gpu because you want performance of some kind cuda is designed in part to allow you to get maximum performance on the gpu right it's obviously as i said also designed to make it programmable um performance is limited by the laws of

**1:43** · physics and i'll get to that in a moment and so cuda is designed to do its best to help you work with the hardware within the laws of physics to get good performance so this is actually really interesting point to make you see what's special about cuda is that we make both the programming language for the hardware and the hardware that runs the programming language this means not only do we get to adjust

**2:07** · the programming language to match what the hardware can do but we also get to adjust the hardware so that it's more programmable the hardware designers come up with really clever stuff to overcome limitations like speed of electricity and silicon and and could revolve to allow this clever stuff to be programmable literally speaking cuda is shaped by the laws of physics

**2:29** · so i made another possibly contentious statement that i want to look at more closely for a moment i gave a whole talk basically about this at gtc last year and i put the link below as a shameless plug for my talk but also because if you're interested it gives you a lot more detail than i'm going to get into right here about about hardware and overcoming physical constraints anyway i won't repeat the whole thing but i will bring up the main points let's start with this statement though because presumably you paid money and

**2:59** · are investing time in gpu computing because you want performance from it so let's look at what that means i'll make up what i hope is an uncontroversial statement that getting the best performance is about using all the gpu resources that you can in other words the more threads i'm running and the more memory i'm moving the more calculations i'm making the better i'm probably doing

### THE NVIDIA AMPERE GPU ARCHITECTURE

**3:25** · so these are the feeds and speeds of the amped gpu and the obvious performance metric to look at is flops it has a ridiculously large number of flops right that's almost 10 teraflops of double precision performance almost 20 of single precision and that's not counting the tensor cores which are way too complex to get into here and normal flops will work fine for this discussion it's easy to say the more of those flops your application is getting the better you're doing

**3:51** · and there's no question about it but very often it's not actually the fact that it is limiting the performance that your application is able to get there's usually more flops than you need i mean 10 teraflops is a lot for reference this single chip is more powerful than the biggest supercomputer in the world from 21 years ago right the ascii white super computer was 200 cabinets it weighed over 100 tons

**4:17** · and it was about three quarters as powerful as this tiny little piece of silicon it's if nothing else this is a testament to moore's law it's truly amazing but it means that this thing that you have here has all of the capability all of the power of of that giant machine and you've got it all at your fingertips in one thing and you know i hope we've evolved much more now to get to a point where it's easy to program easier to access that kind of performance but but that 20 years ago this scale was an entire room right

### BUT FLOPS AREN'T THE ISSUE - BANDWIDTH IS

**4:51** · but i'd like to argue that flops doesn't matter memory bandwidth is what matters i mean yeah you want the compute performance but that's not what limits you and that's almost never what ends up defining how your cuda program works

**5:07** · let's look at a schematic of the a100 gpu uh here on the right it has 108 sms um connected to the memory system and each sm which is sort of the core one of the cores of the machine each sm can request 64 bytes of memory per clock and a clock speed of 14 10 megahertz

**5:27** · that's almost 10 terabytes of memory requested per second by contrast the incredibly fast hbm2 memory system can provide over one and a half terabytes of memory per second that's an enormous amount of memory bandwidth but it's still over six times less data than the sm itself once all the sms together want to pull in so there's just no way to feed data into the gpu at the rate that it can request it and even the rate it can request it

**5:54** · is not enough to saturate all of the flops that it has available but that's another story right it means we're almost always limited by memory performance and not by the threads being unable to keep up with the data if you're not keeping your threads busy you're not getting the most done that you can

**6:14** · so if i'm looking at the rate i can feed data into my system purely from a memory standpoint right which is not completely representative because obviously i have data reuse and and there's other factors which go into flops but if i just look at um what a program that needs to suck in data and process that data as fast as it can the the limit is going to be this one and a

**6:37** · half terabytes per second of data right and if i do the division that's 194 billion double precision values per second giving me a peak performance based on memory of just 194 gigaflops right now i'm only beating the 1996 biggest computer in the world

### A CLOSER LOOK AT RANDOM ACCESS MEMORY

**6:55** · so let's have a look at this this memory thing let's have a closer look at how it works because it's so important in the performance of the machine a single bit of memory is a capacitor and either holds it or one bit on the left or it's empty for reserve it right the memory is red by switching on the transistor which connects it to a wire the bit line and the y then carries a voltage based on the charge in that capacitor so the wire records either an on or an r for one or a zero

**7:27** · the dram chip consists of millions of these cells all connected together in a big 2d matrix right this matrix layout lets me access any row any column and this is why it's called random access memory right that's the random access path as again say a magnetic tape which has a linear axis data is addressed via a row and a column index which are taken from the request address

**7:52** · first the row is accessed all the cells in the row are activated and their state is copied up to these things called the sense amplifiers now the sense amplifiers read the tiny charges on each of the capacitors in the cells and turn them into well-defined voltages that can much more easily be read in the next set right the problem is that the charge in the capacitor is drained as this happens right i'm connecting a wire to the capacitor it's draining all the electrons out and so the data in the row is destroyed i'll come to that in a moment

**8:23** · next the column access takes place instead of reading from memory cells that row is already in the amplifier so it reads the data held in the amplifier this is much quicker much easier to read than a row because the amplifiers are producing a strong clear signal and so i can read much more quickly you can read repeatedly from the amplifiers because they hold their voltage right you can read as many times as you like from the fetch row so if you can open a row and use it repeatedly

**8:48** · then you're you're not having to deal with the capacitance at all because it's so common in fact to read adjacent memory locations in a row there's this thing called a burst mode where a single request returns multiple words of data right this is a huge deal because it means i don't have to pay for the individual requests over and over again and pretty much every processor in the world uses this because the cache system of the processor is always going to go and read multiple bytes at a time and then gpu the cast system is 128 bytes at a time i'll talk about the cache in a bit

**9:18** · the problem is that when i need to read another row i first have to write back the data which was held in the amplifiers if you remember the row was drained when it was copied into the amplifiers because the capacitor is discharged so we now have to rewrite it to avoid memory corruption right so this makes a page switch expensive because it involves both the right back and then a new lower new row load

**9:41** · into the amplifiers right and hardware calls things rows or pages pretty much interchangeably so if you hear the term page then this is what they mean they mean a row of your memory switching page is about three times as expensive as switching column within a page because of this load and store operation or sorry store and load operation so putting a couple of numbers to this and and these are just some hbm numbers i found online but they represent the kind of scale we're talking about the rate at which you can load up and read a value from your dram depends on the physical time it takes

**10:14** · to charge and discharge capacitors right i've got to open a row which involves discharging capacitors i then read a column and then when i switch row i've got to recharge them all right row read takes three times as long because i just have to do the rewrite before i load the new page into my and into the amplifiers which means i all go way faster when i read adjacent data values one column than when i read strided data values long rows my data read pattern matters

**10:44** · because of the physics of the random access memory capacitance with this in mind we ran an experiment to look at what this physics was doing and in this experiment we read eight byte values each with an increasing stride right so a stride of eight is on the x-axis is is

### SO WHAT DOES THIS ALL MEAN?

**11:02** · an eight by value right next to each other sixteen is every other value and so on out to striding by skipping a thousand values which is which is an eight eight one nine two eight kilobyte stride right um i've left the x-axis in bytes because it relates better to what i was just showing you a moment ago and there's a lot of really interesting stuff in this chart for example you can tell the page size is one kilobyte because when the stride goes from 510 to 2512 to 1024 bytes i'm now only getting

**11:28** · one value per page and you can see you can see the bandwidth drop there it literally halves right because i was reading two things from each row access now i'm getting one thing from each row axis likewise at the top left-hand corner of the graph just by reading every other value going from a straight of 8 to 16 i'm dropping by by half and that's because every time i open a row i'm only reading every other value and so if half of my row is now is now wasted but i can't open less than a row

**11:57** · but i'm most interested in how low things go on the right hand side of the graph because this tells me how much impact i can see from not being careful about my memory accesses or from just being forced to have bad memory accesses in effect when my stride gets long

**12:15** · it's like i'm reading random locations right i'm constantly opening and closing pages and issuing individual read commands for single values right the result is that my effective bandwidth drops by 92 percent that is enormous that is a factor 13 loss of bandwidth so if my achieved performance mainly depends on my memory performance as i was arguing earlier your memory access pattern can cost you literally almost everything in this case our 10 teraflop a100

**12:47** · is being fed data at about 14 gigaflop that's a factor 1 thousand off this is a really important result because it affects everything about the way i program cuda i care more about memory layout than anything else because no other optimization i do can come close to speeding me up by a factor of 10 all because of the laws of physics and the capacitance in my memory cells

**13:12** · and just in case some of you were noting that the quoted memory bandwidth which i've been using for a 100 is 1555 gigabytes per second but we only measured 14 18. that's actually because we're reading eight byte values here um if we read 16 byte values that would be just a larger chunk it's a little bit more efficient because you're fetching larger chunks of data it doesn't affect the low end of the performance because there everything is dominated by the memory access time and the road time so the the the difference is just on the high end

### DATA ACCESS PATTERNS REALLY MATTER

**13:42** · so this really leads me into my point here data access patterns really matter most programmers know this um but it's particularly severe on the gpu because memory latency is longer you've uh you've got more threads so you can have more requests uh hbm is a bit finicky those types of things but so you know let's take a a really common data structure a 2d array this could be an image or a matrix either way you typically lay it out in row major format which means adjacent memory locations are incrementing in the x direction like i've drawn down below

**14:15** · i really want to be writing my array traversal like this on the left in a row major way so i'm reading for each column sorry for each row do each column for y do x right this reads adjacent values in one after the other as most programmers know if i instead

**14:37** · access down a column of the code on the right instead of a long row my performance suddenly drops enormously right as we measured on the previous slide it drops by an order of magnitude for all the reasons we talked about so why why were we talking about this well it's because what drives performance is efficient use of resources

**15:02** · and and how does this all tie into cuda well obviously you can't always arrange for a perfect data layout but a factor of 13 difference in performance makes it really worth rewriting everything right you would write you'd write anything for a 10x speeder right it's also very much what leads to cuda's programming model being the way that it is so so let's look for a moment at how the cuda programming model runs work to see how this ties together

**15:30** · let's start with a quick primer on on how cuda breaks work down into pieces right this is this is the core of of kudos programming model and it's probably the most important thing about cuda but once you get the hang of it it's actually something you don't really think about too much we've got this hierarchy of grids blocks and threads and it's a way of subdividing the work into these manageable chunks that can run on there on the sm the fundamental unit of execution in cuda is the thread walk

### THE CUDA THREAD BLOCK

**15:56** · right not the thread not the warp which i haven't mentioned yet but i'll get to it um the block is really the quantum unit of parallelism on the machine right that's because this is the degree of parallelism you're guaranteed you know for sure that all threads in a block are alive so once they so they can work together and exchange data because they're all alive at the same time

### EVERY THREAD RUNS EXACTLY THE SAME PROGRAM

**16:18** · kudo really presents these threads as independent right kind of like p threads if you use them actually you're the code that you write for cuda thread is just like it's running on its own right so in a credit program it looks like a single-threaded program each thread has its own copy of the variables in its own program counter where it is in the code you don't have markup or pragmas or vector instructions or any of those types of things the whole secret lies in two variables thread idx and

**16:45** · block idx which automatically populated by the hardware when the block is launched to give each thread its index into the into the big grid of threads that were launched so don't worry what the program does i'm not trying to teach you how to code the only line that's important is this first line where each thread uses

**17:05** · its thread index and block index to calculate which bit of the data is working on after that everything in the program is the same and this is really the core picture of how a cuda program tends to work as you everybody does the same work on slightly different data addressed by a specific index

**17:26** · people often ask me actually what the difference is between sim d and sim t right because um cuda says it's got a sim t programming right and this line is really the fundamental difference right sim d single instruction multiple data is running a single thread with a vector unit attached the main thread controls everything it controls which lanes of the unit are active or inactive it's it's all very explicit you set a lane mask based on the if condition with sim t single instruction multiple thread thread control is implicit

**17:58** · each thread has its own state right all threads are independent even if they're part of a vector unit which we'll get to in a moment they still each maintain their own state including the index right so they can loop they can branch they can do conditional things they don't all have to be running together it's just more efficient when they are running together i'm going to talk about that right now

**18:20** · because the gpu does run threads together in groups right it runs them in a group of 32 which we call a warp and it does that because it's efficient for many reasons um to run things as a gang but this this is where it ties back into the memory story that i was telling you a moment ago in my little example program um and i wouldn't expect you to have noticed but a core piece of the program is that it's actually loading two points of data to figure out the distance between them right uh point p1 and point

**18:52** · p2 right it's indexed by that really important thread id block id line uh just above but effectively every thread is loading two values to go and calculate something about them what this effectively means is that i'm loading data from 32 different threads at once all at an offset indicated by some permutation function of the thread id in fact adjacency now float 2 is just a structure of two floats a size of 8 bytes

**19:24** · this means each warp is loading 256 consecutive bytes of data because each of its 32 threads fetches one of the values as indexed by its thread id thread ids are guaranteed consecutive which means the data access pattern is guaranteed consecutive i get 20 256 consecutive bytes of data

### WARP EXECUTION ON THE GPU

**19:44** · the streaming multiprocessor the sm on the gpu can manage 64 warps of threads at the same time which is 2048 throughout the per sm but as you can see from this block diagram it really has four separate segments right so at any given time it's really running four of those 64 warps the others are kept in the queue with fast switching but that's a different discussion

**20:06** · so i have four of my warps each with 32 threads each loading my data so each loading 256 bytes at the same time that's four times 256 bytes which is 1024 bytes of fully coalesced adjacent data addresses being loaded from the memory system at the same time

**20:26** · which if you remember is exactly the perfect size to make maximally efficient use of my memory system means that that load will use 100 of all the data that was fetched in the page which puts me right at that top left-hand corner of my graph again

**20:43** · and this is really important because programs read data all over the place right even my simple example does reads from two different point arrays p1 and p2 it's it's reading point one point two takes the ten finds the distance between them it looks like my program at least it looks to the system like my program is just doing random memory reads those arrays aren't adjacent to each other which you know as you saw it costs 90 of my memory performance it is the single most important thing i care about

**21:12** · but in reality because of this warp execution model and because we're running four of them at the same time it works out on my massively parallel gpu to be exactly the right amount of data it's exactly the right amount of data to hit the peak bandwidth of my memory system even if my program reads data from all over the place each read is exactly one page of my my memory and

**21:39** · lets me hit in the top left hand corner of this graph right so if you recruit a programmer and you've wondered why the warp is 32 threads this is one of the reasons it's not an accident right the hardware designers carefully balance the gpu to do exactly this and so whenever someone asks me how big their threadblock should be the answer is always never less than 128 threads

**22:02** · because you always want four warps working together to make it really easy to hit peak memory performance one warp is great so work hard in your program to have all threads in that warp reading from adjacent addresses but you need more than one warp in your block to get all this to work perfectly

### USING ALL THE GPU RESOURCES YOU CAN GET

**22:21** · so that's a lot about memory and data but there's more to why cuda is the way it is than just memory bandwidth in particular there's a finite number of sms which are you know the sms are the individual calls of the gpu and inside

**22:37** · the sm we have a fixed number of threads and other resources to play with and so it's not just getting the memory it's using that data efficiently as well using all the resources you can get i kind of see the gpu like an embedded system where you need to be aware of what resources we're using and you want to pack everything together as efficiently as possible

**22:57** · we're going to talk about something called occupancy if memory patterns are the most important thing you can think about because they make a factor of 10 difference in performance occupancy is the next biggest because that makes an additional factor of two or it can i'll show you in a moment so back to cuda's execution model i've got a grid of work divided into blocks and each block runs many threads okay so far so good let's start with some work to do maybe i'm going to do some some image processing on this picture of a flower

### CUDA'S GPU EXECUTION HIERARCHY

### START WITH SOME WORK TO PROCESS

### DIVIDE INTO A SET OF EQUAL-SIZED BLOCKS: THIS IS THE GRID OF WORK

**23:28** · i break the data up into equal size pieces right this is so i can run each of the pieces independently in parallel because the pieces are independent they can be scheduled in any order at any time right this gives the hardware as much freedom as possible to run things efficiently the one thing that is guaranteed as we talked about before is that the block will have a fixed number of threads and they're guaranteed to be running at the same time on the same sm and i'll i'll use this property in just

**23:59** · a moment so now i can start running my work on my gpu or if the hardware can right once i launch my grid to the gpu the hardware will start placing blocks onto available sms right so that at the moment on the right hand side i've got empty sms and a whole grid of work to be processed

**24:20** · the hardware intentionally spreads them out as widely as possible i'll get back in a minute why they does this but this spreading out of blocks is why they have to be completely independent right there's no guarantee of what block will land where you can't guarantee that block one and block two land on the same ascent in fact they almost certainly will not so each block is this this is the core of the credit program each block is its own standalone piece of work able to to do all the processing it needs with just the threads that it has

**24:45** · the hardware keeps on placing blocks onto an sm until the sm is full i'll talk about what full means in a moment too so here i'm showing that in this case two of the blocks fit onto each sm but in reality it depends on the block size right it could be anything up to 32 that's the limit at some point all the sms are going to be full all running work in whatever blocks they have on them or running it concurrently their threads are going to be used up or whatever as the block completes its work it will exit and the gpu hardware will place

**25:15** · another block in the gap like this this goes on until all my blocks have been processed and that's how we run a grid all this is cuda 101 right but i'm going to this much detail because what i really want to talk about is how work is placed onto an sm this is where we get back to our discussion about efficient use of resources

### WHAT DOES IT MEAN FOR AN SM TO BE "FULL"? ?

### LOOKING INSIDE A STREAMING MULTIPROCESSOR

**25:41** · if we look inside an sm there are a bunch of resources which it uses or which are available for running all the threads that it can right it's a fairly big list it covers a lot of different things which at least also some extent influence how much work the sm can run but by far the most important are these four at the top

**26:01** · oh by the way remember i said how hardware will intentionally spread blocks out across the all the sms as widely as possible it's because of this resource limitation down here right each sm only has a certain number of physical wires into the memory system right because obviously the memory system has to support 108 sm it's all working at once that means any one sm

**26:21** · doesn't have enough on its own to maximize that one and a half terabytes per second of memory bandwidth that i have so by spreading the blocks out across all the sms as widely as possible we maximize the amount of bandwidth that grid can use or if you feel like we reduce the chance of blocks contending for the bandwidth with other sms while while some scenes remain idle right and so as i just spent the last 20 minutes telling you memory bandwidth is the most precious resource of all and so the hardware automatically spreads these things out as widely as it can do

**26:53** · anyway uh back to the key sm resources so i'm actually going to ignore blocks per sem here because it's rare that you run into that problem although by all means ask me in the chat about when you might want to take advantage of such a large number but but we'll pay attention to these three right here

### ANATOMY OF A THREAD BLOCK

**27:09** · so we looked at the block running threads in the context of the memory system now let's look at it in terms of the other resources which used by the threads this is a slightly tweaked version of the code we're looking at earlier because i want to highlight resource use and not memory efficiency but it's largely doing the same thing breaking down the resources um to begin with the block has a known fixed size right you launch your grid telling cuda how many threads are in every block and every single block in the grid has that same size right so block size is one of the resources

**27:38** · i'm also using shared memory in this kind of fair memory is a pool of high speed memory that all the threads in the block can use to communicate with one another that another limited resource and each block in this case is going to have to have some of it finally there are registers this is the working space of the thread registers on gpu are kind of different to how they work on a cpu it's determined by the compiler depending on program structure

**28:02** · and on the complexity of operations so for example a floating point square root or division are complex arithmetic operations they require a lot of live variables because memory performance is so important on the gpu we don't rely on cache in the same way the cpu does instead we have a very large register file of immediately accessible data to use as a working space right so these these more complex math functions are going to start using registers as their

**28:26** · working space right it's quite common for a recruiter program to use 100 registers in every thread right remember that all threads are running the exact same program so they all need the exact same number of registers so my my total budget is the number of threads in my block multiplied by the number of edges per thread so these are the three really key things that i highlighted at the top of that on top of that sm resource table

### HOW THE GPU PLACES BLOCKS ON AN SM

**28:50** · we've talked about how a grid is scheduled on to all the sms right that breaks up the blocks and spreads them around now let's talk about how individual blocks are placed onto a single sm first and most importantly a block never spans two assemblies it's

**29:05** · always entirely resident on the single sm if there's not enough threads left the block can't run that right this allows threads in the block to communicate with each other via shared memory which is one of the resources and to synchronize with each other a block is a cooperative array of threads and it's the largest element with guaranteed parallelism right it's my quantum of parallelism the hardware might run lots of blocks in parallel it might run them one at a time it really depends on what else is running on the gpu but you know for certain that all threads in the block are at least alive simultaneously so on the

**29:36** · right hand side here i've put in some make-believe but typical numbers that you might see for a couple right two to six threads sixty-four registers per thread and and forty-eight k shared memory that many many programs have this this kind of footprint right and i'm gonna walk you through how this affects performance and execution

**29:56** · so let's start by placing blocks onto this sm if you remember we want to pack as many blocks as possible to maximize the number of threads that are running because ultimately my threads are doing the work right so the more threads i have the more efficient i'm being even if memory access is really important the more threads i have the more memory i can read right so what i've done here in this picture is i've sized the blocks in my diagram of the sm according to the fraction of resources taken up right so the register's taking about a quarter per block and the threads are taking less right so here's the first

**30:27** · block there's plenty of space on the sm still so another block will get placed on the sm as well both of these are running at the same time because the sm has enough resources to run them i'm not using all the 2048 threads of all 160k said memory um for this example i've kept the block numbering sequential though as we saw earlier it'll actually spread them out across sms um but it's easy to just look at this in one single picture so the third block will fit just fine as well but now i shared memory down the bottom there it's looking pretty full

**30:59** · you can see i have room for more blogs based on the number of threads i could fit more um and i have room for another block in the register space that's left over but but there's no way to place a fourth block because of shared memory my block needs all three of these right four times 48k of memory would be 192k which is more than the 160 that sm has this this program is what we call shared memory occupancy limited the first thing that i max out is shared memory

**31:27** · so what if i could rearrange my program in some way to use less shared memories let's say 32 down from 48.

**31:34** · if it was 32 4 times 32 is 128.

**31:38** · suddenly i could fit another block in so by dropping my shared memory things start looking better although clearly i'm now running out of registers but i've managed to fit an extra block on the machine so i'm not using all the shared memory anymore i'm certainly not close to using all the threads i've gone from being shared memory limited to register limited i tweet one variable and another one pops up

**32:03** · it's like some crazy four-dimensional tetris game you're never going to get it perfectly packed but you just kind of do the best you can you tweak things and try and pack that extra block so why do i care so much about this it's because we're playing with this thing called occupancy right which is a measure of how much stuff i can pack onto an sm remember what we're trying to do here is maximize use of gpu

**32:26** · resources each block does a certain amount of work i'm usually determined by its number of threads so the more threads i can run on an sm the more stuff i'm usually getting done in this case on the left i could fit three and by adjusting my shared memory i could fit four if i could adjust my registers maybe i'd fit five but this is the tetris that we play in this case the right hand side has 33 percent more threads active than the left right which means the gpu is cranking through my data 33 faster now

### OCCUPANCY IS THE MOST POWERFUL TOOL FOR TUNING A PROGRAM

**32:55** · obviously that's an ideal number right if you remember we compromised on the shared memory uh in order to fit the extra block in so probably that cost me something but you get the idea i hope in general occupancy is the most powerful tool you have for tuning a program once you're doing your best for memory access patterns there's pretty much no algorithm but no algorithmic optimization you can do that will speed your program up by as much as 33 that's huge and people work for a year to get five percent on the weltean code for the case where i've gone from an occupancy of one to two that would

**33:26** · actually double my performance right so so likewise getting it wrong can easily cost you 50 if you if you add a bit of extra shared memory and then boom you suddenly drop a block and you instead of gaining 33 you've lost 33 right that's that's easily done too so a key part when you're looking at how your program works is to always check your occupancy obviously it's not always possible to reduce the use of the key resource just

**33:50** · like it's it's not always possible to change my memory layout but but just like memory layout i actually think about this right at the start when i'm planning my algorithm and designing my program right i intentionally design with occupancy in mind because this is the second biggest lever that i have to pull

### FILLING IN THE GAPS

**34:10** · so this is my sm completely filled right with the grid that we're looking at at least and and with that particular pattern of resources but i'm still not using half my threads and and i've still got a quarter of my registers free i i we're going to try and fill in the gaps as that happens the gpu can run many things at once right it can actually run up to 128 different programs at once so

**34:31** · if we're not completely filling up the gpu with one thing we can try and tetris in another right next to it all right let's think about another grid this time it has a very large number of threads and a very small number of registers per thread and no shared memory obviously it's a little contrived but but actually this would be typical of a data movement kind of right something which is maybe doing a sort or just simply copying data from one place to another so this would be a mem copy kernel

**34:55** · the gpu is smart enough to say well i can't fit any more of the blue grid in let's try the green grid right and it'll pack a block of that green grid into the gap you can't pack two because i've run out of registers but i'm i'm running 66 more threads than i was before that's basically free performance right our tetris problem just gained yet another dimension but the hardware does all this for us so as long as you have multiple grids available to run the hardware will try and drop them in

### CONCURRENCY: DOING MULTIPLE THINGS AT ONCE

**35:23** · so this brings me to the next really important thing about cuda which is concurrency gpu is massively parallel on all sorts of different levels and to make the most of it you need to throw as many things at it as you can right in the previous example i was packing both my image processing kernel and a bonus copy kernel onto the gpu and to do this obviously i'd have to be copying different data from what i'm actually processing the key thing here though is we need to tell the gpu that these things are independent i'll show you what i mean

### CONCURRENCY: DEPENDENCIES

**35:54** · the key topic is dependencies or more importantly avoiding them where possible usually it's pretty obvious so for example i'm copying this flower up to the gpu then i'm processing it then i'm copying it back and those operations have to be done one after another there's no point copying the result before it's processed right

**36:13** · now let's say i want to do another flower the simple thing to do is just to string the sequence of operations together but obviously the second flower is not really dependent on the first flower i could do them both at the same time if there's space on the gpu to do it so in cuda we tell the gpu about this independence between the works using this concept of streams of work each stream is an independent work queue and by submitting work to different streams you tell cuda and hence the hardware what can be overlapped on the gpu at the same time

### CONCURRENCY: IT'S REALLY ALL ABOUT OVERSUBSCRIPTION

**36:43** · as we saw with the occupancy discussion what will actually happen is the gpu will pack the pieces of work which fit together right it'll tetris them it can't fit blocks of flower processing from both the blue and the green stream at the same time because if you remember the sm is shared memory limited but it can fit the green copy alongside the blue flower as as we saw earlier

**37:05** · what will naturally happen then is the two streams will shift in time as the gpu finds ways to play tetris with the independent work and pack things together as tightly as possible right this is a thing called over subscription where there's so much work available

**37:20** · that the gpu can spend all of its effort packing things into little corners and getting end-to-end throughput to be as high as possible right the more you can oversubscribe the gpu the better job it'll do at getting through all the work there's a ton of hardware specialized at playing four-dimensional tetris with dozens of different pieces of work so by simply thinking about what pieces of your workflow are independent from each other you turn on all that hardware and let it figure out the best schedule

**37:51** · so i'm going to have to wrap it up here i had actually had something like 130 slides of material but i obviously can't fit them all in the time available so i just have to give another talk next year anyway let's recap what we've seen today to try to frame the answer to our original question you know why is cuda the way that it is

**38:09** · we started out with the problem that the memory system can only feed about one-sixth of what the execution resources can request so our primary limiting factor is memory but we saw that memory system itself depends on good access patterns and the laws of physics regarding capacitance dictate that randomly reading memory is much more expensive than reading it linearly and we learned that if we get it wrong we slow everything down by 92 percent that's on top of already being limited by the performance of the memory system compared with what the sms won

**38:40** · so the story got a bit bad but we learned that warp execution system the gpu can save us by reading from lots of threads at once but that that we need all the threads in the warp to be working on adjacent data and that all the thread blocks better have a minimum of 128 threads so that i can issue these these maximum performance requests to my memory system

**39:02** · we learned that the hardware spreads blocks out as widely as possible across csm's to maximize the memory bandwidth that they can request and we learned that resource packing limitations have the second biggest impact on performance as much as a factor of two and that a small change in a resource like shared memory going from 48k to 32k can make a big difference in

**39:21** · program performance we learned that the hardware can play a pretty good game of four dimensional tetris but that we need to feed it a lot of concurrent work through over-subscription so that it can pack things efficiently and so in all these ways cuda's programming model represents the properties of the hardware it runs on

**39:42** · and that hardware has these properties because it's in a constant battle for efficiency against the laws of physics which means fundamentally like i said at the beginning cuda works the way it does because of physics

**39:57** · you know my aim when i'm talking about how could in the gpu works is not to tell people how to write cuda that's both more than an hour and also the answer is simply c plus for the most part i i really want to give you a feel for how a program runs on the gpu right for what you need to pay attention to because you want to make the most out of it and because there are weird pitfalls you might not expect right mostly mostly i just want to help you build a mental model of how things work by explaining why things work the way they do cuda programming works through thinking

**40:27** · carefully about your memory layout and about how to fit as much stuff as possible on the machine and maybe just a teeny tiny bit about optimizing your code right but to be honest if you get memory and occupancy and concurrency right there's not much left to optimize right if remember if you end up getting 50 of the peak performance of the gpu that's still 10 teraflops of floating point compute which is huge

**40:50** · and and getting the remaining 50 it's gonna be so much work so if you're going to do just three things look at your memory layout look at how well your things are packing on your sms how well the tetris is doing and make sure that you've told the gpu all the different pieces that are independent and honestly you don't have to do much more than that anyway i hope it's been fun for you thank you all so much for listening to me going about cuda until next time