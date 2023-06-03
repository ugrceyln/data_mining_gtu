def read_file_and_get_transaction_dict(filename):

    with open(filename) as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    Transaction = []

    for i in range(0, len(content)):
        Transaction.append(content[i].split())

    return Transaction

def generate_initial_set(dataset):

    retDict = {}
    for trans in dataset:
        key = frozenset(trans)
        retDict.setdefault(key, 0)
        retDict[key] += 1

    return retDict

# class of FP TREE node
class TreeNode:
    def __init__(self, Node_name, counter, parentNode):
        self.name = Node_name
        self.count = counter
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def increment_counter(self, counter):
        self.count += counter

    def disp(self, ind=1):
        print('  ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)

# To update the link of node in FP Tree
def update_NodeLink(Test_Node, Target_Node):
    while (Test_Node.nodeLink != None):
        Test_Node = Test_Node.nodeLink

    Test_Node.nodeLink = Target_Node

# To create the FP Tree using ordered itemsets
def updateTree(itemset, FPTree, HeaderTable, count):

    if itemset[0] in FPTree.children:
        FPTree.children[itemset[0]].increment_counter(count)
    else:
        FPTree.children[itemset[0]] = TreeNode(itemset[0], count, FPTree)

        if HeaderTable[itemset[0]][1] == None:
            HeaderTable[itemset[0]][1] = FPTree.children[itemset[0]]
        else:
            update_NodeLink(HeaderTable[itemset[0]][1], FPTree.children[itemset[0]])

    if len(itemset) > 1:
        updateTree(itemset[1::], FPTree.children[itemset[0]], HeaderTable, count)

# To create Headertable and ordered itemsets for FP Tree
def create_FP_Tree(dataset, minSupport):

    HeaderTable = {}
    for transaction in dataset:
        for item in transaction:
            HeaderTable[item] = HeaderTable.get(item, 0) + dataset[transaction]
    for k in list(HeaderTable):
        if HeaderTable[k] < minSupport:
            del (HeaderTable[k])

    frequent_itemset = set(HeaderTable.keys())

    if len(frequent_itemset) == 0:
        return None, None

    for k in HeaderTable:
        HeaderTable[k] = [HeaderTable[k], None]

    retTree = TreeNode('Null Set', 1, None)
    for itemset, count in dataset.items():
        frequent_transaction = {}
        for item in itemset:
            if item in frequent_itemset:
                frequent_transaction[item] = HeaderTable[item][0]
        if len(frequent_transaction) > 0:
            # to get ordered itemsets form transactions
            ordered_itemset = [v[0] for v in sorted(frequent_transaction.items(), key=lambda p: p[1], reverse=True)]
            # to update the FPTree
            updateTree(ordered_itemset, retTree, HeaderTable, count)

    return retTree, HeaderTable

# To transverse FPTree in upward direction
def FPTree_uptransveral(leaf_Node, prefixPath):

    if leaf_Node.parent != None:
        prefixPath.append(leaf_Node.name)
        FPTree_uptransveral(leaf_Node.parent, prefixPath)

# To find conditional Pattern Bases
def find_prefix_path(basePat, TreeNode):
    Conditional_patterns_base = {}

    while TreeNode != None:
        prefixPath = []
        FPTree_uptransveral(TreeNode, prefixPath)
        if len(prefixPath) > 1:
            Conditional_patterns_base[frozenset(prefixPath[1:])] = TreeNode.count
        TreeNode = TreeNode.nodeLink

    return Conditional_patterns_base

# function to mine recursively conditional patterns base and conditional FP tree
def Mine_Tree(FPTree, HeaderTable, minSupport, prefix, frequent_itemset):
    bigL = [v[0] for v in sorted(HeaderTable.items(), key=lambda p: p[1][0])]
    for basePat in bigL:
        new_frequentset = prefix.copy()
        new_frequentset.add(basePat)
        # add frequent itemset to final list of frequent itemsets
        frequent_itemset.append(new_frequentset)
        # get all conditional pattern bases for item or itemsets
        Conditional_pattern_bases = find_prefix_path(basePat, HeaderTable[basePat][1])
        # call FP Tree construction to make conditional FP Tree
        Conditional_FPTree, Conditional_header = create_FP_Tree(Conditional_pattern_bases, minSupport)

        if Conditional_header != None:
            Mine_Tree(Conditional_FPTree, Conditional_header, minSupport, new_frequentset, frequent_itemset)

filename = "sample_data_book"       # input()
min_Support = 2                     # int(input())

transactions_dict = read_file_and_get_transaction_dict(filename)
initial_set = generate_initial_set(transactions_dict)

FPtree, HeaderTable = create_FP_Tree(initial_set, min_Support)

# FPtree.disp()

frequent_itemset = []
# call function to mine all ferquent itemsets
Mine_Tree(FPtree, HeaderTable, min_Support, set([]), frequent_itemset)

print("frequent itemsets:")
print(frequent_itemset)
