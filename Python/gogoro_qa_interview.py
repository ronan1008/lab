import sys
import requests
import pandas as pd
import matplotlib.pyplot as plt


def _url_json_link(raw_url):
    ''' input url then format url to json request,like:  https://swapi.co/api/?format=json'''
    return raw_url if raw_url.find('format=json') > 0 else raw_url+"?format=json"


def request_url_to_dict(url):
    ''' imput url then make json format to python dictionary'''
    re_back = requests.get(_url_json_link(url))
    if re_back.status_code != 200:
        print("This request is not available")
        sys.exit()
    else:
        content_dict = re_back.json()
        return content_dict


def sorted_dict_bykeys(dict_type):
    '''input dictionary,then return dic sort by key '''
    keys = list(dict_type.keys())
    keys.sort()
    return {key: dict_type[key] for key in keys}


def find_url_with_num(film_url_list, category, num):
    '''input films_url_list and number to find out match url'''
    url_pattern = "https://swapi.co/api/{}/{}/".format(category, num)
    for film in film_url_list:
        if film['url'] == url_pattern:
            return film['url']


def link_crawler(link):
    '''input a link then recursive the link if there is still has a link in "next" columns'''
    yield link
    vehicles_dict = request_url_to_dict(link)
    if vehicles_dict['next'] is not None:
        yield from link_crawler(vehicles_dict['next'])


def main():
    '''main execute function'''
    root_url = 'https://swapi.co/api/'
    # 1
    print("1. How many different species appears in film-6?\n")
    root_dict = request_url_to_dict(root_url)

    films_url = root_dict['films']
    films_dict = request_url_to_dict(films_url)

    films_list = films_dict['results']
    film_num_url = find_url_with_num(films_list, 'films', 6)
    film_num_dict = request_url_to_dict(film_num_url)

    species_num = len(film_num_dict['species'])
    print("There are {} species in film-6".format(species_num))
    # 2
    print("\n2. List all the film names and sort the name by episode_id : \n")
    films_dict = {film_info['episode_id']: film_info['title']
                  for film_info in films_list}
    films_dict_sort = sorted_dict_bykeys(films_dict)
    for film_id, film_title in films_dict_sort.items():
        print(film_id, film_title)
    # 3
    print("\n3. Please find out all vehicles which max_atmosphering_speed is over 1000 : \n")
    vehicles_url = root_dict['vehicles']
    links_list = link_crawler(vehicles_url)
    over_sp_vehi = {}

    for link in links_list:

        link_dict = request_url_to_dict(link)
        vehicles_lists = link_dict['results']

        for vehicle in vehicles_lists:

            vehi_name, vehi_max_atmo_sp = vehicle['name'], vehicle['max_atmosphering_speed']

            if vehi_max_atmo_sp == 'unknown':
                continue
            else:
                vehi_max_atmo_sp = int(vehi_max_atmo_sp)
            if vehi_max_atmo_sp > 1000:
                over_sp_vehi[vehi_name] = vehi_max_atmo_sp

    vehis = {'name': [vehi_na for vehi_na in over_sp_vehi.keys()],
             'speed': [vehi_sp for vehi_sp in over_sp_vehi.values()]}
    # pandas: dataframe plot
    vehis_speed_df = pd.DataFrame(
        vehis, columns=['speed'], index=vehis['name'])
    print(vehis_speed_df)
    ax = vehis_speed_df.plot(title='Vehicle of Star Wars speed over 1000', kind='barh',
                             fontsize=10, figsize=(15, 5))
    for i in ax.patches:
        ax.text(i.get_width()+100, i.get_y()+0.15,
                i.get_width(), fontsize=10, color='red')
    plt.ylabel('Vehicles')
    plt.xlabel("Speed")
    plt.show()


if __name__ == '__main__':
    main()
