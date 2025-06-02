import time


sta = time.time()
for i in range(100000000):
    pass
end = time.time()
    
print(f"Time cost: {end - sta}")