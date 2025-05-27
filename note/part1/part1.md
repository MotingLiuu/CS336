# regex

**Zero-width match**

表示某个条件成立的那个位置，但是没有提取字符

`^`, `$`, `\b`, `(?=...)`, `(?!=...)`



**re.finditer()**会返回一个迭代器，每一个结果是一个`re.Match`对象

```py
import re

pattern = r'\d+'  # 匹配一个或多个数字
s = "abc123def456ghi789"

matches = re.finditer(pattern, s)
for match in matches:
    print(match)         # Match对象
    print(match.group()) # 匹配到的字符串
    print(match.start()) # 匹配开始位置
    print(match.end())   
```

```bash
<re.Match object; span=(3, 6), match='123'>
123
3
6
<re.Match object; span=(9, 12), match='456'>
456
9
12
<re.Match object; span=(15, 18), match='789'>
789
15
18
```

```py
import re
s = "hi! bye."
# 下面的正则在每个单词边界零宽匹配
matches = list(re.finditer(r'\b', s))
for m in matches:
    print(m.start(), m.group())
```

```bash
0 
2 
4 
7 
```

- **普通匹配**：`start()` 是匹配到的子串的第一个字符的下标。
- **零宽度匹配**：`start()` 返回的是“匹配发生的位置”，可以理解为“字符之间的间隔下标”，也就是“切片分隔点”。



**re.split()**

如果开头被匹配，则第一个`re.match`是`''`，末尾被匹配则最后一个`re.match`是`''`

零间隔返回的`re.match`对象的坐标是间隔的坐标。

**优先匹配能消耗掉字符的分隔符，对于不能消耗任何字符的地方，也会把这些位置当作分割点。**

![](1.png)

得到的结果

![](2.png)

第一个匹配到`...`，之后对`words...`进行匹配，匹配到`''`，之后对没有开头的`words...`匹配，匹配到`w` `o`之间的空隙... 结果为

```bash
['', '', 'w', 'o', 'r', 'd', 's', '', '']
```

```py
re.split(r'(\W*)', '...words...')
['', '...', '', '', 'w', '', 'o', '', 'r', '', 'd', '', 's', '...', '', '', '']
```



# multiprocess

Use `fork()` to create a subprocess.

```py
import os

print(f'Process {os.getpid()}')

pid = os.fork() # os.fork()会将当前进程复制一份，作为新的子进程。父进程和子进程都从fork()这一行继续执行。唯一不同的是父进程fork()返回子进程PID，而子进程返回0
if pid == 0:
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
else:
    print('I (%s) just created a child process (%s).' % (os.getpid(), pid))
```

Use `Process` of `multiprocessing` to create a subprocess

```py
from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',)) # target是子进程运行的函数，args是函数的参数
    print('Child process will start.')
    p.start() # 启动子进程
    p.join() # join() = 等到子进程结束 + 帮操作系统“收尸”（资源回收。join() 内部会调用底层操作系统的 wait() 系统调用，将子进程彻底清理、回收掉，
    print('Child process end.')
```

Use `pool` to create a batch of subprocess

```py
from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(1)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(16) # 创建了一个四个进程的进程池
    start = time.time()
    for i in range(16):
        p.apply_async(long_time_task, args=(i,)) # 进程池会自动管理所有进程的，启动，调度，复用，回收。只需要使用apply_async()提交任务。使用apply_async()提交任务之后，主进程还会继续。不会等待子进程结束。
    print('Waiting for all subprocesses done...')
    p.close() # 结束这个进程池，不再接受新的任务
    p.join() # 等待池中所有进程结束任务
    end = time.time()
    print(f'All subprocesses done. time:{end - start}')
```