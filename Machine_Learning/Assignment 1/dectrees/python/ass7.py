import dtree
import monkdata
import random
import matplotlib.pyplot as plt

dataset = monkdata.monk3
testset = monkdata.monk3test
fractions = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
iterations = 1000

NormalTreeAcc = {}
PrunedTreeAcc = {}


def partition(data, fraction):
    ldata = list(data)
    random.shuffle(ldata)
    breakpoint = int(len(ldata) * fraction)
    return ldata[:breakpoint], ldata[breakpoint:]


for frac in fractions:
    TreeAcc = 0
    PTreeAcc = 0
    for i in range(iterations):
        train, val = partition(dataset, frac)

        tree = dtree.buildTree(train, monkdata.attributes)
        # TreeAcc[frac] = dtree.check(tree, val)
        tAcc = dtree.check(tree, testset)
        TreeAcc += tAcc

        ptree = dtree.allPruned(tree)

        topPt = None
        ptAcc = -1
        for pt in ptree:
            acc = dtree.check(pt, val)
            if acc > ptAcc:
                ptAcc = acc
                topPt = pt

        PTreeAcc += dtree.check(topPt, testset)
        # PTreeAcc += ptAcc

    # PrunedTreeAcc[frac] = dtree.check(TopPT, testset)/
    NormalTreeAcc[frac] = TreeAcc / float(iterations)
    PrunedTreeAcc[frac] = PTreeAcc / float(iterations)

print("Tree Acc: {}".format(NormalTreeAcc))
print("pTree Acc:{}".format(PrunedTreeAcc))

# plotting
x_axis = fractions
y_axis_t = []
y_axis_pt = []
for x in x_axis:
    y_axis_t.append(1.0 - NormalTreeAcc[x])
    y_axis_pt.append(1.0 - PrunedTreeAcc[x])
plt.plot(x_axis, y_axis_t, 'r', x_axis, y_axis_pt, 'g')

plt.show()