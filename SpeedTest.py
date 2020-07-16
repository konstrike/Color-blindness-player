import numpy as np
import time

from algorithm import Algorithm

results=[]

alg = Algorithm()

rezolutii = [(320, 180, 3), (640,360,3),(720,480,3),(1280,720,3),(1920,1080,3),(3840,2160,3)]

# for j in range(6):
#     frame = np.ones(rezolutii[j], dtype='uint8')
#     reza = []
#     for i in range(100):
#         a = time.perf_counter()
#         alg.threadPro(frame, rezolutii[j][0], rezolutii[j][1], rezolutii[j][2],128)
#         b = time.perf_counter() - a
#         reza.append(b)
#     results.append(reza)
#
# print(min(results))
#
# for i in range(6):
#     print(f"{rezolutii[i][0]:4}x{rezolutii[i][1]:4}     {max(results[i]):.6f}    {min(results[i]):.6f}    {sum(results[i])/len(results[i]):.6f}    = .transpose(2, 0, 1).reshape(3,-1)      # ")


frame = np.ones(rezolutii[4], dtype='uint8')
reza = []
for i in range(100):
    a = time.perf_counter()
    alg.threadPro(frame, rezolutii[4][0], rezolutii[4][1], rezolutii[4][2],)
    b = time.perf_counter() - a
    reza.append(b)
results.append(reza)

print(min(results))

# for i in range(6):
print(f"{rezolutii[4][0]:4}x{rezolutii[4][1]:4}     {max(results[0]):.6f}    {min(results[0]):.6f}    {sum(results[0])/len(results[0]):.6f}    = .transpose(2, 0, 1).reshape(3,-1)      # ")
