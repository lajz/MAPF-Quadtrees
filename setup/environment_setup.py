from classes.simple_objects.position import Position
from classes.simple_objects.range import Range
from classes.simple_objects.shape import Shape


# class for defining creation of obstacles or restricted areas
class ObstacleInitializer:

    def __init__(self, position: Position, shape: Shape):
        self.position = position
        self.shape = shape


# class for defining creation of agents, from start and end position
class AgentInitializer:

    def __init__ (self, start_position:Position, end_position:Position, shape:Shape, max_speed):
        self.start_position = start_position
        self.end_position = end_position
        self.shape = shape
        self.max_speed = max_speed


# class for defining creation of enviroment that agents will operate in
class Environment:

    def __init__(self, range_x: Range, range_y: Range, obstacle_initializers: [ObstacleInitializer], agent_initializers: [AgentInitializer]):
        self.range_x = range_x
        self.range_y = range_y
        self.obstacle_initializers = obstacle_initializers
        self.agent_initializers = agent_initializers
