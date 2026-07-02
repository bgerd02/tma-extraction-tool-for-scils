'''
Contains functions that communicate with SCiLS API
'''
import os
import json
import pandas as pd 
import numpy as np
from scilslab import LocalSession
import state


def get_feature_lists(path_to_slx_file):        # called once page 1 'Next' button is clicked
    '''Gets list of all feature lists with their id, name, and number of features in each list

        Creates:  feature_lists_df (DataFrame): one row per feature list with columns id, name, number of features        
    '''
    feature_lists = state.dataset.feature_table.get_feature_lists()
    feature_lists_df = pd.DataFrame(feature_lists)
    feature_lists_df = feature_lists_df.drop(columns=['has_mz_features', 'has_mobility_intervals', 'has_ccs_features', 'has_external_features'])
    print(feature_lists_df.head())
    return feature_lists_df


def get_spots_in_region(regionId):      
    '''Gets coordinates of spots/pixels from a given region. Used in get_intensities_of_region

        Returns: region_spots_df (DataFrame): one row per spot with columns spotId, x, y  
    '''
    region_spots = state.dataset.get_region_spots(regionId)
    region_spots_df = pd.DataFrame(region_spots).drop(columns=['raster', 'z'])
    print(region_spots.keys())
    return region_spots_df


def check_for_attribute(attribute):         # called in page 2
    # get region list with passed attribute

    num_pixels = 0
    # for each region in region list, region_spots_df = get_spots_in_region, then num_pixels += len(region_spots_df)
    print('heyyy')
    #return num_regions, num_pixels


def get_intensities_of_region(regionId, features, normalization):
    '''Gets spot coordinates and intenities of features in passed list of passed region. 
        Combines coordinate and intensity arrays based on spotId.

        Returns: coords_and_intensities (DataFrame): one row per spot with columns spotId, x, y, peak1, peak2, peak3... for a passed region        
    '''
    for mz_low, mz_high in features:
        intensities = state.dataset.get_ion_intensities(     # intensities is an object with two arrays: spot_ids and values (prealigned)
            min_mz=mz_low, max_mz=mz_high, 
            region_id = regionId,
            mode='area',
            normalization_id=normalization
        )
        intensities_df = pd.DataFrame({
            'spotId':intensities.spot_ids,
            f'{mz_low:.3f}_{mz_high:.3f}':intensities.values
        }) 
        all_spots = get_spots_in_region(regionId)      # Get spot ids and coords 
        coords_and_intensities = pd.merge(all_spots, intensities_df, how='outer', on='spotId')
        return coords_and_intensities


def extract_spots(          # called in page 3
        normalization=None, 
        feature_list=None, 
        attribute=None, 
        export_type=None,
        output_directory=None
    ):
    # if attribute:
        #region_list = get_regions_with_attribute(attribute)
    # else: 
        # region_list = get_all_regions()
    # intensities = []
    # for region in region_list: 
        #region_spots_df = get_intensities_of_region(region, feature_list, normalization)
        # add spots to intensities
    
    # if export_type == '.txt': 
        # convert intensities to .txt file
        # save .txt file to output_directory

    # if export_type == '.csv':
        # convert intensities to .csv file
        # save .csv file to output_directory

    print('heyyyyy')