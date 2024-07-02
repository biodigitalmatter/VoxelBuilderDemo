import numpy as np

# parameters backup::
# # grounds_offset
# offset_pheromone.decay_linear_value = 1/6
# offset_pheromone.decay_ratio = 0
# offset_pheromone.diffusion_ratio = 1/3
# grounds_emission_value = 2

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

def set_value_at_index(layer, index = [0,0,0], value = 1):
    # print('set value at index', index)
    i,j,k = index
    layer.array[i][j][k] = value
    return layer

def get_layer_value_at_index(layer, index = [0,0,0]):
    # print('get value at index', index)
    index2 = np.mod(index, layer.voxel_size)
    i,j,k = index2
    v = layer.array[i][j][k]
    return v

def get_nb_cell_directions_w_corners():
    # horizontal
    f = direction_dict_np['front']
    b = direction_dict_np['back']
    l = direction_dict_np['left']
    r = direction_dict_np['right']
    u = direction_dict_np['up']
    d = direction_dict_np['down']
    # first_story in level:
    story_1 = [f, f + l, f + r, l, r, b, b + l, b + r]
    story_0 = [i + d for i in story_1]
    story_2 = [i + u for i in story_1]
    nbs_w_corners = story_1 + story_0 + story_2 + [u] + [d] + [np.asarray([0,0,0])]
    return nbs_w_corners

def get_nb_cell_directions_w_edges():
    # horizontal
    face_nbs = list(direction_dict_np.values())
    nbs_w_edges = face_nbs + [np.asarray([0,0,0])]
    return nbs_w_edges

def conditional_fill(array, n, condition = '<', value = 0.5, override_self = False):
    """returns new voxel_array with 0,1 values based on condition"""
    if condition == '<':
        mask_inv = array < value
    elif condition == '>':
        mask_inv = array > value
    elif condition == '<=':
        mask_inv = array <= value
    elif condition == '>=':
        mask_inv = array >=  value
    a = create_zero_array(n)
    a[mask_inv] = 0
    if override_self:
        array = a
    return a

def make_solid_box_z(voxel_size, z_max):
    n = voxel_size
    test_i = np.indices((n,n,n))
    z = test_i[2,:,:,:] <= z_max
    d = np.zeros((n,n,n))
    d[z] = 1
    return d

def make_solid_box_xxz(voxel_size, x_min, x_max, z_max):
    n = voxel_size
    test_i = np.indices((n,n,n))
    x1 = test_i[0,:,:,:] >= x_min
    x2 = test_i[0,:,:,:] <= x_max
    z = test_i[2,:,:,:] <= z_max
    d = np.zeros((n,n,n))
    d[x2 & x1 & z] = 1
    return d

def make_solid_box_xxyyzz(voxel_size, x_min, x_max, y_min, y_max, z_min, z_max):
    """boolean box including limits"""
    n = voxel_size
    test_i = np.indices((n,n,n))
    x1 = test_i[0,:,:,:] >= x_min
    x2 = test_i[0,:,:,:] <= x_max
    y1 = test_i[1,:,:,:] >= y_min
    y2 = test_i[1,:,:,:] <= y_max
    z1 = test_i[2,:,:,:] >= z_min
    z2 = test_i[2,:,:,:] <= z_max
    d = np.zeros((n,n,n))
    d[x2 & x1 & y1 & y2 & z1 & z2] = 1
    return d

global direction_dict_np, direction_keys

direction_dict_np = {
    'up' : np.asarray([0,0,1]),
    'left' : np.asarray([-1,0,0]),
    'down' : np.asarray([0,0,-1]),
    'right' : np.asarray([1,0,0]),
    'front' : np.asarray([0,-1,0]),
    'back' : np.asarray([0,1,0])
}
direction_keys = list(direction_dict_np.keys())
# print(direction_keys)[5]


class Layer:
    def __init__(self, name = '', voxel_size = 20, rgb = [1,1,1], 
                diffusion_ratio = 0.12, diffusion_random_factor = 0,
                decay_ratio = 0, decay_random_factor = 0, decay_linear_value = 0, emission_factor = 0.1,
                gradient_resolution = 0, color_array = None):
        
        # self._array =  # value array
        self._color_array = None # colored array 4D
        self._axis_order = 'zyx'
        self._name = name
        self._n = voxel_size
        self._array = np.zeros(self._n ** 3).reshape([self._n, self._n, self._n])
        self._rgb = rgb
        self._diffusion_ratio = diffusion_ratio
        self._diffusion_random_factor = diffusion_random_factor
        self._decay_ratio = decay_ratio
        self._decay_random_factor = decay_random_factor
        self._decay_linear_value = decay_linear_value
        self._gradient_resolution = gradient_resolution
        self._voxel_crop_range = [0,1] # too much
        self._iter_count = 0
        self._color_array = color_array
        self._emission_factor = emission_factor
        self._emmision_array = None
    
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
        self.calculate_color_array(False)
        return self._color_array

    @property
    def color_array_inverse(self):
        self.calculate_color_array(True)
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
    
    @property
    def emission_factor(self):
        return self._emission_factor

    @property
    def voxel_crop_range(self):
        return self._voxel_crop_range

    # Property setters

    @emission_factor.setter
    def emission_factor(self, value):
        self._emission_factor = value
    
    @iter_count.setter
    def iter_count(self, value):
        if not isinstance(value, float):
            raise ValueError("value must be a float")
        self._iter_count = value

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
    def decay_linear_value(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Decay linear ratio must be a number")
        self._decay_linear_value = abs(value * -1)

    @decay_random_factor.setter
    def decay_random_factor(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Decay random factor must be a number")
        self._decay_random_factor = value

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

    def set_layer_value_at_index(self, index = [0,0,0], value = 1):
        index2 = np.mod(index, self.voxel_size)
        i,j,k = index2
        self.array[i][j][k] = value
        return self.array

    def get_value_at_index(self, index = [0,0,0]):
        i,j,k = index
        v = self.array[i][j][k]
        return v

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
    

    def emission(self, external_emission_array = None, external_emission_factor = 1, proportional = True):
        """updates array values based on self array values
        by an emission factor ( multiply / linear )"""

        if proportional: #proportional
            self.array += self.array * self.emission_factor
        else: # absolut
            self.array = np.where(self.array != 0, self.array + self.emission_factor, self.array)
    

    def emission_intake(self, external_emission_array, factor, proportional = True):
        """updates array values based on a given array
        and an emission factor ( multiply / linear )"""

        if proportional: #proportional
            # self.array += external_emission_array * self.emission_factor
            self.array = np.where(external_emission_array != 0, self.array + external_emission_array * factor, self.array)
        else: # absolut
            self.array = np.where(external_emission_array != 0, self.array + factor, self.array)
    
    def block_layers(self, other_layers = []):
        """acts as a solid obstacle, stopping diffusion of other layers
        input list of layers"""
        for i in range(len(other_layers)):
            layer = other_layers[i]
            layer.array = np.where(self.array == 1, 0 * layer.array, 1 * layer.array)
        pass

    def decay(self):
        if self._decay_random_factor == 0:
            self.array -= self.array *  self._decay_ratio
        else:
            randomized_decay = self._decay_ratio * (1 - create_random_array(self._n) * self._decay_random_factor)
            randomized_decay = abs(randomized_decay) * -1
            self.array += self.array * randomized_decay

    def decay_linear(self):
        s,e = self.voxel_crop_range
        self._array = self.crop_array(self._array - self.decay_linear_value, s,e)

    def calculate_color_array(self, inverse = True):
        r,g,b = self.rgb
        colors = np.copy(self.array)
        if inverse:
            colors = 1 - colors

        reds = np.reshape(colors * (r), [self._n, self._n, self._n, 1])
        greens = np.reshape(colors * (g), [self._n, self._n, self._n, 1])
        blues = np.reshape(colors * (b), [self._n, self._n, self._n, 1])
        colors = np.concatenate((reds, greens, blues), axis = 3)
        self._color_array = colors
        return self._color_array

    def iterate(self, diffusion_limit_by_Hirsh=False, reintroduce_on_the_other_end=False ):
        self.iter_count += 1
        # emission update
        self.emmission_in()
        # decay
        self.decay()
        # diffuse
        self.diffuse(diffusion_limit_by_Hirsh, reintroduce_on_the_other_end)
        #emission_out
        self.emmission_out_update()


    


class Agent:
    def __init__(self, 
        pose = [0,0,0], 
        compass_array = direction_dict_np,
        ground_layer = None, 
        limited_to_ground = 'offset_pheromon',
        space_layer = None, 
        construction_layer = None,
        track_layer = None,
        leave_trace = False):

        self.pose = np.asarray(pose)  # [i,j,k]
        self.compass_array = compass_array
        self.compass_keys = list(compass_array.keys())
        self.limited_to_ground = limited_to_ground
        self.leave_trace = leave_trace
        self.space_layer = space_layer
        self.construction_layer = construction_layer
        self.track_layer = track_layer
        self.ground_layer = ground_layer
        if ground_layer != None:
            self.voxel_size = ground_layer.voxel_size
        if self.limited_to_ground == 'cube_corner_nb_check':
            self.cube_array = get_nb_cell_directions_w_corners()
        elif self.limited_to_ground == 'cube_edge_nb_check':
            self.cube_array = get_nb_cell_directions_w_edges()

    def move(self, i, n = 0):
        """move to a neighbor voxel based on the compas dictonary key index"""
        v = self.compass_array[self.compass_keys[i]]
        self.pose += v
        if n != 0:
            self.pose = np.mod(self.pose, np.asarray([n,n,n]))

    def move_key(self, key, n=0):
        """move to a neighbor voxel based on the compas dictonary key"""
        v = self.compass_array[key]
        self.pose += v
        if n != 0:
            self.pose = np.mod(self.pose, np.asarray([n,n,n]))
    def random_move(self):
        i = np.random.randint(0,5)
        all_dir = self.compass_array.keys()
        v = all_dir[i]
        self.pose += v
    
    def update_space(self):
        self.space_layer.set_layer_value_at_index(self.pose, 1)
    
    def random_pheromones(self):
        return np.random.random(6)
    
    def direction_preference_pheromones(self, up = True):
        if up:
            direction_preference = np.asarray([1,0.5,0.1,0.5,0.5,0.5])
        else:
            direction_preference = np.ones(6)
        return direction_preference
    
    def get_nb_cell_indicies(self, pose):
        """returns the list of nb cell indexes"""
        nb_cell_index_list = []
        for key in self.compass_array.keys():
            d = self.compass_array[key]
            nb_cell_index_list.append( d + pose)
        return nb_cell_index_list

    def get_nb_cell_values(self, layer, pose = None):
        # nb_value_dict = {}
        value_list = []
        for key in self.compass_array.keys():
            d = self.compass_array[key]
            nb_cell_index = d + pose
            # dont check index in boundary
            v = get_layer_value_at_index(layer, nb_cell_index)
            value_list.append(v)
        return np.asarray(value_list)


    def get_cube_nbs_value_sums(self, layer, nb_pose):
        value_sum = 0
        nb_cube_array = self.cube_array + nb_pose
        for p in nb_cube_array:
            v = get_layer_value_at_index(layer, p)
            value_sum += v
        return value_sum
    
    def get_cube_nbs_value_sums_with_mask(self, layer, nb_pose):
        nb_cube_array = self.cube_array + nb_pose
        v = np.where(layer.array.indicies() == nb_cube_array, 1, 0)
        value_sum = np.sum(v)
        return value_sum


    def check_ground(self, ground_layer):
        """        return ground directions as bools
        checks nbs of the nb cells
        if value > 0: return True"""
        # get nb cell indicies
        nb_cells = self.get_nb_cell_indicies(self.pose)
        cells_to_check = list(nb_cells)

        check_failed = []
        # iterate through nb cells
        for nb_pose in cells_to_check:
            # print('nb_pose;', nb_pose)
            # check nbs of nb cell
            nbs_values = self.get_nb_cell_values(ground_layer, nb_pose)
            # check nb cell
            nb_value = get_layer_value_at_index(ground_layer, nb_pose)
            if np.sum(nbs_values) > 0 and nb_value == 0:
                check_failed.append(False)
            else: check_failed.append(True)
        exclude_pheromones = np.asarray(check_failed)
        return exclude_pheromones
    
    def check_ground_in_cubes(self, ground_layer):
        """return ground directions as bools
        checks cube nbs of the nb cells
        if value > 0: return True"""
        # get nb cell indicies
        nb_cells = self.get_nb_cell_indicies(self.pose)
        cells_to_check = list(nb_cells)
        check_failed = []
        # iterate through nb cells
        for nb_pose in cells_to_check:
            nbs_values = self.get_cube_nbs_value_sums(ground_layer, nb_pose)
            nb_value = get_layer_value_at_index(ground_layer, nb_pose)
            if np.sum(nbs_values) > 0 and nb_value == 0:
                check_failed.append(False)
            else: check_failed.append(True)
        exclude_pheromones = np.asarray(check_failed)
        return exclude_pheromones
    
    def follow_pheromones(self, six_pheromones, offset_limit = None):
        # check ground condition
        if self.limited_to_ground == 'nb_check':
            exclude_pheromones = self.check_ground(self.ground_layer)
            six_pheromones[exclude_pheromones] = -1
        
        elif self.limited_to_ground == 'offset_ph':
            nbs_values = self.get_nb_cell_values(offset_limit, self.pose)
            exclude_pheromones = np.logical_not(nbs_values != 0)
            six_pheromones[exclude_pheromones] = -1
        
        elif self.limited_to_ground == 'cube_corner_nb_check' or self.limited_to_ground == 'cube_edge_nb_check':
            exclude_pheromones = self.check_ground_in_cubes(self.ground_layer)
            six_pheromones[exclude_pheromones] = -1
        
        if np.sum(six_pheromones) == -6:
            return -1

        # select best pheromon
        choice = np.argmax(six_pheromones)
        # update location in space layer
        if self.leave_trace:
            self.track_layer.set_layer_value_at_index(self.pose, 1)
        self.space_layer.set_layer_value_at_index(self.pose, 0)
        self.move(choice, n = self.space_layer.voxel_size)
        self.space_layer.set_layer_value_at_index(self.pose, 1)
        return choice
    
    def construct(self, pheromon_layer, limit1, limit2):
        """agent builds on construction_layer, if pheromon value in cell hits limit
        return bool"""
        v = get_layer_value_at_index(pheromon_layer, self.pose)
        # print(v)
        if limit1 <= v <= limit2:
            try:
                set_value_at_index(self.construction_layer, self.pose, 1)
            except:
                print(self.pose)
            return True
        else: return False 

    def check_offset(self, offset_layer):
        """        return ground directions as bools"""
        # get nb cell indicies
        nbs_values = self.get_nb_cell_values(offset_layer, self.pose)
        exclude_pheromones = np.logical_not(nbs_values == 0)
        return exclude_pheromones





# Other helper functions

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
builder = Agent(pose=(5, 5, 5), movement_limitations={'max_steps': 10}, pathpheromon_strength=0.9)
explorer = Agent(pose=(2, 2, 2), movement_limitations={'max_steps': 15}, pathpheromon_strength=0.6)

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