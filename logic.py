'''
Contains functions that communicate with SCiLS API
'''
import os
import json
import pandas as pd 
import numpy as np
from scilslab import LocalSession
import state


def get_feature_lists():        # called once page 1 'Next' button is clicked
    '''Gets list of all feature lists with their id, name, and number of features in each list

        Creates:  feature_lists_df (DataFrame): one row per feature list with columns id, name, number of features        
    '''
    feature_lists = state.dataset.feature_table.get_feature_lists()
    feature_lists_df = pd.DataFrame(feature_lists)
    feature_lists_df = feature_lists_df.drop(columns=['has_mz_features', 'has_mobility_intervals', 'has_ccs_features', 'has_external_features'])
    print(feature_lists_df.head())
    return feature_lists_df

def get_normalization_types():
    '''
        Returns: normalization_types_df (DataFrame): one row per normalization type with columns uniqueId and description (also indexed maybe)
    '''
    normalization_types = state.dataset.get_normalizations() 
    normalization_types_df = pd.DataFrame(
        list(normalization_types.items()), columns=['uniqueId', 'description']
    )
    return normalization_types_df


def get_spots_in_region(regionId):      
    '''Gets coordinates of spots/pixels from a given region. Used in get_intensities_of_region

        Returns: region_spots_df (DataFrame): one row per spot with columns spotId, x, y  
    '''
    region_spots = state.dataset.get_region_spots(regionId)
    region_spots_df = pd.DataFrame(region_spots).drop(columns=['raster', 'z'])
    print(region_spots.keys())
    return region_spots_df


def check_for_attribute():
    '''Get list of regions whose attribute dict contains a value matching state.attribute'''
    region_tree = state.dataset.get_region_tree()
    region_list = []
    for region in region_tree.get_all_regions():
        if len(region.subregions) == 0:
            name = region.name[region.name.rfind('/')+1:]
            region_list.append((region.id, name, region.attributes))
    region_list_df = pd.DataFrame(region_list, columns=('id', 'name', 'attribute'))

    search_term = state.attribute.lower()

    def matches(attr):
        if not isinstance(attr, dict):
            return False
        return any(search_term in str(v).lower() for v in attr.values())

    filtered_df = region_list_df[region_list_df['attribute'].apply(matches)]
    num_regions = len(filtered_df)
    return num_regions


def get_intensities_of_region(regionId, features):
    '''Gets spot coordinates and intenities of features in passed list of passed region. 
        Combines coordinate and intensity arrays based on spotId.

        Returns: coords_and_intensities (DataFrame): one row per spot with columns spotId, x, y, peak1, peak2, peak3... for a passed region        
    '''
    coords_and_intensities = get_spots_in_region(regionId)
    for _, feature in features.iterrows(): 
        mz_low, mz_high = feature['mz_low'], feature['mz_high']
        intensities = state.dataset.get_ion_intensities(     # intensities is an object with two arrays: spot_ids and values (prealigned)
            min_mz=mz_low, max_mz=mz_high, 
            region_id = regionId,
            mode='area',
            normalization_id=state.normalization
        )
        intensities_df = pd.DataFrame({
            'spot_id':intensities.spot_ids,
            f'{mz_low:.3f}_{mz_high:.3f}':intensities.values
        }) 
        coords_and_intensities = pd.merge(coords_and_intensities, intensities_df, how='outer', on='spot_id')
    return coords_and_intensities
    

def get_root_region():
    region_list = []
    region_tree = state.dataset.get_region_tree()
    for region in region_tree.get_all_regions():
        clean_name = region.name.rstrip('/')
        parent_path = clean_name.rsplit('/', 1)[0] if '/' in clean_name else clean_name

        if parent_path == 'Regions':
            region_list.append((region.id, region.name, region.attributes))
    
    region_list.sort(key=lambda x: x[0])
    parent_region_df = pd.DataFrame(region_list, columns=('id', 'name', 'attribute'))
    return parent_region_df

def get_regions_with_attribute():
    region_tree = state.dataset.get_region_tree()
    region_list = []
    for region in region_tree.get_all_regions():
        if len(region.subregions) == 0:
            name = region.name[region.name.rfind('/')+1:]
            region_list.append((region.id, name, region.attributes))
    region_list_df = pd.DataFrame(region_list, columns=('id', 'name', 'attribute'))

    search_term = state.attribute.lower()

    def matches(attr):
        if not isinstance(attr, dict):
            return False
        return any(search_term in str(v).lower() for v in attr.values())

    filtered_df = region_list_df[region_list_df['attribute'].apply(matches)]
    return filtered_df

def extract_spots():
    '''Extracts feature intensities for all spots in one or more regions and exports them to file.

        Regions are either those matching state.attribute (if set) or all top-level 
        regions under 'Regions' (if not). For each region, merges spot coordinates 
        with intensities for every feature in state.feature_list, then saves the 
        combined result as .txt or .csv to state.output_path.

        Reads from state: dataset, feature_list, attribute, normalization, 
        export_type, output_path
    '''
    ## Get features in feature list
    features =  state.dataset.feature_table.get_features(feature_list_name=state.feature_list)
    print(type(features))       #debug
    print(features)     #debug
    
    ## Get list of regions based on whether attribute was passed or not
    print('Getting region(s)...')
    if state.attribute:
        region_list = get_regions_with_attribute()
    else: 
        region_list = get_root_region()
    
    ## Extract intensities for each spot
    intensities = []
    for index, region in region_list.iterrows(): 
        region_spots = get_intensities_of_region(region['id'], features)
        region_spots['regionId'] = region['id']
        region_spots['regionName'] = region['name']
        region_spots['attributes'] = json.dumps(region['attribute'])
        intensities.append(region_spots)

    intensities = pd.concat(intensities, ignore_index=True)

    ## Export intensities 
    print(f'Saving as {state.export_type}...')
    if state.export_type == '.txt': 
        intensities.to_csv(os.path.join(state.output_path, f'intensities_{state.attribute}.txt'), sep='\t', index=False)
    
    else:
        intensities.to_csv(os.path.join(state.output_path, f'intensities_{state.attribute}.csv'), index=False)

    print('Extraction complete!')
