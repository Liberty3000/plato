
global_features = [
#### Constant Feature Groups ###################################################
    # terrain
    'land',
    'air',
    'sea',
#### Entity Feature Groups #####################################################
    # entity types
    'drone',
    'infantry',
    'vehicle',
    # static landmarks
    'area_of_interest', # goals that remain constant in time and space
    # dynamic landmarks
    'temporal_area_of_interest',
    'spatial_area_of_interest',
    'spatiotemporal_area_of_interest',
    'routes',
#### Asset Feature Groups ######################################################
    # weapons
    'weapon_range',
    'weapon_radius',
    'weapon_power',
    # sensors
    # ...
    # cargo
    # ...
#### Capability Feature Groups #################################################
    'durability',
    'visibility',
    'mobility',
#### Information Gain Maps #####################################################
    # detections
    'infantry_detections', # infantry detections
    'vehicle_detections', # vehicle detections
    'drone_detections', # drone detections
    'unknown_detections', # unknown/unidentitied detections
    # mortality maps
    'negative_casualties', # kills
    'positive_casualties', # causalties
    # execution maps
    'negative_engagements', # where they've fired at us
    'positive_engagements', # where we've fired at them
]

n_global_feats = len(global_features)
