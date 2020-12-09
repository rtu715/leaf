from __future__ import division
import json
import math
import numpy as np
import os
import sys

from PIL import Image

TARGET_NAME = 'Smiling'
parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

MAX_CELEBS = 100 

def get_metadata():
        f_identities = open(os.path.join(
                parent_path, 'data', 'raw', 'identity_CelebA.txt'), 'r')
        identities = f_identities.read().split('\n')

        f_attributes = open(os.path.join(
                parent_path, 'data', 'raw', 'list_attr_celeba.txt'), 'r')
        attributes = f_attributes.read().split('\n')

        return identities, attributes


def get_celebrities_and_images(identities):
        all_celebs = {}

        for line in identities:
                info = line.split()
                if len(info) < 2:
                        continue
                image, celeb = info[0], info[1]
                if celeb not in all_celebs:
                        all_celebs[celeb] = []
                all_celebs[celeb].append(image)

        good_celebs = {c: all_celebs[c] for c in all_celebs if len(all_celebs[c]) >= 5}
        return good_celebs


def _get_celebrities_by_image(identities):
        good_images = {}
        for c in identities:
                images = identities[c]
                for img in images:
                        good_images[img] = c
        return good_images


def get_celebrities_and_target(celebrities, attributes, attribute_name=TARGET_NAME):
        col_names = attributes[1]
        col_idx = col_names.split().index(attribute_name)

        celeb_attributes = {}
        good_images = _get_celebrities_by_image(celebrities)

        for line in attributes[2:]:
                info = line.split()
                if len(info) == 0:
                        continue

                image = info[0]
                if image not in good_images:
                        continue
                
                celeb = good_images[image]
                att = (int(info[1:][col_idx]) + 1) / 2
                
                if celeb not in celeb_attributes:
                        celeb_attributes[celeb] = []

                celeb_attributes[celeb].append(att)

        return celeb_attributes


def write_json(json_data):
        file_name = 'all_data.json'
        dir_path = os.path.join(parent_path, 'data', 'all_data')

        if not os.path.exists(dir_path):
                os.mkdir(dir_path)

        file_path = os.path.join(dir_path, file_name)

        print('writing {}'.format(file_name))
        with open(file_path, 'w') as outfile:
                json.dump(json_data, outfile)



def process_x(raw_x_batch):
    x_batch = [load_image(i) for i in raw_x_batch]
    #x_batch = np.array(x_batch)
    return x_batch

def process_y(raw_y_batch):
    return raw_y_batch

def load_image(img_name, IMAGES_DIR):
    IMAGE_SIZE = 28,28
    img = Image.open(os.path.join(IMAGES_DIR, img_name))
    img = img.convert('RGB')

    img.thumbnail(IMAGE_SIZE, Image.ANTIALIAS)
    img = np.array(img) / 255.0
    img = img.tolist()
    
    return img

def build_json(celebrities, targets):
        users = []
        num_samples = []
        user_data = {}



        celeb_keys = [c for c in celebrities]
        num_json = int(math.ceil(len(celeb_keys) / MAX_CELEBS))
        #num_samples = [len(celebrities[c]) for c in celeb_keys]

        IMAGES_DIR = os.path.join(parent_path, 'data', 'raw', 'img_align_celeba')
        celeb_count = 0
        json_index = 0
        for c in celeb_keys:
                users.append(c)
                num_samples.append(len(celebrities[c]))
                user_data[c] = {'x':[], 'y':[]}

                for img in celebrities[c]:
                    user_data[c]['x'].append(load_image(img, IMAGES_DIR))

                user_data[c]['y'] = targets[c]
                celeb_count += 1
                if celeb_count == MAX_CELEBS:
                        all_data = {}
                        all_data['users'] = users
                        all_data['num_samples'] = num_samples
                        all_data['user_data'] = user_data

                        file_name = 'all_data%d.json' % json_index
                        file_path = os.path.join(parent_path, 'data', 'all_data', file_name)

                        print('writing %s out of %s files' % (file_name, str(num_json)))

                        with open(file_path, 'w') as outfile:
                                json.dump(all_data, outfile)

                        celeb_count = 0 
                        json_index += 1

                        users[:] = []
                        num_samples[:] = []
                        user_data.clear()

        return 







def main():
        identities, attributes = get_metadata()
        celebrities = get_celebrities_and_images(identities)
        targets = get_celebrities_and_target(celebrities, attributes)

        json_data = build_json(celebrities, targets)
        #write_json(json_data)




if __name__ == '__main__':
        main()


