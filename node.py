class Node:
    def __init__(self, xy_value, parent = None):
        self.xy = xy_value
        self.parent = parent 

    def get_value(self):
        return self.xy

    def get_parent(self):
        return self.parent
    

# n = Node((5, 3))
# print(n.get_value())
