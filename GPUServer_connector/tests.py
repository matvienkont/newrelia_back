#!/usr/bin/python3.8
import GPUserverAPI
import json

s = '{"content_img":"tubingen.jpg","style_imgs" : "shipwreck.jpg", "style_imgs_weights" : "1", "tv_weight" : "5", "temporal_weight":"200", "original_colors":"False", "pooling_type" : "max"}'

j = json.loads(s)

GPUserverAPI.RunProcessing(j, result_resolution = 60, max_iterations = 10, print_iteration = 5, device = 'cpu')
