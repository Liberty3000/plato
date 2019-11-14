import gym, random, os, time, tqdm
import numpy as np, matplotlib.pyplot as mp
from plato.actions import attack, patrol
from plato.features import global_features
from plato.entity.util import plot_entities, randomize_entities
from plato.objective.util import plot_objectives, encode_objectives
from plato.router import pathfinder
from plato.terrain import perlin
from plato.util import coverage, quantize_area

class Environment(gym.Env):
    def __init__(self, config=None, shape=(64,64), objectives=[], controlled=[], time_limit=2**14):
        self.config, self.shape = config, shape
        self.state_space = (len(global_features), *shape)
        self.pathfinder = pathfinder()
        self.global_reward, self.local_rewards = 0, {}
        self.objectives = objectives
        self.controlled = controlled
        self.time_limit = time_limit

    def initialize_terrain(self):
        self.air = np.zeros(self.shape)
        self.sea = np.zeros(self.shape)
        self.land= perlin(self.shape[0], self.shape[1], seed=0)

    def reset(self):
        self.state, self.reward, self.timer = None,0,0

        cfg = self.config['whites']
        init_params = cfg['params'].values()
        init_area = quantize_area(cfg['init'], self.shape)
        self.whites = randomize_entities(*init_params, init_area, 'whites')

        cfg = self.config['blacks']
        init_params = cfg['params'].values()
        init_area = quantize_area(cfg['init'], self.shape)
        self.blacks = randomize_entities(*init_params, init_area, 'blacks')

        self.white_detections, self.black_detections = [],[]
        self.white_casualties, self.black_casualties = [],[]

        self.initialize_terrain()
        return self.observation(self.whites, self.blacks)

    def terrain(self):
        return np.asarray([self.sea, self.land, self.air])

    def observation(self, positive, negative=None):
        minimap = np.zeros((len(global_features),*self.shape))

        minimap[global_features.index('land'),:]= self.land
        minimap[global_features.index('air'),:] = self.air
        minimap[global_features.index('sea'),:] = self.sea

        for ent in positive.values():
            x,y = ent.xy[0],ent.xy[1]

            minimap[global_features.index(ent.entity_type),x,y] += 1

            if ent.weapons:
                weapon_model = ent.weapons[0]

                minimap[global_features.index('weapon_power'), x,y]  += weapon_model['weapon_power']

                for xy in coverage(ent.xy, weapon_model['weapon_range'], self.shape):
                    for (i,j) in coverage(xy, weapon_model['weapon_radius'], self.shape):
                        minimap[global_features.index('weapon_radius'),i,j] += weapon_model['weapon_radius']

                for (x,y) in coverage(ent.xy, weapon_model['weapon_range'], self.shape):
                    minimap[global_features.index('weapon_range'),x,y] += weapon_model['weapon_range']

            if ent.sensors:
                sensor_model = ent.sensors[0]
                minimap[global_features.index('sensor_coverage'),x,y]+= sensor_model['sensor_coverage']
                for (x,y) in coverage(ent.xy, sensor_model['sensor_range'], self.shape):
                    minimap[global_features.index('sensor_range'),x,y] += weapon_model['sensor_range']

            minimap[global_features.index('durability'),x,y] += ent.properties['durability']

            for (x,y) in coverage(ent.xy, ent.properties['mobility'], self.shape):
                minimap[global_features.index('mobility'),x,y] += (1 - ent.properties['mobility'])

            for (x,y) in coverage(ent.xy, ent.properties['visibility'], self.shape):
                minimap[global_features.index('visibility'),x,y] += ent.properties['visibility']


        if any([ent.id in self.blacks.keys() for ent in positive.values()]):
            dets,kills,casts = self.white_detections,self.white_casualties,self.black_casualties
        else:
            dets,kills,casts = self.black_detections,self.black_casualties,self.white_casualties
            minimap = encode_objectives(self.objectives, minimap, self.white_detections, self.shape)

        for ent in dets:
            x,y = ent.xy
            minimap[global_features.index(ent.entity_type + '_detections'),x,y] += 1
        for ent in kills:
            x,y = ent.xy
            minimap[global_features.index('positive_casualties'),x,y] += 1
        for ent in casts:
            x,y = ent.xy
            minimap[global_features.index('negative_casualties'),x,y] += 1

        return minimap

    def observe_detections(self):
        self.white_detections, self.black_detections = [],[]
        for white in self.whites.values():
            for black in self.blacks.values():
                operational = white.operational and black.operational
                white_cells = coverage(white.xy, white.properties['visibility'], self.shape)
                black_cells = coverage(black.xy, black.properties['visibility'], self.shape)
                if black.xy in white_cells and operational:
                    self.white_detections += [black]
                if white.xy in black_cells and operational:
                    self.white_detections += [white]
        self.white_detections = set(self.white_detections)
        self.black_detections = set(self.black_detections)

    def calculate_damage(self, damage_map, targets):
        casualities = []
        for target in targets.values():
            x,y = target.xy
            target.properties['durability'] -= damage_map[x,y]
            if target.properties['durability'] < 0:
                target.operational = False
                casualities.append(target)
        return set(casualities)

    def shape_reward(self):
        reward = 0

        # reward kills
        for _ in self.black_casualties: reward += 0.2
        # penalize casualties
        for _ in self.white_casualties: reward -= 0.2
        # reward survival
        if all([not ent.operational for ent in self.blacks.values()]): reward += 1
        # penalize extinction
        if all([not ent.operational for ent in self.whites.values()]): reward -= 1
        # reward objectives
        reward += sum([obj.reward for obj in self.objectives])

        return reward

    def termination_condition(self):
        terminal,status = False,'neutral'

        args = dict(entities=self.whites, enemies=self.blacks, timer=self.timer)

        terminal = any([obj(**args) for obj in self.objectives])
        if terminal: status = 'success'

        if self.timer >= self.time_limit: terminal,status = True,'neutral'

        if all([not ent.operational for ent in self.whites.values()]):
            terminal,status = True,'failure'
        if all([not ent.operational for ent in self.blacks.values()]):
            terminal,status = True,'success'

        return terminal,status

    def step(self, white_actions={}, black_actions={}, verbose=False):
        self.timer += 1

        metadata = {'positive_observables':  None, # what we see
                    'negative_observables':  None, # what they see
                    'fully_observable':      None} # everything

        # white's actions
        positive_damage_map = np.zeros((*self.shape,))
        for id_,action in white_actions.items():
            entity = self.whites[id_]
            if entity.operational:
                if action in entity.patrol_actions:
                    entity.xy = patrol(entity, action, self.terrain())
                if action in entity.attack_actions:
                    positive_damage_map = attack(entity, action, positive_damage_map)
        self.black_casualties = self.calculate_damage(positive_damage_map, self.blacks)

        # blacks's actions
        negative_damage_map = np.zeros((*self.shape,))
        for id_,action in black_actions.items():
            entity = self.blacks[id_]
            if entity.operational:
                if action in entity.patrol_actions:
                    entity.xy = patrol(entity, action, self.terrain())
                if action in entity.attack_actions:
                    negative_damage_map = attack(entity, action, negative_damage_map)
        self.white_casualties = self.calculate_damage(negative_damage_map, self.whites)

        self.observe_detections()

        metadata['positive_observables'] = self.observation(self.whites, self.blacks)
        metadata['negative_observables'] = self.observation(self.blacks, self.whites)
        metadata[ 'positive_damage_map'] = positive_damage_map
        metadata[ 'negative_damage_map'] = negative_damage_map
        metadata[ 'positive_casualties'] = self.white_casualties
        metadata[ 'negative_casualties'] = self.black_casualties

        white_map = np.zeros((*self.shape,))
        for ent in self.whites.values():
            x,y = ent.xy[0],ent.xy[1]
            white_map[x,y] += 1
        metadata['white_map'] = white_map

        black_map = np.zeros((*self.shape,))
        for ent in self.blacks.values():
            x,y = ent.xy[0],ent.xy[1]
            black_map[x,y] += 1
        metadata['black_map'] = black_map

        self.global_reward = self.shape_reward()
        self.terminal, status = self.termination_condition()
        metadata['status'] = status
        return metadata['positive_observables'], self.global_reward, self.terminal, metadata

    def render(self, notebook=False, show=True, routes=False):
        fig,ax = mp.subplots(1,1,figsize=(10,10))

        canvas = np.zeros((*self.shape,3))
        ax.set_aspect('equal')

        controlled = [ent for ent in self.whites.values() if ent.controlled == True]

        canvas,ax,wpatches = plot_entities(self.whites, controlled, canvas, ax)
        canvas,ax,bpatches = plot_entities(self.blacks, [], canvas, ax)
        canvas,ax,opatches = plot_objectives(self.objectives, self.timer, canvas, ax)

        mp.title('PLATO Environment', size=16)
        ax.imshow(canvas.astype(np.uint8))
        mp.show(block=False)
        mp.pause(1e-9)
        fig.canvas.draw_idle()
        try: fig.canvas.flush_events()
        except NotImplementedError: pass

        for p in wpatches: p.remove()
        for p in bpatches: p.remove()
        for p in opatches: p.remove()
        return canvas
