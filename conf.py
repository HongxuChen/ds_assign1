#!/usr/bin/env python
import os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'facebook'))
combined_fname = 'facebook_combined.gz'
gzip_file = os.path.join(data_dir, combined_fname)

ext_list = ['circles', 'edges', 'egofeat', 'feat', 'featnames']