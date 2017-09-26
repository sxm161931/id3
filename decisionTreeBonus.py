from __future__ import division
from __future__ import print_function
from math import log10
from Node import Node
import random
import sys
import pandas as pd
import copy

global other_count
global leaf_count
global node_num

def main(args):
    for arg in args[1:]:
        print(arg)

    if(len(sys.argv) == 1):
        # print("Please enter training data file location")
        # loc = raw_input("Please enter training data file location")
        loc = "training_set1.csv"
        loc_val="validation_set.csv"
        loc_test ="test_set.csv"
        df_training = pd.read_csv(loc)
        df_val=pd.read_csv(loc_val)
        df_test=pd.read_csv(loc_test)
    else:
        df_training = pd.read_csv(sys.argv[1])
    # print(df_training)
    # print(len(df_training))
    # print(len(df_training[(df_training['Class']==0)]))
    target_attr = list(df_training)
    #print(len(df_training))
    target_attr.remove('Class')
   # print(len(target_attr))


    global root_node
    global  node_num
    node_num=1
    root_node = Node(None, None, 0, 0, 0, target_attr,
                     '', node_num, '', df_training, False,None)
    root_node = root_def(df_training, target_attr)
    global leaf_count
    global total_count
    global leaf_height
    leaf_height = 0
    total_count = 0
    leaf_count = 0
    build_children(root_node)
    #temp = root_node
    #temp = build_children(temp)

    #print(node_num)
    print("Printing Tree")
#print_tree(root_node)
    printTree(root_node,0)
    # print(total_count)
    # print(leaf_count)
    ntp= int(0.02 * total_count)
    # print(ntp)
    #prune(root_node,ntp,total_count)

    print('Pre-prunned Accuracy' )
    # printDetails(root_node,df_training,df_val,df_test)
    print("--------------------------------------------------------------")
    no_train = len(df_training)
    target_attr_train = list(df_training)
    target_attr_train.remove('Class')
    no_attri = len(target_attr_train)

    print('Number of training instances = ' + str(no_train))
    print('Number of training attributes = ' + str(no_attri ))
    print('Total number of nodes in the tree = ' + str(total_count))
    print('Number of leaf nodes in the tree = ' + str(leaf_count))
    print('Accuracy of the model on the training dataset = ' + getaccuracy(df_training,root_node) )
    print()

    target_attr_val = list(df_val)
    target_attr_val.remove('Class')
    no_attri_val = len(target_attr_val)
    acc_val=getaccuracy(df_val,root_node)
    print('Number of validation instances = ' + str(len(df_val)))
    print('Number of validation attributes = ' +str(no_attri_val))
    print('Accuracy of the model on the validation dataset = ' + getaccuracy(df_val,root_node) )
    print()

    target_attr_test = list(df_test)
    target_attr_test.remove('Class')
    no_attri_test = len(target_attr_test)
    print('Number of testing instances = ' + str(len(df_test)))
    print('Number of testing attributes = ' + str(no_attri_test))
    print('Accuracy of the model on the testing dataset = ' + getaccuracy(df_test,root_node))
    print()
    global sum
    sum =0
    calLeafDept(root_node,0)
    print("Avg depth = " + str(sum/ leaf_count))


def calLeafDept( root,count_tab):
    global sum
    if(root is None):
        return 0
    if(root is not None and root.leaf_flag == True):
        
        count_tab += 1
        sum += count_tab
    else:
        
        
        calLeafDept(root.left,count_tab+1);
       
        
        calLeafDept(root.right,count_tab+1);

    

def build_children(root_node):
    global  node_num
    #print(node_num)

    while(root_node is not None and not root_node.leaf_flag and (len(root_node.target_attr) != 0 ) and root_node.attr != ''):
        left = root_node.df[(root_node.df[root_node.attr] == 0)]
        #print(left.Class.nunique())
        if(left.Class.nunique() == 1):
            val = left['Class'].iloc[0]
            node_num+=1


            #print val
            root_node.left = Node(None, None, 0, len(left), root_node.rightcount,
                                  root_node.target_attr, '', node_num, val, left,True,root_node)

            root_node.left.leaf_flag = True

            #(root_node.left)
        else:
            node_num+=1
            root_node.left = Node(None, None, 0, 0, 0,
                                  root_node.target_attr, '', node_num, '0', left,False,root_node)
            root_node.left.target_attr = copy.deepcopy(root_node.target_attr)
            root_node.left.target_attr.remove(root_node.attr)
            
            root_node.left.entropy, root_node.left.attr, root_node.left.leftcount, root_node.left.rightcount = random_attr(
                root_node.left.target_attr, root_node.left.df)
            if(root_node.left.attr != ''):
                build_children(root_node.left)
            else :
                #root_node.left = None
                root_node.left.leaf_flag = True
                if(root_node.left.leftcount > root_node.left.rightcount):
                    root_node.left.label = '0'
                else:
                    root_node.left.label = '1'

        right = root_node.df[(root_node.df[root_node.attr] == 1)]
        if(right.Class.nunique() == 1):
            val = right['Class'].iloc[0]
            node_num+=1
            root_node.right = Node(None, None, 0, root_node.leftcount, len(right),
                                   root_node.target_attr, '', node_num, val, right,True,root_node)
            root_node.right.leaf_flag = True
            return build_children(root_node.right)
        else:
            node_num+=1
            root_node.right = Node(None, None, 0, 0, 0,
                                   root_node.target_attr, '', node_num, '1', right,False,root_node)

            root_node.right.target_attr = copy.deepcopy(root_node.target_attr)
            root_node.right.target_attr.remove(root_node.attr)
            
            root_node.right.entropy, root_node.right.attr, root_node.right.leftcount, root_node.right.rightcount = random_attr(
                root_node.right.target_attr, root_node.right.df)
            if(root_node.right.attr != ''):
                return build_children(root_node.right)
            else :
                #root_node.left = None
                root_node.right.leaf_flag = True
                if(root_node.right.leftcount > root_node.right.rightcount):
                    root_node.right.label = '0'
                else:
                    root_node.right.label = '1'
                return root_node.right

    return root_node


def printTree( root,count_tab):
    global leaf_count
    global total_count
    if(root is None):
        return
    if(root is not None and root.leaf_flag == True):
        print(root.label)
        leaf_count += 1
        total_count += 1
    else:
        if(count_tab!=0):
            print ()
        for i in range(0,count_tab):
            print("|  " , end = ' ')
        print(root.attr +" = 0 : ", end=" ")
        total_count += 1
        printTree(root.left,count_tab+1);
        for i in range(0,count_tab):
            print("|  ",end=" ")
        print(root.attr+" = 1 : ",end=" ")
        printTree(root.right,count_tab+1);


def print_tree(root):

    if root is None:
        return
    elif root.leaf_flag :
        print("leaf node"+ root.attr + "decision " + str(root.label))

        return
    else:
        print(root.attr + " " + "0")
        print_tree(root.left)
        print(root.attr + " " + "1")
        print_tree(root.right)


def root_def(df_training, target_attr):
    global node_num
    root_node.entropy, root_node.attr, root_node.leftcount, root_node.rightcount = random_attr(
        target_attr, df_training)

    

    return root_node



def random_attr(target_attr, df):
    min_entropy = 1
    attr = ''
    entropy = 0
    minus_side_len = 0
    plus_side_len = 0


    if(len(target_attr) > 0) : 
        col = random.choice(target_attr)
        #col = target_attr[0]
        #print(col)
        minus_side = df[(df[col] == 0)]
            # print(minus_side.head(5))

        minus_side_len = float(len(minus_side))
        plus_side = df[(df[col] == 1)]
        plus_side_len = float(len(plus_side))

        attr = col
        if minus_side_len == 0 or plus_side_len ==0 :
            attr = ''
        
    return min_entropy, attr, minus_side_len, plus_side_len


def getclass(instance, tree,default=None):
    attribute = tree.attr
    if(tree.left is not None and tree.right is not None):
        #  print(instance[attribute])
        if instance[attribute]== 0 :
            return getclass(instance,tree.left)
        elif instance[attribute]== 1 :
            return getclass(instance,tree.right)
    elif(tree.leaf_flag== True):
        lab = tree.label
        return lab



def getaccuracy(df,root_node):
    df['predicted'] = (df.apply(getclass, axis=1, args=(root_node, '1')))
    acc = str( sum(df['Class']==df['predicted'] ) / (1.0*len(df.index))*100.0)
    #df.remove['predicted']
    return acc





def trim(node,node_to_prune):
    # print(node_to_prune)
    #print("node name"+ str(node.name))
    #print("node_to_prune" + str(node_to_prune))
    node_found_flag=False
    if node is None :
        return False

    else:
        if(node.name==node_to_prune and node.left is not None and node.right is not None and node.left.right is None and node.left.left is None and node.right.left is None and node.right.right is None):
            #print("matching node")
            node.left = None
            node.right = None
            node.leaf_flag = True
            if(node.leftcount>node.rightcount):
                node.label=0
            else:
                node.label=1
            node_found_flag = True
            return node_found_flag
        else:
            node_found_flag = trim(node.left,node_to_prune)
            if(not node_found_flag):
                return trim(node.right,node_to_prune)
    return node_found_flag
    # print(node_found_flag)




#if __name__ == "__main__":
main(sys.argv)