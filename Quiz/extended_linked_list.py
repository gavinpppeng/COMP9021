# Written by Gavin for COMP9021

from linked_list_adt import *


class ExtendedLinkedList(LinkedList):
        def __init__(self, L=None):
            super().__init__(L)
            self.len = super().__len__()

        def rearrange(self, step):
            if not self.head:
                return 0
            end_node = self.head
            while end_node.next_node:
                end_node = end_node.next_node
            end_node.next_node = self.head

            new_node = self.head
            count = step
            while count > 2:
                new_node = new_node.next_node
                count -= 1
            self.head = new_node.next_node
            new_node.next_node = new_node.next_node.next_node
            new_node = self.head

            count = step
            current_node = self.head
            while count > 1:
                for _ in range(count-1):
                    current_node = current_node.next_node
                    if current_node == end_node:
                        count -= 1

                new_node.next_node = current_node.next_node
                current_node.next_node = current_node.next_node.next_node
                new_node = new_node.next_node
                current_node = new_node
            end_node.next_node = None


        def print(self, separator=', '):
            super().print(separator=', ')


'''
    # find the tail and connect the tail with the head
            current_node = self.head
            while (current_node.next_node):
                current_node = current_node.next_node
            tail = current_node
            tail.next_node = self.head

            # find the new head
            previous_node = self.head
            for _ in range(step - 2):
                previous_node = previous_node.next_node
            # previous_node is the target node's previous node, which means
            # if we want to set the head to a specific node, then the previous_node
            # is the target head's previous node
            self.head = previous_node.next_node
            current_node = self.head
            # break the link which points to the target node
            previous_node.next_node = self.head.next_node
            previous_node = self.head

            # every time we loop through the link list, the step should be reduced by 1
            # and we stop at the point that the step is equal to 1
            while (step > 1):
                for _ in range(step - 1):
                    current_node = current_node.next_node
                    # when step loop through the tail, the step should be reduce by 1
                    if (current_node == tail):
                        step -= 1

                previous_node.next_node = current_node.next_node
                current_node.next_node = current_node.next_node.next_node
                current_node = previous_node.next_node
                previous_node = current_node
            tail.next_node = None
'''