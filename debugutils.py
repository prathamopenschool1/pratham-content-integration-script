import csv
import json
import os
import requests
from urllib.parse import urlparse

from le_utils.constants.languages import getlang_by_name

from sushichef import load_pradigi_structure, find_games_for_lang, get_all_game_names
from sushichef import should_skip_file
from sushichef import PRADIGI_WEBSITE_LANGUAGES, PRADIGI_STRINGS



# STRUCTURE DIAGNOSE AND DEBUG TOOLS
################################################################################

def getlang_by_language_en(language_en):
    """
    Convert language names used on PraDigi websites to le_utils language object.
    """
    if language_en == 'Odiya' or language_en == 'Odisa':
        language_en = 'Oriya'
    elif language_en == 'Bangali':
        language_en = 'Bengali'
    elif language_en == 'Telagu':
        language_en = 'Telugu'
    lang_obj = getlang_by_name(language_en)
    return lang_obj



def compute_games_by_language_csv(game_names):
    """
    Checks which game names exist in all the PraDigi languages
    Matching is performed based on language code suffix, e.g. _MR for Marathi.
    Returns list of all languages matched.
    """
    languages_matches = []
    not_found_names = []
    languages_en = [PRADIGI_STRINGS[lang]['language_en'] for lang in PRADIGI_LANGUAGES]
    fieldnames = ['Name on gamerepo'] + languages_en
    
    with open('games_by_language_matrix.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for game_name in game_names:
            row_dict = {}
            row_dict['Name on gamerepo'] = game_name
            found = False
            for lang in PRADIGI_LANGUAGES:
                games = find_games_for_lang(game_name, lang)
                if games:
                    value = ' and '.join([game['title'] for game in games])
                    languages_matches.extend(games)
                    found = True
                else:
                    value = "N/A"
                languages_en = PRADIGI_STRINGS[lang]['language_en']
                row_dict[languages_en] = value
            writer.writerow(row_dict)
            if not found:
                not_found_names.append(game_name)
    print('not_found_names', not_found_names)
    return languages_matches


def flatten_tree(tree):
    if len(tree['children'])==0:
        return [tree]
    else:
        result = []
        for child in tree['children']:
            flat_child = flatten_tree(child)
            result.extend(flat_child)
        return result

def flatten_website_games(data):
    result = []
    for lang, gamelist in data.items():
        result.extend(gamelist)
    return result


def find_undocumented_games():
    # all repo games
    data = json.load(open('chefdata/vader/trees/pradigi_games_all_langs.json','r'))
    gamelist = flatten_tree(data)
    all_set = set([game['url'] for game in gamelist])
    
    # the ones in TEST_GAMENAMES
    game_names = get_all_game_names()
    found_gamelist = compute_games_by_language_csv(game_names)
    found_set = set([game['url'] for game in found_gamelist])
    
    diff_set = all_set.difference(found_set)
    diff_gamelist = []
    for diff_url in diff_set:
        for game in gamelist:
            if game['url'] == diff_url and not should_skip_file(diff_url):
                diff_gamelist.append(game)
    
    sorted_by_lang = sorted(diff_gamelist, key=lambda s:s['title'])
    for game in sorted_by_lang:
        print(game['title']+'\t'+game['language_en']+'\t'+game['url'])
    
    # Print just names
    # diff_game_names = set()
    # for game in sorted_by_lang:
    #     title = game['title']
    #     if '_' in title:
    #         root = '_'.join(title.split('_')[0:-1])
    #     else:
    #         root = title
    #     diff_game_names.add(root)
    # for name in sorted(diff_game_names):
    #     print(name)


def new_find_undocumented_games():
    """
    Same as find_undocumented_games but works with game names instead of URLs.
    """
    # all repo games
    data = json.load(open('chefdata/vader/trees/pradigi_games_all_langs.json','r'))
    gamelist = flatten_tree(data)
    all_set = set([game['title'] for game in gamelist])
    # print('len(all_set)', len(all_set))

    # all website games
    wdata = json.load(open('chefdata/vader/trees/website_games_all_langs.json','r'))
    wgamelist = flatten_website_games(wdata)
    for wgame in wgamelist:
        wgame['title'] = wgame['title_en']
        gamelist.append(wgame)
    all_set = all_set.union([game['title_en'] for game in wgamelist])
    # print('len(all_set)', len(all_set))


    # the ones in TEST_GAMENAMES
    game_names = get_all_game_names()
    # print('game_names = ', game_names)

    
    found_gamelist = compute_games_by_language_csv(game_names)
    found_set = set()
    for game in found_gamelist:
        if 'title_en' in game:
            found_set.add(game['title_en'])
        else:
            found_set.add(game['title'])
    print('len(found_set)', len(found_set))

    diff_set = all_set.difference(found_set)
    diff_gamelist = []
    for diff_name in diff_set:
        for game in gamelist:
            if game['title'] == diff_name:
                diff_gamelist.append(game)
    
    sorted_by_lang = sorted(diff_gamelist, key=lambda s:s['title'])
    for game in sorted_by_lang:
        print(game['title']+'\t'+game['url'])
        # print(game['title']+'\t'+game['language_en']+'\t'+game['url'])



# WEBSITE DIAGNOSE AND DEBUG TOOLS
################################################################################


def find_large_video_files(tree, parent):
    if tree['kind'] == 'PrathamVideoResource':
        url_p = urlparse(tree['url'])
        filename = os.path.basename(url_p.path)
        if 'content-length' in tree:
            size_bytes = tree['content-length']
            size_mb = int(size_bytes)/1024/1024
            if size_mb > 100:
                print('Large video file' + '\t' + filename + '\t'+ tree['url'] + \
                    '\t' + parent['url'] + '\t' + 'File size is %.2fMB, so not good for web' % size_mb)
        else:
            print('404 video file' + '\t' + filename + '\t' + tree['url'] + '\t' + parent['url'])




def find_missing_zip_resources(tree, parent):
    if tree['kind'] == 'PrathamZipResource':
        url = tree['url']
        url_p = urlparse(url)
        filename = os.path.basename(url_p.path)
        
        resp = requests.head(url)
        if resp.status_code == 404:
            print('404 zip file' + '\t' + filename + '\t' + url + '\t' + parent['url'])



def walk_tree(tree, parent={'url':None}, el_fn=lambda x: x):
    el_fn(tree,parent)
    for child in tree['children']:
        walk_tree(child, parent=tree, el_fn=el_fn)


def find_problem_resources_files():
    for lang in ['hi', 'mr']:
        wrt_filename = 'chefdata/vader/trees/pradigi_{}_web_resource_tree.json'.format(lang)
        with open(wrt_filename) as jsonfile:
            web_resource_tree = json.load(jsonfile)
            # walk_tree(web_resource_tree, el_fn=find_large_video_files)
            walk_tree(web_resource_tree, el_fn=find_missing_zip_resources)

