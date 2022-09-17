# The following script is used to demonstrate real-time system activity that displays the current parking situation at the Holon Institute of Technology.
# In the absence of suitable sensors for monitoring the presence of cars in the parking lot, there are various methods in this script whose role is to
# randomly change and update changes in parking lot occupancy.
# If the institute chooses to implement a plan to install suitable sensors in the parking lots, it will be possible to cancel these methods and use the real time obtained from the sensors.
# The script reads and edits the file obtained from the parking mapping done in advance in the QGIS software,
# uses the file as a database and updates it on the fly so that every time you click to refresh the page you will receive an updated snapshot of the parking lots in the institute.

import os
import random
import shutil
import json
import time
from pathlib import Path
from random import randrange


# read Json values into new Python Object. return Python Object
def readJson(jsonPath):
    with open(jsonPath) as f:
        j = json.load(f)
        # print(j)
        # print()
        return j


# update Python Object Values to new random values
def update_parking_values():
    features = Json1['features']
    for feature in features:
        rand_num = randrange(10)
        rand_list.append(rand_num)
        # print('rand_num = ', rand_num)
        p = feature['properties']
        # print(p)
        new_emptySpace = int(feature['properties']['emptySpace']) - rand_num
        new_takenSpace = int(feature['properties']['takenSpace']) + rand_num
        p['emptySpace'] = new_emptySpace
        p['takenSpace'] = new_takenSpace
        # print(p)
        # print()
    return Json1


def fill_parking_space(parking_space):
    if parking_space == '1':  # space already taken - not filling space
        return 1
    return 2   # space is not taken - filling space


def update_parking_spaces():
    features = Json2['features']
    random.shuffle(features)
    park1_change_count = rand_list[0]
    park2_change_count = rand_list[1]
    park3_change_count = rand_list[3]
    park4_change_count = rand_list[2]
    for feature in features:
        if (int(feature['properties']['ParkId']) == 1) and (park1_change_count > 0):
            filled = fill_parking_space(feature['properties']['taken'])
            if filled == 2:
                feature['properties']['taken'] = '1'
                park1_change_count -= 1
        elif (int(feature['properties']['ParkId']) == 2) and (park2_change_count > 0):
            filled = fill_parking_space(int(feature['properties']['taken']))
            if filled == 2:
                feature['properties']['taken'] = '1'
                park2_change_count -= 1
        elif (int(feature['properties']['ParkId']) == 3) and (park3_change_count > 0):
            filled = fill_parking_space(int(feature['properties']['taken']))
            if filled == 2:
                feature['properties']['taken'] = '1'
                park3_change_count -= 1
        elif (int(feature['properties']['ParkId']) == 4) and (park4_change_count > 0):
            filled = fill_parking_space(int(feature['properties']['taken']))
            if filled == 2:
                feature['properties']['taken'] = '1'
                park4_change_count -= 1
    return Json2


# create new Json file from the Python object with the new random values
def createNewJson(myjson):
    if myjson == Json1:
        with open('new_parking_state.json', 'w') as f:
            json.dump(myjson, f, indent=2)
        return (myjson)
    with open('new_park_spaces_6.json', 'w') as f:
        json.dump(myjson, f, indent=2)
    return (myjson)


# append js style prefix to Json file
def line_prepender(result, line):
    with open(result, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


# change json extension to js extension: js extension marks that the content of the file should be script following javascript syntax, and also human-readable.
def change_extension(path):
    if path == '/Users/admin/PycharmProjects/updateMap/new_parking_state.json':
        p = Path('/Users/admin/PycharmProjects/updateMap/new_parking_state.json')
        p.rename(p.with_suffix('.js'))
    else:
        p = Path('/Users/admin/PycharmProjects/updateMap/new_park_spaces_6.json')
        p.rename(p.with_suffix('.js'))


# rename file and put it in place
def rename_file(old_name, new_name):
    os.rename(old_name,new_name)


if __name__ == '__main__':
    park_5js_path = '/Users/admin/PycharmProjects/updateMap/Park_5.json'
    parkspaces_6js_path = '/Users/admin/PycharmProjects/updateMap/ParkSpaces_6.json'
    data_directory = '/Users/admin/Desktop/Omer/Study/Year/ D/Summer/ Semester/GIS/latest/HitParking0.2/data/'
    rounds = 0
    while 1:
        rand_list = []
        rounds += 1
        print('# round ', rounds)
        Json1 = readJson(park_5js_path)
        Json2 = readJson(parkspaces_6js_path)
        print()
        print('- finished reading json files')
        new_parking_values = update_parking_values()
        print('- park_5 values changed')
        result1 = createNewJson(Json1)
        print('- new park_5 file created as new_parking_state.json')
        line_prepender('/Users/admin/PycharmProjects/updateMap/new_parking_state.json', 'var json_Park_5 = ')
        print('- appended "var" prefix to new_parking_state.json')
        change_extension('/Users/admin/PycharmProjects/updateMap/new_parking_state.json')
        print('changed extension of new_parking_state.json to new_parking_state.js')

        print()
        print('rand_list = ', rand_list)
        print()

        update_parking_spaces()
        print('- park_spaces_6 values changed')
        result2 = createNewJson(Json2)
        print('NEW GENERATED JSON2 (new_parking_state.json) CONTENTS: ')
        print('- new_park_spaces_6.json file created')
        line_prepender('/Users/admin/PycharmProjects/updateMap/new_park_spaces_6.json', 'var json_ParkSpaces_6 = ')
        print('- appended "var" prefix to new_park_spaces_6.json')
        change_extension('/Users/admin/PycharmProjects/updateMap/new_park_spaces_6.json')
        print('changed extension of new_park_spaces_6.json to new_park_spaces_6.js')
        rename_file('/Users/admin/PycharmProjects/updateMap/new_park_spaces_6.js', '/Users/admin/Desktop/Omer/Study/Year D/Summer Semester/GIS/latest/HitParking0.2/data/ParkSpaces_6.js')
        rename_file('/Users/admin/PycharmProjects/updateMap/new_parking_state.js', '/Users/admin/Desktop/Omer/Study/Year D/Summer Semester/GIS/latest/HitParking0.2/data/Park_5.js')

        print()
        print()
        print('round ', rounds, ' finished. ')
        time.sleep(4)
        print('starting round ', rounds+1)
        time.sleep(1)