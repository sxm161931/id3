from __future__ import division
import sys
from math import log10

import pandas as pd
from Node import Node


def main(args):
    for arg in args[1:]:
        print arg

    if(len(sys.argv) == 1):
        # print("Please enter training data file location")
        # loc = raw_input("Please enter training data file location")
        loc = "training_set.csv"
        df_training = pd.read_csv(loc)
    else:
        df_training = pd.read_csv(sys.argv[1])
    # print(df_training)
    # print(len(df_training))
    # print(len(df_training[(df_training['Class']==0)]))
    target_attr = list(df_training)

    target_attr.remove('Class')
    print(len(target_attr))

    #test_node = Node(None,None,0,150,150,target_attr,'','','',df_training)

    global root_node

    root_node = Node(None, None, 0, 0, 0, target_attr,
                     '', '', '', df_training, True)
    root_node = root_def(df_training, target_attr)

    if((root_node.left is not None) and len(root_node.left.target_attr) != 0):
        #root_def(root_node.left.df , root_node.target_attr)
        root_node.leaf_flag = False
        root_node.left.entropy, root_node.left.attr, root_node.left.leftcount, root_node.left.rightcount = best_attr(
            root_node.left.target_attr, root_node.left.df)

    if((root_node.right is not None) and len(root_node.right.target_attr) != 0):
        #root_def(root_node.left.df , root_node.target_attr)
        root_node.leaf_flag = False
        root_node.right.entropy, root_node.right.attr, root_node.right.leftcount, root_node.right.rightcount = best_attr(
            root_node.right.target_attr, root_node.right.df)

    print_tree(root_node)
    '''
    attrs = vars(test_node)
    print ', '.join("%s: %s" % item for item in attrs.items())
    '''
    # calculation for left i.e 0 (-), right i.e 1(+)


def print_tree(root):
    if root is None:
        return
    else:
        print(root.attr + " " + root.label)
        print_tree(root.left)

        print_tree(root.right)


def root_def(df_training, target_attr):

    root_node.entropy, root_node.attr, root_node.leftcount, root_node.rightcount = best_attr(
        target_attr, df_training)

    left = df_training[(df_training[root_node.attr] == 0)]
    if(len(left) == 0):
        root_node.left = None
    else:
        root_node.left = Node(None, None, 0, 0, 0,
                              target_attr, '', '', '0', left,True)
        root_node.left.target_attr = [
            s for s in target_attr if s != root_node.attr]
        #root_node.left.target_attr = root_node.left.target_attr.remove(root_node.attr)

    right = df_training[(df_training[root_node.attr] == 1)]
    if(len(right) == 0):
        root_node.right = None
    else:
        root_node.right = Node(None, None, 0, 0, 0,
                               target_attr, '', '', '1', right,True)
        root_node.right.target_attr = [
            s for s in target_attr if s != root_node.attr]
        # print(target_attr)
        # root_node.right.target_attr = root_node.right.target_attr.remove(root_node.attr)
        print(root_node.right.target_attr)
        #root_node.right.target_attr = root_node.right.target_attr.remove(root_node.attr)

    return root_node
    # if entropy = 0 || target_attr.len == 0 stop else generate child nodes

    '''
    root_node.entropy, root_node.attr,root_node.leftcount,root_node.rightcount  = best_attr(target_attr,df_training)
    root_node.target_attr = target_attr.remove(root_node.attr)
    
    '''


def best_attr(target_attr, df):
    min_entropy = 1
    attr = ''
    entropy = 0
    minus_side_len = 0
    plus_side_len = 0

    for col in target_attr:
        minus_side = df[(df[col] == 0)]
        # print(minus_side.head(5))

        minus_side_len = float(len(minus_side))
        plus_side = df[(df[col] == 1)]
        plus_side_len = float(len(plus_side))

        minus_side_zero = len(minus_side[minus_side['Class'] == 0])
        # print(minus_side_zero.head(5))

        minus_side_pos = len(minus_side[minus_side['Class'] == 1])

        plus_side_zero = len(plus_side[plus_side['Class'] == 0])
        plus_side_pos = len(plus_side[plus_side['Class'] == 1])

        entropy_minus = 0
        firstTerm = (minus_side_zero / minus_side_len)
        firstTermLog = 0
        secTerm = (minus_side_pos / minus_side_len)
        secTermLog = 0
        #print(((len(minus_side_zero) / minus_side_len )))
        if(minus_side_zero == 0):
            firstTermLog = 0
        else:
            firstTermLog = ((log10(firstTerm)) / log10(2.0))

        if(minus_side_pos == 0):
            secTermLog = 0
        else:
            secTermLog = ((log10(secTerm)) / log10(2.0))
        entropy_minus = -((firstTerm * firstTermLog) + (secTerm * secTermLog))

        entropy_plus = 0
        firstTerm = (plus_side_zero / plus_side_len)
        secTerm = (plus_side_pos / plus_side_len)
        if(plus_side_zero == 0):
            firstTermLog = 0
        else:
            firstTermLog = ((log10(firstTerm)) / log10(2.0))

        if(plus_side_pos == 0):
            secTermLog = 0
        else:
            secTermLog = ((log10(secTerm)) / log10(2.0))

        entropy_plus = -((firstTerm * firstTermLog) + (secTerm * secTermLog))
        entropy = ((entropy_minus * (minus_side_len / (minus_side_len + plus_side_len))
                    ) + (entropy_plus * (plus_side_len / (minus_side_len + plus_side_len))))
        if(entropy < min_entropy):
            min_entropy = entropy
            attr = col

    print(min_entropy)
    print(attr)
    return min_entropy, attr, minus_side_len, plus_side_len


def cal_entropy(minus_cnt, plus_cnt, total):
    entropy = -[((minus_cnt / total) * (math.log10((minus_cnt / total)) / math.log10(2))
                 ) + ((plus_cnt / total) * (math.log10((plus_cnt / total)) / math.log10(2)))]
    print(entropy)
    return entropy


if __name__ == "__main__":
    main(sys.argv)

    #  a = Test()
    # b = a.test("abc")
