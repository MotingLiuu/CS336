# Efficiency Analysis

## Cpu time consuming:



## TinyStories_valid.txt, multiprocess = 64, num_chunks = 256, vocab_size = 2000

python: 14%

native: 55%

system: 29%

![](1.png)



## TinyStories_valid.txt, multiprocess=16, num_chunks=16,vocab_size=2000

python: 23

native: 73

system: 2.9

![](2.png)



## TinyStories_valid.txt, multiprocess=16, num_chunks=256,vocab_size=2000

![](6.png)





## TinyStories_valid.txt, multiprocess=64, num_chunks=16,vocab_size=2000

python: 11

native: 48

system: 40

![](3.png)



## TinyStories_train.txt, multiprocess = 64, num_chunks = 64, vocab_size = 32000

python: 23%

native: 72%

system: 4.7%

![](4.png)



## TinyStories_train.txt, multiprocess = 64, num_chunks = 256, vocab_size = 32000

python: 23%

native: 72%

system: 4.7%

