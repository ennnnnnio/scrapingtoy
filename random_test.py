import random
# M = 16**4
# print("2001:cafe:" + ":".join(("%x" % random.randint(0, M) for i in range(6))) )


for x in range(1,100):
  ip = "192.168."
  ip += ".".join(map(str, (random.randint(0, 255)
                          for _ in range(2))))

  print(ip)
