import os
import time
import random
import argparse
import sys
from multiprocessing import Pool, Process, Queue
import subprocess

# =======================
# 示例1：fork()
# =======================
def example_fork():
    print(f'Process {os.getpid()}')
    pid = os.fork()  # os.fork()会将当前进程复制一份，作为新的子进程。父进程和子进程都从fork()这一行继续执行。唯一不同的是父进程fork()返回子进程PID，而子进程返回0
    if pid == 0:
        print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
    else:
        print('I (%s) just created a child process (%s).' % (os.getpid(), pid))

# =======================
# 示例2：Pool进程池
# =======================
def example_pool():
    def long_time_task(name):
        print('Run task %s (%s)...' % (name, os.getpid()))
        start = time.time()
        time.sleep(1)
        end = time.time()
        print('Task %s runs %0.2f seconds.' % (name, (end - start)))

    print('Parent process %s.' % os.getpid())
    p = Pool(16) # 创建了一个16个进程的进程池
    start = time.time()
    for i in range(16):
        p.apply_async(long_time_task, args=(i,)) # 进程池会自动管理所有进程的，启动，调度，复用，回收。只需要使用apply_async()提交任务。使用apply_async()提交任务之后，主进程还会继续。不会等待子进程结束。
    print('Waiting for all subprocesses done...')
    p.close() # 结束这个进程池，不再接受新的任务
    p.join() # 等待池中所有进程结束任务
    end = time.time()
    print(f'All subprocesses done. time:{end - start}')

# =======================
# 示例3：Process
# =======================
def example_process():
    # 子进程要执行的代码
    def run_proc(name):
        print('Run child process %s (%s)...' % (name, os.getpid()))

    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',)) # target是子进程运行的函数，args是函数的参数
    print('Child process will start.')
    p.start() # 启动子进程
    p.join() # join() = 等到子进程结束 + 帮操作系统“收尸”（资源回收。join() 内部会调用底层操作系统的 wait() 系统调用，将子进程彻底清理、回收掉，
    print('Child process end.')

# =======================
# 示例4：subprocess调用外部命令
# =======================
def example_subprocess():
    result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
    print(result.stdout)  # 输出命令的结果
    
def example_comm():
    
    def write(q):
        print('Process to write: %s' % os.getpid())
        for value in ['A', 'B', 'C']:
            print('Put %s to queue...' % value)
            q.put(value)
            time.sleep(random.random())
    
    def read(q):
        print('Process to read: %s' % os.getpid())
        while True:
            value = q.get(True) # 数据只能被读取一次，当一个数据被get()后就从队列中消失
            print('Get %s from queue.' % value)
            
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入:
    pw.start()
    # 启动子进程pr，读取:
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run multiprocessing/subprocess examples')
    parser.add_argument(
        'example',
        choices=['fork', 'pool', 'process', 'subprocess', 'queue'],
        help='Which example to run'
    )
    args = parser.parse_args()

    if args.example == 'fork':
        if os.name == 'nt':
            print("os.fork() 只支持Unix/Linux，不支持Windows")
            sys.exit(1)
        example_fork()
    elif args.example == 'pool':
        example_pool()
    elif args.example == 'process':
        example_process()
    elif args.example == 'subprocess':
        example_subprocess()
    elif args.example == 'queue':
        example_comm()
