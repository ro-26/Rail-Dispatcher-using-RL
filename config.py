# write your code here to build the Infrastructure Graph and
# attributes of rolling stock and input timetable and initial state

# here we build a simple infrastructure with two incoming tracks(one longer in which a express travels) and
# one shorter where local travels, and it makes one stop, so this track is composed of two track sections) one
# outgoing track and one station following the outgoing track and two signals preceding
# the junction of the two incoming tracks

from infra_builder import InfraBuilder
import math


def simple_infra():
    builder = InfraBuilder()
    tracksection1 = builder.add_track_section((-64.95, 37.5), 37.5, -math.pi/6)
    tracksection2 = builder.add_track_section((-32.475, 18.75), 37.5, -math.pi/6)
    tracksection3 = builder.add_track_section((-108.25, -62.5), 125, math.pi/6)
    tracksection4 = builder.add_track_section((0, 0), 100, 0)

    node1 = builder.add_node('node1_2', [tracksection1], [tracksection2])
    node2 = builder.add_node('node23_4', [tracksection2, tracksection3], [tracksection4])

    return builder

simple_infra()