'''
Created on 24/10/2012

@author: diego.peinado
'''
class Node:
    data, left, right, = 0, None, None
     
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
         
class BTree:
    # Creates new nodes
    def create(self, node, data):
        # Check if node has a root and create it if necessary
        if node is None:
            return Node(data)
        else:
            if data <= node.data:
                node.left = self.create(node.left, data)
                return node.left
            elif data >= node.data:
                node.right = self.create(node.right, data)
                return node.right
     
    # Gets the node in the tree
    def read(self, node, target):
        if (target or node) is None:
            return None
        elif target == node.data:
            return node
        else:
            if target < node.data:
                return self.read(node.left, target)
            elif target > node.data:
                return self.read(node.right, target)
     
    # Gets the parent of the specified node to search for
    def readParent(self, node, target, parent):
        if (target or node) is None:
            return None
        elif target.data == node.data:
            return parent
        else:
            if target.data < node.data:
                return self.readParent(node.left, target, node)
            elif target.data > node.data:
                return self.readParent(node.right, target, node)
         
    # Non-recursive deletion
    def delete(self, root, target):
        node = self.read(root, target)
        nodeParent = self.readParent(root, node, None)
         
        if (node.left and node.right) is None:
            # Delete parent pointers and the node pointer
            if nodeParent is not None and nodeParent.left is not None:
                if nodeParent.left == node:
                    del nodeParent.left
            if nodeParent is not None and nodeParent.right is not None:
                if nodeParent.right == node:
                    del nodeParent.right
                 
            del node
        else:                
            # Restructure internal nodes, then delete
            # Internal nodes are replaced, parents will not need to be deleted
            if node.data < root.data:
                node.right.left = node.left
                node = node.right
            elif node.data > root.data:
                node.left.right = node.right
                node = node.left
     
    # Gets the size of the tree
    def size(self, node):
        if node is None:
            return 0
        else:
            return self.size(node.left) + 1 + self.size(node.right)
         
    # Gets the height of the tree
    def maxDepth(self, node):
        if (node.left and node.right) is None:
            return 0
        else:
            lDepth = self.maxDepth(node.left)
            rDepth = self.maxDepth(node.right)
             
            return (max(lDepth, rDepth) + 1)
     
    # Gets the minimum value
    def minValue(self, node):
        while node.left is not None:
            node = node.left
        return node.data
     
    # Gets the maximum value
    def maxValue(self, node):
        while node.right is not None:
            node = node.right
        return node.data
     
    # Prints the tree with print()
    def printTree(self, node):
        if node is not None:
            self.printTree(node.left)
            print(node.data)
            self.printTree(node.right)
def main():
    
    # Instantiate the tree
    tree = BTree()
 
# Add a root element
    root = tree.create(None, 5)
 
# Add children
    child1 = tree.create(root, 4)
    child2 = tree.create(root, 6)
    child3 = tree.create(child1, 3)
    child4 = tree.create(child1, 8)
    child5 = tree.create(child2,9)
    child6 = tree.create(child2,1)
# Delete a child
    #tree.delete(root, 6)
 
    print(tree.printTree(root))
    
    
main()
 