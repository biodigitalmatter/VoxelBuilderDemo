import numpy as np

def create_zero_array(n):
    # create voxel-like array
    a = np.zeros(n ** 3)  # 3 dimensional numpy array representing voxel voxel
    a = np.reshape(a, [n, n, n])
    return a

def create_random_array(n):
    # create voxel-like array
    a = np.random.random(n ** 3)
    a = np.reshape(a, [n, n, n])
    return a

class Layer:
    def __init__(self, name = 'Air', voxel_size = 100, diffusion_strength = 1/12, rgb = [1, 0.5, 0.5], axis_order = ['z', 'y', 'x']):
        self._name = name
        self._n = voxel_size
        self._d = diffusion_strength
        self._rgb = rgb
        self._axis_order = axis_order
        self._array = None
        
    def __repr__(self):
        return f"Layer(_name={self._name}, voxel_shape={self._array.shape}, diffusion_strength={self.diffusion_strength}, rgb={self._rgb}, axis_order = {self._axis_order})"

    def zeros(self):
        self._array = np.zeros(self._n ** 3).reshape([self._n, self._n, self._n])
        return self._array
    
    def random(self, add = 0, strech = 1, crop = False, start = 0, end = 1):
        self._array = (np.random.random(self._n ** 3).reshape(self._n,self._n,self._n) + add) * strech
        if crop:
            self._array = self.crop_array(self._array, start ,end)


    
    def crop_array(self, array, start = 0, end = 1):
        array = np.minimum(array, end)
        array = np.maximum(array, start)
        return array
    
    def diffuse(self, repeat = 1, limit_by_Hirsh = True):
        """every value of the voxel cube diffuses with its face nb
         standard finite volume approach (Hirsch, 1988). 
         diffusion change of voxel_x between voxel_x and y:
           delta_x = -a(x-y) 
           where 0 <= a <= 1/6 
        """
        if limit_by_Hirsh:
            self._d = max(0, self._d)
            self._d = min(1/6, self._d)
        
        shifts = [-1, 1]
        axes = [0,0,1,1,2,2]
        for j in range(repeat):
            # six face nb 
            total_diffusions = create_zero_array(self._n)
            
            for i in range(6):
                y = np.copy(self._array)
                y = np.roll(y, shifts[i % 2], axis = axes[i])
                diffusion_one_side = -1 * self._d * (self._array - y)
                total_diffusions += diffusion_one_side
                # print('total_diffusions', total_diffusions)
        
            self._array += total_diffusions

        
        return self._array
    
    def get_color_dimension(self):
        r,g,b = self._rgb
        colors = np.copy(self.array)
        colors = (1 - self.crop_array(colors, 0, 1))
        reds = np.reshape(colors * (r), [self._n, self._n, self._n, 1])
        greens = np.reshape(colors * (g), [self._n, self._n, self._n, 1])
        blues = np.reshape(colors * (b), [self._n, self._n, self._n, 1])
        self._colors = np.concatenate((reds, greens, blues), axis = -1)
        return self._colors
    
    # Property getters
    @property
    def colors(self):
        self.get_color_dimension()
        return self._colors

    @property
    def rgb(self):
        return self._rgb
    
    @property
    def diffusion_strength(self):
        return self._d
    
    @property
    def axis_order(self):
        return self._axis_order
    
    @property
    def color(self):
        return self._color
    
    @property
    def array(self):
        return self._array
    
    # Property setters
    @array.setter
    def array(self, a):
        """Setter method for size property"""
        if not isinstance(a, np.ndarray):
            raise ValueError("Size must be a np.ndarray instance")
        if np.ndim(a) != 3:
            raise ValueError("Array should be 3D")
        self._array = a
    
    @rgb.setter
    def rgb(self, a):
        """Setter method for size property"""
        if not isinstance(a, list):
            raise ValueError("rgb must be a list of three floats")
        if len(a) != 3:
            raise ValueError("list length should be 3")
        self._rgb = a



class Agent:
    def __init__(self, position, movement_limitations, pathpheromon_strength):
        self.position = position  # tuple representing the agent's position in the environment
        self.movement_limitations = movement_limitations  # constraints on agent's movement
        self.pathpheromon_strength = pathpheromon_strength  # strength of the path pheromone

    def move(self):
        # Implementation of agent movement
        pass

    def check_move_options(self):
        # Implementation to check possible movement options
        pass

    def get_impulse(self):
        # Implementation to get the impulse controlling the agent
        pass

    def get_neighbor_voxels(self):
        # Implementation to get neighboring voxels in the environment
        pass

    def __repr__(self):
        return f"Agent(position={self.position}, movement_limitations={self.movement_limitations}, pathpheromon_strength={self.pathpheromon_strength})"


def overlay_layers(layers, weight_mask):
    # add several layers
    pass

def dump_state(state):
    # Implementation to dump the state of a layer or the entire world
    pass

def load_as_built(self, as_built_data):
    # Implementation to load AsBuilt data
    pass


"""
# Examples of layers
earth = Layer(name="Earth", voxel=np.zeros((10, 10, 10)), diffusion_strength=0.5, color='brown', attraction_strength=0.1)
air = Layer(name="Air", voxel=np.ones((10, 10, 10)), diffusion_strength=0.1, color='blue', attraction_strength=0.05)
path_pheromons = Layer(name="PathPheromons", voxel=np.zeros((10, 10, 10)), diffusion_strength=0.8, color='green', attraction_strength=0.3)
food_pheromons = Layer(name="FoodPheromons", voxel=np.zeros((10, 10, 10)), diffusion_strength=0.7, color='red', attraction_strength=0.4)
as_built = Layer(name="AsBuilt", voxel=np.zeros((10, 10, 10)), diffusion_strength=0.2, color='grey', attraction_strength=0.0)
collision_area = Layer(name="CollisionArea", voxel=np.zeros((10, 10, 10)), diffusion_strength=0.0, color='black', attraction_strength=0.0)

# Examples of agents
builder = Agent(position=(5, 5, 5), movement_limitations={'max_steps': 10}, pathpheromon_strength=0.9)
explorer = Agent(position=(2, 2, 2), movement_limitations={'max_steps': 15}, pathpheromon_strength=0.6)

# Example of mechanism usage
voxel_engine = VoxelEngine()
voxel_engine.add_layer(earth)
voxel_engine.add_layer(air)
voxel_engine.build_voxel()

# Diffuse a layer
voxel_engine.diffuse_a_layer(earth)

# Overlay layers
voxel_engine.overlay_layers([earth, air, path_pheromons])

# Dump and load state
voxel_engine.dump_state(earth)
voxel_engine.load_as_built(as_built)
"""