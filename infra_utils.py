# Contains the objects that are needed to build the infrastructure :

# TrackSection : Object which models the railway track on which rolling stock runs on
# its bidirectional and Stations and Signals are placed relative to the start of the TrackSection
# the ends of the TrackSection can either be open or connected to other TrackSection via Nodes.

# Node : Object which models the link between TrackSections in this project. It has certain incoming TrackSections
# and certain outgoing TrackSections.

# Station : Object which models the stations in real life. Like Node it has certain incoming TrackSections
# and certain outgoing TrackSections but trains can stop here for some time, but it has a holding capacity.

# Signal: Object which models the train signals. If it is red then the TrackSection ahead of it is occupied and the
# incoming train has to stop until it changes to green.

import math


class TrackSection:
    def __init__(self, start, length, angle):
        """
        start(tuple) : Tuple contains the coordinates of starting point
        length(float): Float value representing the length of the TrackSection
        angle(float): Angle of the TrackSection in radians
        """
        if type(start) != tuple:
            raise TypeError('The start location must be specified using Tuple')
        for x in start:
            if type(x) != float and type(x) != int:
                raise TypeError('Only float is allowed for specifying coordinates')
        if type(length) != float and type(length) != int:
            raise TypeError('Only float is allowed for specifying lengths')
        self.start = start
        self.length = length
        self.angle = angle
        self.objects = {}  # Relative position : object(Station,Signal)

    def get_end_position(self):
        start_x, start_y = self.start
        end_x = start_x + self.length * round(math.cos(self.angle), 3)
        end_y = start_y + self.length * round(math.sin(self.angle), 3)
        return end_x, end_y

    def add_object(self, object, pos):
        """
        object: Either a Station or a Signal that needed to be placed along the TrackSection
        pos: Relative distance of the object from the starting of the TrackSection
        """
        if type(pos) != float and type(pos) != int:
            raise TypeError('Use float to specify the relative position')
        if pos >= self.length:
            raise Exception('The position of the object exceeds the length of the TrackSection')
        self.objects[pos] = object


class Node:
    def __init__(self, incoming, outgoing, location):
        """
        incoming(list): Collection of incoming TrackSections
        outgoing(List): Collection of outgoing TrackSections
        location(tuple): Coordinates of the node location
        """
        if type(incoming) != list and type(outgoing) != list:
            raise TypeError('Use List to define collection of TrackSections')
        for x in incoming + outgoing:
            if not isinstance(x, TrackSection):
                raise TypeError('The object used is not an instance of class TrackSection')
        if type(location) != tuple:
            raise TypeError('The location must be specified using Tuple')
        for x in location:
            if type(x) != float:
                raise TypeError('Only float is allowed for specifying coordinates')

        self.incoming = incoming
        self.outgoing = outgoing
        self.location = location


class Station:
    def __init__(self, incoming, outgoing, capacity):
        """
        incoming(list): Collection of incoming TrackSections
        outgoing(List): Collection of outgoing TrackSections
        capacity(int): Max # of trains that the Station could hold at any given time
        """
        if type(incoming) != list and type(outgoing) != list:
            raise TypeError('Use List to define collection of TrackSections')
        for x in incoming + outgoing:
            if not isinstance(x, TrackSection):
                raise TypeError('The object used is not an instance of class TrackSection')
        if type(capacity) != int:
            raise TypeError('The value of capacity must be an int')
        self.incoming = incoming
        self.outgoing = outgoing
        self.capacity = capacity


class Signal:
    def __init__(self):
        self.status = 'RED'

    def change_status(self):
        if self.status == 'RED':
            self.status = 'GREEN'
        else:
            self.status = 'RED'
