from scierror import Measurement as M

weight1 = M(15, 0.1)
weight2 = M(20, 0.5)
weight3 = M(5, 0.5)
weight4 = M(0.5,0.1) # needed for inverse trig functions over -1, 1

print("+:", weight2 + weight1)
print("-:", weight2 - weight1)
print("*:", weight2 * weight1)
print("/:", weight2 / weight1)

print("sin:", M.sin(weight3))
print("cos:", M.cos(weight3))
print("tan:", M.tan(weight3))
print("pow:", M.pow(weight3, 4))
print("log:", M.log(weight3))
print("log2:", M.logbase(weight3,2))
print("arcsin:", M.arcsin(weight4))
print("arccos:", M.arccos(weight4))
print("arctan:", M.arctan(weight4))
print("exp:", M.exp(weight3))