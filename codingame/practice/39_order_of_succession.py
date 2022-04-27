'''

https://www.codingame.com/training/easy/order-of-succession

'''

from typing import Optional


class Person():
    def __init__(self, name, parent, birth, death, religion, gender):
        self.name = name
        self.parent = parent or None
        self.birth = birth
        self.death = death if death.isdigit() else None
        self.religion = religion
        self.gender = gender

    @property
    def is_included(self):
        """Only alive non Catholic persons are included"""
        return not self.death and self.religion != "Catholic"

    def __repr__(self):
        """Just the string representation of a person"""
        parent = self.parent.name if self.parent else '-'
        return (f"{self.name} {parent} {self.birth} {self.death or '-'} {self.religion} {self.gender}")

    def __eq__(self, other):
        """This is needed for the sorted"""
        if not self or not other:
            return False
        return self.name == other.name

    def __lt__(self, other):
        """Sort a person based on the gender first and then the age"""
        priority = {'M': 1, 'F': 2}

        if self.gender == other.gender:
            return self.birth < other.birth
        return priority[self.gender] < priority[other.gender]


def find_root(tree: list) -> Person:
    """Find the root of the tree which is the person w/o parent"""
    return [p for p in tree if p.parent is None][0]


def get_children(person: Person, tree: list) -> list:
    """Get the children list"""
    return [p for p in tree if p.parent is not None if p.parent.name == person.name]


def get_next_sibling(person: Optional[Person], tree: list) -> Optional[Person]:
    """Find the next sibling of a person"""

    # If no person is provided, then return None
    if not person:
        return None

    # Find the siblings of the persons and sort them.
    siblings = sorted([p for p in tree if p.parent == person.parent])

    # First locate the current person, the find the first available sibling.
    this_person_found = False
    for s in siblings:
        # When locating the current person it moves directly to the next one.
        if not this_person_found and s == person:
            this_person_found = True
            continue

        # When the current person is found, return the next.
        if this_person_found:
            return s
    else:
        return None


def get_first_child(person: Person, tree: list) -> Optional[Person]:
    """Find the first child from a list of siblings"""
    
    # Find all the children
    children = get_children(person, tree)

    # Return the first one 
    return None if len(children) == 0 else sorted(children)[0]


def find_successor(person: Optional[Person], tree: list) -> Optional[Person]:
    """Find the successor of a person"""

    if not person:
        return None

    # Find the first child
    first_child = get_first_child(person, tree)
    if first_child:
        return first_child

    beneficial = person
    while True:
        next_sibling = get_next_sibling(beneficial, tree)
        
        # If they have a sibling the we are done.
        if next_sibling:
            return next_sibling
        
        # If there are not siblings move one generation upwards.
        if not beneficial.parent:
            return None
        beneficial = beneficial.parent

def get_succession(tree: list) -> list:
    """Get the succession list of a tree following the rules"""
    # Find the root of the tree
    successor = find_root(tree)

    # Add the root of the tree if they are included
    successors = []
    if successor.is_included:
        successors.append(successor)

    # Find the successors recursively
    while True:
        successor = find_successor(successor, tree)
        if successor:
            if successor.is_included:
                successors.append(successor)
        else:
            return successors


def read_tree(n) -> list:
    """Read the tree list and construct a list of persons,
    where the parents are also persons"""
    tree = []
    for i in range(n):
        inputs = input().split()
        
        parent = None
        for person in tree:
            if person.name == inputs[1]:
                parent = person

        p = Person(
            name=inputs[0],
            parent=parent,
            birth=inputs[2],
            death=inputs[3],
            religion=inputs[4],
            gender=inputs[5],
        )
        tree.append(p)
    return tree

# Read the tree from the input
tree = read_tree(int(input()))

# Get the succession of the tree 
succession = get_succession(tree)

# Print out the names of successors
for s in succession:
    print(s.name)

