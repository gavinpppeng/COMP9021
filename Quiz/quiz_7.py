# Defines two classes, Point() and Disk().
# The latter has an "area" attribute and three methods:
# - change_radius(r)
# - intersects(disk), that returns True or False depending on whether
#   the disk provided as argument intersects the disk object.
# - absorb(disk), that returns a new disk object that represents the smallest
#   disk that contains both the disk provided as argument and the disk object.
#
# Written by Gavin and Eric Martin for COMP9021


from math import pi, hypot


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point({self.x:.2f}, {self.y:.2f})'


class Disk:
    def __init__(self, *, centre=Point(0, 0), radius=0):
        self.centre = centre
        self.centre.x = centre.x
        self.centre.y = centre.y
        self.radius = radius
        self.area = pi * radius ** 2

    def __repr__(self):
        return f'Disk(Point({self.centre.x:.2f},{self.centre.y:.2f}), {self.radius:.2f})'

    def change_radius(self, radius=0):
        self.radius = radius
        self.area = pi * radius ** 2

    def intersects(self, disk):
        distance = hypot((disk.centre.x - self.centre.x), (disk.centre.y - self.centre.y))
        sum_radius = disk.radius + self.radius
        if sum_radius >= distance:
            return True
        else:
            return False

    def absorb(self, disk):
        distance = hypot((disk.centre.x - self.centre.x), (disk.centre.y - self.centre.y))
        if distance <= (abs(self.radius - disk.radius)):
            if self.radius >= disk.radius:
                new_disk = self
            else:
                new_disk = disk
            return new_disk
        else:
            r3 = (self.radius + disk.radius + distance)/2
            ratio = (r3 - self.radius) / (r3 - disk.radius)
            x3 = (self.centre.x + ratio * disk.centre.x) / (1 + ratio)
            y3 = (self.centre.y + ratio * disk.centre.y) / (1 + ratio)
            new_disk = Disk(centre=Point(x3,y3), radius=r3)
            return new_disk

'''
disk = Disk(centre=Point(1,2),radius=6)
print(disk)
disk2 = Disk(centre=Point(-2,0),radius=5)
disk3 = disk.absorb(disk2)
print(disk3)
'''



