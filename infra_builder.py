from dataclasses import dataclass, field
import networkx as nx

from infra_utils import TrackSection, Node, Station, Signal


@dataclass
class InfraBuilder:
    track_sections: list = field(default_factory=list)
    nodes: dict = field(default_factory=dict)
    stations: dict = field(default_factory=dict)
    signals: list = field(default_factory=list)
    graph: nx.Graph = field(default_factory=nx.Graph)

    def add_track_section(self, start, length, angle):
        track_section = TrackSection(start, length, angle)
        self.track_sections.append(track_section)
        return track_section

    def add_node(self, node_id, incoming_tracks, outgoing_tracks):
        # Validate that the incoming track sections intersect at the end
        end_positions = []
        for track in incoming_tracks:
            end_position = track.get_end_position()
            end_positions.append(end_position)

        # Check if all end positions are the same
        first_end_position = end_positions[0]
        if len(incoming_tracks) >= 2:
            for end_position in end_positions[1:]:
                if end_position != first_end_position:
                    raise ValueError("The incoming track sections do not intersect at the end.")

        # Compute the node location
        node_location = first_end_position

        node = Node(incoming_tracks, outgoing_tracks, node_location)
        self.nodes[node_id] = node
        self.add_to_graph(node_id, incoming_tracks, outgoing_tracks)
        return node

    def add_station(self, station_id, incoming_tracks, outgoing_tracks, capacity):
        station = Station(incoming_tracks, outgoing_tracks, capacity)
        self.stations[station_id] = station
        self.add_to_graph(station_id, incoming_tracks, outgoing_tracks)
        return station

    def add_signal(self, track_section, position):
        signal = Signal()
        track_section.add_object(signal, position)
        self.signals.append(signal)
        return signal

    def add_to_graph(self, node_or_station_id, incoming_tracks, outgoing_tracks):
        for track in incoming_tracks:
            self.graph.add_edge(track, node_or_station_id, weight=track.length)
        for track in outgoing_tracks:
            self.graph.add_edge(node_or_station_id, track, weight=track.length)

    def build_graph(self):
        # To facilitate finding path from starting station to destination along the stations
        # mentioned in timetable
        for node_id, node in self.nodes.items():
            self.add_to_graph(node_id, node.incoming, node.outgoing)
        for station_id, station in self.stations.items():
            self.add_to_graph(station_id, station.incoming, station.outgoing)
        return self.graph
