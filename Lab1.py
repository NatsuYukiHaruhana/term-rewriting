from typing import Optional

functions = {
    'f': 2,
    'i': 1,
    'e': 0
}
variables = set(['x', 'y'])

class Node:
    def __init__(self, value="", previous=None, next=None):
        self.value = value
        self.previous = previous
        self.next = next


def CreateTree(filename: str) -> Optional[Node] :
    """
        This function takes in a string filename, reads the first line
        and returns the corresponding tree, if it can be created. It will otherwise return None.
    Args:
        filename (str): path to file to read from

    Returns:
        Optional[Node]: returns the head of the tree or None if it can't be created
    """
    with open(filename, "r") as fileInput:
        input_str = fileInput.readline()
            
    head = Node()
    current_node = head
    
    for char in input_str:
        if char in functions.keys(): # if current char represents a function
            if current_node.value != "":
                print("Error in string! More than one function is trying to occupy the same node!")
                return None
            current_node.value = char # first we note this down
            
            if functions[char] > 0:
                current_node.next = [] # we prepare a list of Nodes if the function takes more than zero arguments

                for _ in range(0, functions[char]): # then we add as many further Nodes as the function has possible arguments
                    current_node.next.append(Node(previous=current_node))
        elif char == '(':
            if current_node.next == None:
                print("Error in string! There's an open paranthesis, but we're not expecting any arguments!")
                return None
            
            current_node = current_node.next[0] # we go in the first Node in the list of children of the current one
        elif char == ')':
            if current_node.previous == None:
                print("Error in string! There are too many closed parantheses!")
                return None
            
            if current_node.next != None:
                for node in current_node.next:
                    if node.value == "":
                        print("Error in string! Function is still expecting arguments!")
                        return None
            
            current_node = current_node.previous # we jump one level above our current one
        elif char == ',':
            if current_node.previous == None: # if there is no higher level to jump to
                print("Error in string! Too many commas!")
                return None
            
            current_node = current_node.previous # we need to jump a level up
            initial_node = current_node
            for node in current_node.next: # look for a Node which hasn't been populated yet
                if node.value == "":
                    current_node = node
                    break
                
            if current_node == initial_node: # we couldn't find an unpopulated Node
                print("Error in string! Function given more arguments than it can accept!")
                return None
        elif char in variables:
            if current_node.value != "":
                print("Error in string! More than one variable is trying to occupy the same node!")
                return None
            
            current_node.value = char

    return head


def PrintTree(head: Node, spacing: int = 2, current_level: int = 0) -> None:
    """
    This function takes in the head of a tree and prints the content out to the console.

    Args:
        head (Node): head of the tree you want to display
        spacing (int): how many whitespaces and dash characters should be used when displaying a new line (has to be > 0)
        current_level (int): the current level of the tree (this shouldn't be given as a parameter on the first call)
    """
    print(' ' * (spacing + 1) * (current_level - 1) + ('+' + '-' * spacing) * (current_level > 0) + head.value)
    
    if head.next == None: # no more children to look into
        return
    
    for node in head.next:
        PrintTree(node, spacing, current_level + 1)
    

def main():
    head = CreateTree("input.txt")
    
    if head != None:
        PrintTree(head)

if __name__ == "__main__":
    main()
