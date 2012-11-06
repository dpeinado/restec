'''
Created on 24/10/2012

@author: diego.peinado
'''
def left(index):
    return 2 * index + 1

def right(index):
    return 2 * index + 2

def parent(index):
    return index / 2

def inorder(tree, index):
    """Here's a sample algorithm that uses this tree
       representation.  Inorder traversal."""
    if index >= len(tree):
        return
    inorder(tree, left(index))
    print tree[index]
    inorder(tree, right(index))

def preorder(tree, index):
    if index >= len(tree): return
    print tree[index]
    preorder(tree, left(index))
    preorder(tree, right(index))

if __name__ == '__main__':
    mytree = [1, 2, 3, 4, 5, 6, 7, 8]
    print "Here's an inorder traversal of our mytree."
    inorder(mytree, 0)   ## Start an inorder traversal at the root at 0.
    print
    print "Here's a preorder traversal:"
    preorder(mytree, 0)