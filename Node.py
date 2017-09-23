class Node:
     

    def _init_():
        self.label =''
        self.leaf_flag
        
    def __init__(self,left,right,entropy,leftcount,rightcount,target_attr,attr,name,label,df,leaf_flag,parent):
        self.left = None
        self.right = None
        self.entropy = entropy
        self.leftcount = leftcount
        self.rightcount = rightcount
        self.target_attr = target_attr
        self.attr = attr
        self.name = name
        self.label = label
        self.df = df
        self.leaf_flag = leaf_flag
        self.parent = parent

    