#!/usr/bin/env python
import os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'facebook'))
combined_fname = 'facebook_combined.gz'

ext_list = ['circles', 'edges', 'egofeat', 'feat', 'featnames']
