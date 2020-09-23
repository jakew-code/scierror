from scierror import Measurement as M

weight1 = M(15, 0.1)
weight2 = M(20, 0.5)
weight3 = M(5, 0.5)

print("+:", weight2 + weight1)
print("-:", weight2 - weight1)
print("*:", weight2 * weight1)
print("/:", weight2 / weight1)

print("sin:", M.sin(weight3))
print("cos:", M.cos(weight3))
print("tan:", M.tan(weight3))
print("pow:", M.pow(weight3, 4))
print("log:", M.log(weight3))
print("exp:", M.exp(weight3))