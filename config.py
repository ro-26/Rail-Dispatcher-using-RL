# write your code here to build the Infrastructure Graph and
# attributes of rolling stock and input timetable and initial state

# here we build a simple infrastructure with two incoming tracks(one longer in which a express travels) and
# one shorter where local travels, and it makes one stop, so this track is composed of two track sections) one
# outgoing track and one station following the outgoing track and two signals preceding
# the junction of the two incoming tracks

from infra_builder import InfraBuilder, RollingStock, TimeTable
import math


def simple_infra():
    builder = InfraBuilder()
    tracksection1 = builder.add_track_section((-64.95, 37.5), 37.5, -math.pi / 6)
    tracksection2 = builder.add_track_section((-32.475, 18.75), 37.5, -math.pi / 6)
    tracksection3 = builder.add_track_section((-108.25, -62.5), 125, math.pi / 6)
    tracksection4 = builder.add_track_section((0, 0), 100, 0)
    tracksection5 = builder.add_track_section((100, 0), 200, 0)

    node1 = builder.add_node('node1_2', [tracksection1], [tracksection2])
    node2 = builder.add_node('node23_4', [tracksection2, tracksection3], [tracksection4])

    signal1 = builder.add_signal(tracksection2, 30)
    signal2 = builder.add_signal(tracksection3, 100)

    station = builder.add_station('station1', [tracksection4], [tracksection5], 2)

    return builder


infra = simple_infra()

rolling_stock1 = RollingStock(
    id='train1',
    type='local',
    speed=100,
    acceleration=10,
    deceleration=10
)

timetable1 = TimeTable(
    id='timetable1',
    rolling_stock_id='train1'
)

timetable1.add_stop(
    station='station1',
    arrival_time=2,
    departure_time=4
)

rolling_stock1.schedule = timetable1
