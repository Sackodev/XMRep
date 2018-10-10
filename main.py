from xmread import XMReader

poop = XMReader('ezername.xm')
poop.readXM()
print(poop.patList[-1].ch[-1].notes[-1].type)
