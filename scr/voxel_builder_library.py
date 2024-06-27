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
    def __init__(self, name = '', voxel_size = 20, rgb = [1,1,1], 
                diffusion_ratio = 0.12, diffusion_random_factor = 0,
                decay_ratio = 0, decay_random_factor = 0, decay_linear_value = 0,
                gradient_resolution = 0):
        
        self._array = None # value array
        self._color_array = None # colored array 4D
        self._axis_order = 'zyx'
        self._name = name
        self._n = voxel_size
        self._rgb = rgb
        self._diffusion_ratio = diffusion_ratio
        self._diffusion_random_factor = diffusion_random_factor
        self._decay_ratio = decay_ratio
        self._decay_random_factor = decay_random_factor
        self._decay_linear_value = decay_linear_value
        self._gradient_resolution = gradient_resolution
        self._voxel_crop_range = [0,1] # too much
        self._iter_count = 0
    
    def __str__(self):
        properties = []
        count = 0
        for name in dir(self):
            if isinstance(getattr(self.__class__, name, None), property):
                # Conditionally exclude properties from the string
                if name == 'array' or name == "color_array":  # Example condition: exclude 'voxel_size' property
                    pass
                else:
                    value = getattr(self, name)
                    properties.append(f"{name}={value}")
                    # if (count % 2) == 1:
                    properties.append('\n')
                    count += 1
        return f"{self.__class__.__name__}({', '.join(properties)})"
    


    def get_params(self):
        text = str(self.__str__)
        return text
    
    # Property getters
    @property
    def array(self):
        return self._array
    
    @property
    def color_array(self):
        self.calculate_color_array()
        return self._color_array
    
    @property
    def name(self):
        return self._name

    @property
    def voxel_size(self):
        return self._n

    @property
    def rgb(self):
        return self._rgb

    @property
    def diffusion_ratio(self):
        return self._diffusion_ratio

    @property
    def diffusion_random_factor(self):
        return self._diffusion_random_factor

    @property
    def decay_ratio(self):
        self._decay_ratio = abs(self._decay_ratio * -1)
        return self._decay_ratio

    @property
    def decay_linear_value(self):
        return self._decay_linear_value

    @property
    def decay_random_factor(self):
        return self._decay_random_factor

    @property
    def decay_linear_value(self):
        self._decay_linear_value = abs(self._decay_linear_value * -1)
        return self._decay_linear_value

    @property
    def axis_order(self):
        return self._axis_order

    @property
    def gradient_resolution(self):
        return self._gradient_resolution

    @property
    def iter_count(self):
        return self._iter_count

    # Property setters
    @array.setter
    def array(self, a):
        """Setter method for size property"""
        if not isinstance(a, np.ndarray):
            raise ValueError("must be a np.ndarray instance")
        if np.ndim(a) != 3:
            raise ValueError("Array should be 3D, in shape [n,n,n]")
        self._array = a

    @color_array.setter
    def color_array(self, a):
        """Setter method for size property"""
        if not isinstance(a, np.ndarray):
            raise ValueError("Size must be a np.ndarray instance")
        if np.ndim(a) != 3:
            raise ValueError("Array should be 4D, in shape [n, n, n, 3]")
        self._array = a
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        self._name = value

    @voxel_size.setter
    def voxel_size(self, value):
        if not isinstance(value, (int)):
            raise ValueError("Voxel size must be an integrer")
        self._n = value

    @rgb.setter
    def rgb(self, a):
        """Setter method for size property"""
        if not isinstance(a, (list, tuple, np.ndarray)):
            raise ValueError("rgb must be a list of three floats")
        self._rgb = a

    @diffusion_ratio.setter
    def diffusion_ratio(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Diffusion ratio must be a number")
        self._diffusion_ratio = value

    @diffusion_random_factor.setter
    def diffusion_random_factor(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Diffusion random factor must be a number")
        if not 0 <= value:
            raise ValueError('Diffusion random factor must be non-negative')
        self._diffusion_random_factor = value

    @decay_ratio.setter
    def decay_ratio(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Decay ratio must be a number")
        if not 0 <= value:
            raise ValueError('Decay ratio must be non-negative')
        self._decay_ratio = value

    @decay_linear_value.setter
    def decay_linear_ratio(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Decay linear ratio must be a number")
        self._decay_linear_value = value

    @decay_random_factor.setter
    def decay_random_factor(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Decay random factor must be a number")
        self._decay_random_factor = value

    @decay_linear_value.setter
    def decay_linear_value(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Decay linear value must be a number")
        self._decay_linear_value = value

    @axis_order.setter
    def axis_order(self, value):
        if not isinstance(value, (list, tuple)):
            raise ValueError("Axis order must be a list or tuple")
        self._axis_order = value

    @gradient_resolution.setter
    def gradient_resolution(self, value):
        if not isinstance(value, (int)) or value < 0 :
            raise ValueError("Gradient resolution must be a nonnegative integrer")
        self._gradient_resolution = value
    
    @property
    def voxel_crop_range(self):
        return self._voxel_crop_range
    
    @voxel_crop_range.setter
    def voxel_crop_range(self,value):
        if not(isinstance(list, tuple)):
            raise ValueError('range must be a list or tuple of floats')
        self._voxel_crop_range = value

    def empty_array(self):
        self._array = np.zeros(self._n ** 3).reshape([self._n, self._n, self._n])
    
    def random(self, add = 0, strech = 1, crop = False, start = 0, end = 1):
        self._array = (np.random.random(self._n ** 3).reshape(self._n,self._n,self._n) + add) * strech
        if crop:
            self._array = self.crop_array(self._array, start ,end)

    def crop_array(self, array, start = 0, end = 1):
        array = np.minimum(array, end)
        array = np.maximum(array, start)
        return array
    
    def conditional_fill(self, condition = '<', value = 0.5, override_self = False):
        """returns new voxel_array with 0,1 values based on condition"""
        if condition == '<':
            mask_inv = self.array < value
        elif condition == '>':
            mask_inv = self.array > value
        elif condition == '<=':
            mask_inv = self.array <= value
        elif condition == '>=':
            mask_inv = self.array >=  value
        a = create_zero_array(self._n)
        a[mask_inv] = 0
        if override_self:
            self.array = a
        return a

    def get_nonzero_point_list(self, array):
        """returns indicies of nonzero values
        if list_of_points:
            shape = [n,3]
        else:
            shape = [3,n]"""
        non_zero_array = np.nonzero(array)
        return np.transpose(non_zero_array)
    
    def get_nonzero_index_coordinates(self, array):
        """returns indicies of nonzero values
        list of coordinates
            shape = [3,n]"""
        non_zero_array = np.nonzero(array)
        return non_zero_array
    
    def grade(self):
        if self.gradient_resolution == 0:
            pass
        else:
            self._array = np.int64(self.array * self._gradient_resolution) / self._gradient_resolution
    
    def diffuse(self, limit_by_Hirsh = True, reintroduce_on_the_other_end = False):
        """infinitive borders
        every value of the voxel cube diffuses with its face nb
        standard finite volume approach (Hirsch, 1988). 
        diffusion change of voxel_x between voxel_x and y:
        delta_x = -a(x-y) 
        where 0 <= a <= 1/6 
        """
        if limit_by_Hirsh:
            self._diffusion_ratio= max(0, self._diffusion_ratio)
            self._diffusion_ratio= min(1/6, self._diffusion_ratio)
        
        shifts = [-1, 1]
        axes = [0,0,1,1,2,2] 
        # order: left, right, front
        # diffuse per six face_neighbors
        total_diffusions = create_zero_array(self._n)
        for i in range(6):
            # y: shift neighbor
            y = np.copy(self._array)
            y = np.roll(y, shifts[i % 2], axis = axes[i])
            if not reintroduce_on_the_other_end:
                e = self._n - 1
                # removing the values from the other end after rolling
                if i == 0:
                    y[:][:][e] = 0
                elif i == 1:
                    y[:][:][0] = 0
                elif 2 <= i <= 3:
                    m = y.transpose((1,0,2))
                    if i == 2:
                        m[:][:][e] = 0
                    elif i == 3:
                        m[:][:][0] = 0
                    y = m.transpose((1,0,2))
                elif 4 <= i <= 5:
                    m = y.transpose((2,0,1))
                    if i == 4:
                        m[:][:][e] = 0
                    elif i == 5:
                        m[:][:][0] = 0
                    y = m.transpose((1,2,0))
            # calculate diffusion value
            if self._diffusion_random_factor == 0:
                diff_ratio = self.diffusion_ratio
            else:
                diff_ratio = self.diffusion_ratio * (1 - create_random_array(self._n) * self.diffusion_random_factor)
            # summ up the diffusions per faces
            total_diffusions += diff_ratio * (self._array - y) / 2
        self._array -= total_diffusions
        return self._array
    
    def emmission(self):
        pass

    def decay(self):
        if self._decay_random_factor == 0:
            self.array -= self.array *  self._decay_ratio
        else:
            randomized_decay = self._decay_ratio * (1 - create_random_array(self._n) * self._decay_random_factor)
            self.array += self.array * self._decay_ratio * randomized_decay

    def decay_linear(self):
        s,e = self.voxel_crop_range
        self._array = self.crop_array(self._array - self.decay_linear_value, s,e)

    def calculate_color_array(self):
        r,g,b = self.rgb
        s, e = self.voxel_crop_range
        colors = np.copy(self.array)
        colors = (1 - self.crop_array(colors, s,e))
        # colors = self.crop_array(colors, s,e)
        reds = np.reshape(colors * (r), [self._n, self._n, self._n, 1])
        greens = np.reshape(colors * (g), [self._n, self._n, self._n, 1])
        blues = np.reshape(colors * (b), [self._n, self._n, self._n, 1])
        self._color_array = np.concatenate((reds, greens, blues), axis = -1)
        return self._color_array

    def iterate(self, diffusion_limit_by_Hirsh=False, reintroduce_on_the_other_end=False ):
        self.iter_count += 1
        # decay
        self.decay()
        # diffuse
        self.diffuse(diffusion_limit_by_Hirsh, reintroduce_on_the_other_end)
        # emmite
        self.emmission()
        

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



def convert_to_compas_pointcloud(voxel_array, order = 'xyz'):
    pass

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