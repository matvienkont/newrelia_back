#!/usr/bin/python3.8
import os
import json
from colab_ssh import launch_ssh
from colab_ssh import get_tunnel_config

def ReadConectionInfoJSON():
    with open('/content/connection/GPU_server_connection_info', 'r') as f:
        j = json.loads(f.read())
        print(j)
    return j

def SendCommand(command):
    j = ReadConectionInfoJSON()
    os.system('sshpass -p 777 ssh -o StrictHostKeyChecking=no -p ' + j["port"] + ' root@' + j["domain"] + ' ' + command)


def RunProcessing(parametersJSON, result_resolution = 512, max_iterations = 700, print_iteration = 50, device = 'gpu'):
    command  = 'ipython /content/drive/MyDrive/Style-Transfer-Network/neural_style.ipy --'
    command += ' --content_img_dir /content/drive/MyDrive/Style-Transfer-Network/image_input '
    command += ' --style_imgs_dir /content/drive/MyDrive/Style-Transfer-Network/styles '
    command += ' --model_weights /content/drive/MyDrive/Style-Transfer-Network/imagenet-vgg-verydeep-19.mat '
    command += ' --img_output_dir /content/drive/MyDrive/Style-Transfer-Network/image_output/'
    command += ' --max_size ' + str(result_resolution)
    command += ' --max_iterations ' + str(max_iterations)
    command += ' --print_iteration ' + str(print_iteration)
    
    command += ' --content_img '        + parametersJSON["content_img"]
    command += ' --style_imgs '         + parametersJSON["style_imgs"]
    command += ' --style_imgs_weights ' + str(parametersJSON["style_imgs_weights"])
    command += ' --tv_weight '          + str(parametersJSON["tv_weight"])
    command += ' --temporal_weight '    + str(parametersJSON["temporal_weight"])
    
    if(parametersJSON["original_colors"] == "True"):
     command += ' --original_colors '
 
    command += ' --pooling_type '       + parametersJSON["pooling_type"]
    command += ' --device /' + device + ':0'
    
    SendCommand(command)


def SendFile(sourceFilePath, destinationFilePath):
    j = ReadConectionInfoJSON()
    os.system('sshpass -p 777 scp -o StrictHostKeyChecking=no -P ' + j["port"] + ' ' + sourceFilePath + ' root@' + j["domain"] + ':' + destinationFilePath)


def SendContentImage(sourceFilePath):
    SendFile(sourceFilePath,'/content/drive/MyDrive/Style-Transfer-Network/image_input/')


def SendStyleImage(sourceFilePath):
    SendFile(sourceFilePath,'/content/drive/MyDrive/Style-Transfer-Network/styles/')











