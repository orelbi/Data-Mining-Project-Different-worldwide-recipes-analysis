
import numpy
from bs4 import BeautifulSoup
import requests
import re
from time import sleep
import json
import lxml

"""USA website - gets the link for the first page of chocolate cakes recipes. 
collects and prints recipes links and their sugar, eggs, butter, servings amounts lists. 
 and print the recipes links list, the sugar amounts, the servings num, the sugar avg and sugar amounts
 consider the servings"""



def ezer(soap,lst):
    for line in str(soap).split('"'):
        if 'https://www.allrecipes.com/recipe/' in line:
            try:
                if int(line.split('/')[4]):
                    lst.append(line)
            except:
                pass

from time import sleep as ss

def get_recipes_links(url_base, links_amount):
    """
    get links to recipes
    :param url_base: pattern of a "menu" page of recipes
    :param links_amount: amount of links to download
    :return: list of recipes links, in size of links_amount
    """

    links = set()
    i = 1
    lst=[]
    while len(lst) < links_amount:
        #print('length: ', len(links))
        cur_url = url_base + str(i)
        soup = BeautifulSoup(requests.get(cur_url).text, "html.parser")
        ezer(soup, lst)
        lst = list(set(lst))
        sleep(1)
        #print('ezer=', len(lst))
        #print(cur_url)
        # cur_links = [l['href'] for l in
        #          soup.findAll("a", {"class": "recipeCard__titleLink"})]
        # for link in cur_links:
        #     if 'https://www.allrecipes.com/recipe/' in link:
        #         print(link)
        # cur_links = {re.findall("https://www.allrecipes.com/recipe/\d+",
        #                         link)[0] for link in cur_links}
        # print(cur_links)
        # links = links.union(cur_links)
        i += 1
    #return list(links)[:links_amount]
    print(lst)
    print(len(lst))
    return lst[:links_amount]

urli = "https://www.allrecipes.com/recipes/835/desserts/cakes/chocolate-cake/?internalSource=hub%20nav&referringId=276&referringContentType=Recipe%20Hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202&page="


def get_html_page_from_link(link):
    """Gets a url link and return its web page """
    url_text = requests.get(link).text
    html_page = BeautifulSoup(url_text, 'lxml')
    return html_page


def get_ingredients_list_from_page(html_page):
    """Gets a web_page and returns the ingredients list from it"""
    ingredient_list = []
    ingredients = html_page.findAll('span', class_="ingredients-item-name")
    for ing in ingredients:
        new_ing = str(ing)
        ingredient_list.append(new_ing)
    return ingredient_list


def clean_ingredients(ingredient_list):
    """Gets ingredients list """
    new_ing_lst = []
    for i in ingredient_list:
        x = i.split("\n")
        y = x[1]
        new_ing_lst.append(y[48:])
    return new_ing_lst

# def add_links(new_links_list, more_links_by_hand):
#     for i in more_links_by_hand:
#         if i not in new_links_list:
#             new_links_list.append(i)
#     return new_links_list


def get_sugar(recipes_dict):
    """get dict of ingredients for each cake, returns a dict with url and a
    line of the sugar ing"""
    sugar_dict = {}
    ezer = 0
    print(len(recipes_dict))
    for cake in recipes_dict.items():
        print("new_cake", cake)
        ezer = 0
        for ing in cake[1]:
            print(ing)
            if "sugar" in ing and "confectioners' sugar" not in ing:
                #i ignored powdered sugar, coconut sugar, vanilla sugar > let them count in
                sugar_dict[cake[0]] = ing
                ezer = 1
        if ezer == 0:
            sugar_dict[cake[0]] = "0"
    return sugar_dict


def get_sugar_in_numbers(sugar_dict):
    """gets a dict with url and line of the sugar ing, returns the sugar amount
    """
    new_sugar_dict = {}
    ezer = 0
    sugar_list = []

    print("sugar_dict", sugar_dict)
    for cake in sugar_dict.items():
        print("cake", cake[1])
        if "cup" in cake[1]:
            sugar_splited = cake[1].split("cup")
            print("sugar_splited", sugar_splited)
            ezer = 1
        elif "tablespoon" in cake[1]:
            sugar_splited = cake[1].split("tablespoon")
            print("sugar_splited", sugar_splited)
            ezer = 2
        elif "ounces" in cake[1]:
            sugar_splited = cake[1].split("ounces")
            print("sugar_splited", sugar_splited)
            ezer = 3
        else:
            sugar_splited = ["0", "0"]
        like_num = sugar_splited[0]
        amount = engineering(like_num)
        if ezer == 2:
            amount = int(amount)*0.0625
        elif ezer == 3:
            amount = int(amount) * (1 / 8)
        new_sugar_dict[cake[0]] = amount
        sugar_list.append(amount)
    print("sugar list", sugar_list)
    return new_sugar_dict

num_dict = {"¾": 0.75, "¼": 0.25, "½": 0.5, "⅞": 0.875, "⅔": 0.666, "⅛": 0.125}
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def engineering(like_num):
    """makes Yifat a genius"""
    num = 0
    for char in like_num:
        if char in numbers:
            num += int(char)
        if char in num_dict:
            num += num_dict[char]
    return num


def get_amount_avg(new_sugar_dict):
    sum = 0
    count = 0
    for val in new_sugar_dict.values():
        sum += val
        count += 1
    mean = sum/count
    return mean


def amounts_in_lst(new_sugar_dict):
    """Gets dict with url and amounts of sugar in numbers, returns just the amounts in a list"""
    val_lst = []
    for i in new_sugar_dict.values():
        val_lst.append(float(i))
    return val_lst


def get_num_servings(html_page):
    """Gets a web_page and returns the num servings from it"""
    servings_list = []
    servings = html_page.findAll('span', class_="recipe-meta-item-body")
    for mana in servings:
        new_ing = str(mana)
        servings_list.append(new_ing)
    return servings_list


#####3
# def clean_servings_and_time(servings_list):
#     """"""
#     servings_and_time_definitions = []
#     for single in servings_list:
#         x = single.split("\n")
#         if "mins" in x[1]:
#             servings_and_time_definitions.append(x[1][42:])
#         else:
#             servings_and_time_definitions.append(x[1][40:])
#     return servings_and_time_definitions


def get_servings_num_as_str(html_page):
    """Gets a web_page and returns the num servings from it"""
    try:
        ser_text = html_page.find('div', class_="recipe-adjust-servings__size-quantity").text
        print("ser_text", ser_text)
        real_ser = ser_text[1:-1]
        real_ser_in_number = int(real_ser)
    except:
        real_ser_in_number = 12
    return real_ser_in_number


    #print("ser", ser)
    #servings = html_page.findAll('div', class_="recipe-meta-item-body")
    #print("servings", servings)
    #servings_place = html_page.findAll('div', class_="recipe-meta-item-header")
    #print("servings_place", servings_place)
    #x = servings[servings_place].split(":")
    #print(x)
    #place_num = 0
    #for i, val in enumerate(x):
     #   if "Servings" in val:
      #      print(val)
       #     place_num = i+1
        #else:
         #   print("there is a problem, hooo noooo")
    #for mana in servings:
     #   new_ing = str(mana)
      #  servings_list.append(new_ing)
    #servings_and_time_definitions = clean_servings_and_time(servings_list)
    #print(servings_and_time_definitions[place_num])

link = "https://www.allrecipes.com/recipe/22953/dark-chocolate-cake-ii/"


# def get_html_page_from_link(link):
#     """Gets a url link and return its web page """
#     url_text = requests.get(link).text
#     html_page = BeautifulSoup(url_text, 'lxml')
#     return html_page

#
# html_page = get_html_page_from_link(link)
# new_x = get_servings_and_time(html_page)
######

def get_avg(servings, sugar_amounts):
    new_amounts = []
    for i in range(len(servings)):
        if sugar_amounts[i] != 0:
            new_amounts.append(sugar_amounts[i]/servings[i])
        elif sugar_amounts == 0:
            new_amounts.append(0)
    av = numpy.average(new_amounts)

    print(new_amounts)
    print(av)
#
# def get_butter_num(new_ing_lst):
#     """Gets an ingredients list and returns eggs amount"""
#     butter_amount = 0
#     for i in new_ing_lst:
#         if "butter" in i:
#             print("<><>", i)
#             counter = 0
#             butter_a = ""
#             butter_b = 0
#             for letter in i:
#                 if letter in "1234567890":
#                     counter = 1
#                     butter_a += letter
#                 elif letter in num_dict.keys():
#                     counter = 1
#
#                     butter_b += engineering(letter)
#                     print("<<<", letter)
#
#                # else: # if counter == 1:
#                 #    break
#             if butter_a != "":
#                 butter_amount += float(butter_a) + butter_b
#             elif butter_a == "" and butter_b > 0:
#                 butter_amount += butter_b
#             else:
#                 butter_amount = 1
#         # if butter_amount == 0:
#         #     butter_amount = 1
#     print("New ing list: ", new_ing_lst)
#     print("butter: ", butter_amount)
#     return butter_amount


def get_butter_num(new_ing_lst):
    """Gets an ingredients list and returns eggs amount"""
    butter_amount = 0
    for i in new_ing_lst:
        if "butter" in i:
            print("<><>", i)
            counter = 0
            butter_a = ""
            butter_b = 0
            for letter in i:
                if letter in "1234567890":
                    counter = 1
                    butter_a += letter
                elif letter in num_dict.keys():
                    counter = 1

                    butter_b += engineering(letter)
                    print("<<<", letter)

               # else: # if counter == 1:
                #    break
            if butter_a != "":
                butter_amount += float(butter_a) + butter_b
            elif butter_a == "" and butter_b > 0:
                butter_amount += butter_b
            else:
                butter_amount = 1
            print("New ing list: ", new_ing_lst)
            print("butter: ", butter_amount)
            return butter_amount

        # if butter_amount == 0:
        #     butter_amount = 1
    print("New ing list: ", new_ing_lst)
    print("butter: ", butter_amount)
    return 0


def get_eggs_num(new_ing_lst):
    """Gets an ingredients list and returns eggs amount"""
    eggs_amount = 0
    for i in new_ing_lst:
        if "egg" in i:
            counter = 0
            egg_a = ""
            for letter in i:
                if letter in "1234567890":
                    counter = 1
                    egg_a += letter
                elif counter == 1:
                    break
            if egg_a != "":
                eggs_amount = int(egg_a)
            elif egg_a == "":
                eggs_amount = 1
    print("New ing list: ", new_ing_lst)
    print("eggs: ", eggs_amount)
    return eggs_amount


########### sugar


def get_sugar_1(ingredients):
    ezer = 0
    sugar_ings = []
    for ing in ingredients:
        print(ing)
        if "sugar" in ing and "confectioners' sugar" not in ing:
                #i ignored powdered sugar, coconut sugar, vanilla sugar > let them count in
            sugar_ings.append(ing)
            ezer = 1
    if ezer == 0:
        sugar_ings = ["0"]
    return sugar_ings


def get_sugar_in_numbers_1(sugar_ings):
    """gets a dict with url and line of the sugar ing, returns the sugar amount
    """
    ezer = 0
    sugar_list = []
    print("sugar_dict", sugar_ings)
    for ing in sugar_ings:
        if "cup" in ing:
            print("<<<cup in ing>>>")
            sugar_splited = ing.split("cup")
            print("sugar_splited", sugar_splited)
            ezer = 1
        elif "tablespoon" in ing:
            sugar_splited = ing.split("tablespoon")
            print("sugar_splited", sugar_splited)
            ezer = 2
        elif "ounces" in ing:
            sugar_splited = ing.split("ounces")
            print("sugar_splited", sugar_splited)
            ezer = 3
        else:
            sugar_splited = ["0", "0"]
        like_num = sugar_splited[0]
        amount = engineering(like_num)
        if ezer == 2:
            amount = int(amount)*0.0625
        elif ezer == 3:
            amount = int(amount) * (1 / 8)
        sugar_list.append(amount)
    print("sugar list", sugar_list)
    amount = 0
    for i in sugar_list:
        amount += i
    print(amount)
    return amount




def main_function():
    #new_links_list = get_recipes_links(urli,493)
    new_links_list = ['https://www.allrecipes.com/recipe/7664/thirty-minute-cocoa-cake-with-quick-cocoa-frosting/', 'https://www.allrecipes.com/recipe/151749/chocolate-truffle-pie/', 'https://www.allrecipes.com/recipe/7502/coco-cola-cake-ii/', 'https://www.allrecipes.com/recipe/257833/sugar-free-molten-chocolate-cakes/', 'https://www.allrecipes.com/recipe/256135/have-mercy-triple-chocolate-cake/', 'https://www.allrecipes.com/recipe/279600/dark-chocolate-bundt-cake/', 'https://www.allrecipes.com/recipe/16779/vegan-chocolate-cake/', 'https://www.allrecipes.com/recipe/19106/ultimate-mayonnaise-cake/', 'https://www.allrecipes.com/recipe/23422/black-chocolate-cake/', 'https://www.allrecipes.com/recipe/7516/best-chocolate-cake/', 'https://www.allrecipes.com/recipe/90310/donauwellen/', 'https://www.allrecipes.com/recipe/223065/dark-german-chocolate-cake/', 'https://www.allrecipes.com/recipe/7992/chocolate-mint-cake-squares/', 'https://www.allrecipes.com/recipe/215416/chocolate-swirl-zucchini-sheet-cake/', 'https://www.allrecipes.com/recipe/24997/hazels-chocolate-cake/', 'https://www.allrecipes.com/recipe/7564/sour-cream-mocha-cake/', 'https://www.allrecipes.com/recipe/278643/peanut-butter-chocolate-layer-cake/', 'https://www.allrecipes.com/recipe/8042/sleepy-cake/', 'https://www.allrecipes.com/recipe/24965/gateau-africaine/', 'https://www.allrecipes.com/recipe/233298/german-chocolate-cupcakes/', 'https://www.allrecipes.com/recipe/7439/swiss-chocolate-cake/', 'https://www.allrecipes.com/recipe/19007/chocolate-decadence/', 'https://www.allrecipes.com/recipe/8149/flourless-chocolate-cake-i/', 'https://www.allrecipes.com/recipe/15707/german-chocolate-chip-pound-cake/', 'https://www.allrecipes.com/recipe/246848/black-forest-cupcakes/', 'https://www.allrecipes.com/recipe/17217/mexican-chocolate-cake/', 'https://www.allrecipes.com/recipe/208084/glendoras-chocolate-fudge-pudding-cake/', 'https://www.allrecipes.com/recipe/256755/chocolate-guinness-cake/', 'https://www.allrecipes.com/recipe/279709/super-moist-chocolate-bundt-cake/', 'https://www.allrecipes.com/recipe/7374/fudge-cake/', 'https://www.allrecipes.com/recipe/268572/ghirardelli-individual-chocolate-lava-cakes/', 'https://www.allrecipes.com/recipe/22275/crazy-mixed-up-cake/', 'https://www.allrecipes.com/recipe/278975/chocolate-cake-from-scratch/', 'https://www.allrecipes.com/recipe/7947/mocha-decadence/', 'https://www.allrecipes.com/recipe/216903/moms-chocolate-pound-cake/', 'https://www.allrecipes.com/recipe/7259/grandmas-eggless-butterless-milkless-cake/', 'https://www.allrecipes.com/recipe/35822/paradise-of-chocolate/', 'https://www.allrecipes.com/recipe/8383/chocolate-decadence-cake-i/', 'https://www.allrecipes.com/recipe/8134/aunt-marys-chocolate-cake/', 'https://www.allrecipes.com/recipe/7931/secret-cake/', 'https://www.allrecipes.com/recipe/7918/white-chocolate-pound-cake/', 'https://www.allrecipes.com/recipe/8380/the-most-popular-cake-in-america-cake/', 'https://www.allrecipes.com/recipe/272783/red-velvet-strawberry-cake/', 'https://www.allrecipes.com/recipe/193139/rich-chocolate-cupcake/', 'https://www.allrecipes.com/recipe/7256/chocolate-chip-oatmeal-cake/', 'https://www.allrecipes.com/recipe/263461/vegan-and-gluten-free-chocolate-cake/', 'https://www.allrecipes.com/recipe/219065/willard-family-german-chocolate-cake/', 'https://www.allrecipes.com/recipe/7957/richest-ever-chocolate-pound-cake/', 'https://www.allrecipes.com/recipe/232461/perfect-mississippi-mud-cake/', 'https://www.allrecipes.com/recipe/25618/sherrys-chocolate-cake/', 'https://www.allrecipes.com/recipe/7416/chocolate-mayo-cake/', 'https://www.allrecipes.com/recipe/7497/sachertorte/', 'https://www.allrecipes.com/recipe/7295/chocolate-pound-cake-i/', 'https://www.allrecipes.com/recipe/21312/scrumptious-chocolate-cake/', 'https://www.allrecipes.com/recipe/7454/caramel-nougat-cake-iii/', 'https://www.allrecipes.com/recipe/8257/german-sweet-chocolate-cake-i/', 'https://www.allrecipes.com/recipe/238748/chocolate-raspberry-cupcakes/', 'https://www.allrecipes.com/recipe/56127/black-forest-angel-food-cake/', 'https://www.allrecipes.com/recipe/8312/chocolate-pudding-cake-ii/', 'https://www.allrecipes.com/recipe/245378/ghirardelli-chocolate-and-orange-mousse-cake/', 'https://www.allrecipes.com/recipe/7438/chocolate-peanut-butter-wacky-cake/', 'https://www.allrecipes.com/recipe/17697/quick-chocolate-chip-cake/', 'https://www.allrecipes.com/recipe/77782/warm-flourless-chocolate-cake-with-caramel-sauce/', 'https://www.allrecipes.com/recipe/7667/chocolate-mocha-cake-i/', 'https://www.allrecipes.com/recipe/7971/chocolate-macaroon-cake/', 'https://www.allrecipes.com/recipe/36171/chocolate-black-tea-cake/', 'https://www.allrecipes.com/recipe/17567/red-velvet-cake-v/', 'https://www.allrecipes.com/recipe/220447/chocolate-beer-cupcakes-with-whiskey-filling-and-irish-cream-icing/', 'https://www.allrecipes.com/recipe/278181/chocolate-swiss-roll/', 'https://www.allrecipes.com/recipe/275301/peppermint-tea-chocolate-cake/', 'https://www.allrecipes.com/recipe/8189/port-wine-chocolate-cake/', 'https://www.allrecipes.com/recipe/260623/chocolate-cake-in-an-air-fryer/', 'https://www.allrecipes.com/recipe/268208/homemade-chocolate-cake/', 'https://www.allrecipes.com/recipe/235835/devils-float/', 'https://www.allrecipes.com/recipe/261172/cookies-n-creme-cream-cheese-bundt-cake/', 'https://www.allrecipes.com/recipe/268910/nutella-cream-cheese-pound-cake/', 'https://www.allrecipes.com/recipe/8001/oooh-baby-chocolate-prune-cake/', 'https://www.allrecipes.com/recipe/8145/chocolate-cakes-with-liquid-centers/', 'https://www.allrecipes.com/recipe/49953/chocolate-banana-cake-roll/', 'https://www.allrecipes.com/recipe/60942/sweet-and-spicy-chocolate-cake/', 'https://www.allrecipes.com/recipe/220798/justins-frosted-chocolate-cone-cakes/', 'https://www.allrecipes.com/recipe/26005/chocolate-zucchini-cake-iv/', 'https://www.allrecipes.com/recipe/278160/chocolate-ganache-cupcakes/', 'https://www.allrecipes.com/recipe/7280/the-easiest-chocolate-cake/', 'https://www.allrecipes.com/recipe/22281/black-bottom-cupcakes-ii/', 'https://www.allrecipes.com/recipe/278925/chocolate-cream-filled-cupcakes-with-fudge-icing/', 'https://www.allrecipes.com/recipe/259188/chocolate-chile-zucchini-cake/', 'https://www.allrecipes.com/recipe/49947/chocolate-poke-cake/', 'https://www.allrecipes.com/recipe/8195/sinful-flourless-espresso-cake/', 'https://www.allrecipes.com/recipe/270408/keto-chocolate-cake/', 'https://www.allrecipes.com/recipe/7661/chocolate-icebox-cake/', 'https://www.allrecipes.com/recipe/26006/chocolatissimo/', 'https://www.allrecipes.com/recipe/7314/favorite-chocolate-cake/', 'https://www.allrecipes.com/recipe/25976/busy-day-syrup-cake/', 'https://www.allrecipes.com/recipe/17789/hot-water-chocolate-cake/', 'https://www.allrecipes.com/recipe/9295/red-velvet-cake/', 'https://www.allrecipes.com/recipe/8100/wacky-cake-v/', 'https://www.allrecipes.com/recipe/270711/keto-cocoa-mug-cake/', 'https://www.allrecipes.com/recipe/22990/maureens-mocha-cake/', 'https://www.allrecipes.com/recipe/8082/chocolate-spice-cake-with-potato/', 'https://www.allrecipes.com/recipe/7640/gob-cake/', 'https://www.allrecipes.com/recipe/260674/chocolate-cake-in-the-instant-pot/', 'https://www.allrecipes.com/recipe/25624/peanut-butter-and-chocolate-cake-ii/', 'https://www.allrecipes.com/recipe/18150/holiday-fudge-cake/', 'https://www.allrecipes.com/recipe/7723/chocolate-roll-i/', 'https://www.allrecipes.com/recipe/245748/ultimate-black-forest-cake/', 'https://www.allrecipes.com/recipe/26001/chocolate-sheet-cake-ii/', 'https://www.allrecipes.com/recipe/256615/whole-grain-chocolate-cake/', 'https://www.allrecipes.com/recipe/260282/basic-eggless-chocolate-cake/', 'https://www.allrecipes.com/recipe/262689/greek-yogurt-chocolate-cake/', 'https://www.allrecipes.com/recipe/8396/chocolate-oil-cake/', 'https://www.allrecipes.com/recipe/218460/little-french-fudge-cakes/', 'https://www.allrecipes.com/recipe/273154/mint-chocolate-chip-cake/', 'https://www.allrecipes.com/recipe/278638/spiced-chocolate-layer-cake/', 'https://www.allrecipes.com/recipe/60425/chocolate-macaroon-tunnel-cake/', 'https://www.allrecipes.com/recipe/8472/chocolate-bundt-cake/', 'https://www.allrecipes.com/recipe/18167/yum-yum-cake-ii/', 'https://www.allrecipes.com/recipe/264065/chocolate-olive-oil-cake/', 'https://www.allrecipes.com/recipe/279134/buttermilk-chocolate-cake/', 'https://www.allrecipes.com/recipe/273149/chocolate-cake-with-raspberry-filling/', 'https://www.allrecipes.com/recipe/279133/never-fail-buttermilk-chocolate-cake/', 'https://www.allrecipes.com/recipe/9359/classic-yule-log/', 'https://www.allrecipes.com/recipe/9292/mafioso-chocolate-cake/', 'https://www.allrecipes.com/recipe/7264/waldorf-astoria-red-cake/', 'https://www.allrecipes.com/recipe/246815/german-chocolate-cheesecake-swirl-cake/', 'https://www.allrecipes.com/recipe/277610/pumpkin-chocolate-layer-cake/', 'https://www.allrecipes.com/recipe/18175/wellesley-fudge-cake-ii/', 'https://www.allrecipes.com/recipe/277950/air-fryer-chocolate-molten-cakes/', 'https://www.allrecipes.com/recipe/260742/monster-mini-cupcakes/', 'https://www.allrecipes.com/recipe/15595/one-bowl-chocolate-cake-ii/', 'https://www.allrecipes.com/recipe/7249/sourdough-chocolate-cranberry-cake/', 'https://www.allrecipes.com/recipe/15705/chocolate-mousse-cake-iii/', 'https://www.allrecipes.com/recipe/7956/dark-chocolate-orange-cake/', 'https://www.allrecipes.com/recipe/23398/jennys-black-forest-cake/', 'https://www.allrecipes.com/recipe/25560/baked-fudge-cake/', 'https://www.allrecipes.com/recipe/270210/chocolate-oreo-cake/', 'https://www.allrecipes.com/recipe/7696/berthas-big-bourbon-bundt-cake/', 'https://www.allrecipes.com/recipe/278982/old-fashioned-chocolate-sheet-cake/', 'https://www.allrecipes.com/recipe/7955/chocolate-applesauce-cake-i/', 'https://www.allrecipes.com/recipe/263058/bunny-cake-with-round-cake-pans/', 'https://www.allrecipes.com/recipe/7917/chocolate-web-cake/', 'https://www.allrecipes.com/recipe/19037/dessert-crepes/', 'https://www.allrecipes.com/recipe/25603/mars-bar-cake/', 'https://www.allrecipes.com/recipe/8066/passover-chocolate-sponge-cake/', 'https://www.allrecipes.com/recipe/257979/so-easy-black-magic-cake/', 'https://www.allrecipes.com/recipe/8328/german-chocolate-upside-down-cake/', 'https://www.allrecipes.com/recipe/203307/zucchini-raspberry-cupcakes/', 'https://www.allrecipes.com/recipe/7349/devils-food-cake-i/', 'https://www.allrecipes.com/recipe/18061/egg-free-dairy-free-nut-free-cake/', 'https://www.allrecipes.com/recipe/7862/chocolate-angel-torte/', 'https://www.allrecipes.com/recipe/234807/chef-johns-red-velvet-cupcakes/', 'https://www.allrecipes.com/recipe/21164/annes-low-sugar-chocolate-cake/', 'https://www.allrecipes.com/recipe/202074/salad-dressing-chocolate-cake/', 'https://www.allrecipes.com/recipe/217160/chocolate-banana-layer-cake/', 'https://www.allrecipes.com/recipe/256815/chocolate-flaxseed-cake/', 'https://www.allrecipes.com/recipe/7940/floating-brownie/', 'https://www.allrecipes.com/recipe/231892/idahoan-coca-cola-cake/', 'https://www.allrecipes.com/recipe/7601/chocolate-mint-mayonnaise-cake/', 'https://www.allrecipes.com/recipe/17527/mississippi-mud-cake-iv/', 'https://www.allrecipes.com/recipe/232225/yost-chocolate-cake/', 'https://www.allrecipes.com/recipe/275660/secret-ingredient-dark-chocolate-cake/', 'https://www.allrecipes.com/recipe/8183/easy-eggless-chocolate-cake/', 'https://www.allrecipes.com/recipe/25994/chocolate-fudge-cupcakes/', 'https://www.allrecipes.com/recipe/162426/moist-potato-chocolate-cake/', 'https://www.allrecipes.com/recipe/8136/cherry-chocolate-cake/', 'https://www.allrecipes.com/recipe/18161/coco-cola-cake-iv/', 'https://www.allrecipes.com/recipe/278540/french-molten-chocolate-cake/', 'https://www.allrecipes.com/recipe/7647/double-chocolate-cake-ii/', 'https://www.allrecipes.com/recipe/234000/chocolate-cake-pops/', 'https://www.allrecipes.com/recipe/7762/chocolate-mocha-cake-ii/', 'https://www.allrecipes.com/recipe/220932/easy-peasy-easter-cake-egg-and-milk-free/', 'https://www.allrecipes.com/recipe/26027/elizabeths-extreme-chocolate-lovers-cake/', 'https://www.allrecipes.com/recipe/7265/krazy-kake/', 'https://www.allrecipes.com/recipe/8387/welfare-cake/', 'https://www.allrecipes.com/recipe/231895/idahoan-potato-chocolate-cake-pops/', 'https://www.allrecipes.com/recipe/218622/zucchini-chocolate-chip-cake/', 'https://www.allrecipes.com/recipe/8467/moist-german-chocolate-cake/', 'https://www.allrecipes.com/recipe/8364/zucchini-chocolate-rum-cake/', 'https://www.allrecipes.com/recipe/25989/chocolate-cream-cheese-cake/', 'https://www.allrecipes.com/recipe/8009/eggless-chocolate-cake-i/', 'https://www.allrecipes.com/recipe/8307/texas-sheet-cake-iv/', 'https://www.allrecipes.com/recipe/245741/high-altitude-buttermilk-devils-food-cake/', 'https://www.allrecipes.com/recipe/213997/chocolate-chocolate-cake/', 'https://www.allrecipes.com/recipe/7501/coco-cola-cake-i/', 'https://www.allrecipes.com/recipe/25583/george-washington-chocolate-cake/', 'https://www.allrecipes.com/recipe/259990/ghirardelli-chocolate-chip-mini-bundt-cakes/', 'https://www.allrecipes.com/recipe/8023/pour-cake/', 'https://www.allrecipes.com/recipe/17528/extreme-chocolate-cake/', 'https://www.allrecipes.com/recipe/17644/german-chocolate-cake-iii/', 'https://www.allrecipes.com/recipe/8097/chocolate-rapture-cake/', 'https://www.allrecipes.com/recipe/279161/gluten-free-texas-sheet-cake/', 'https://www.allrecipes.com/recipe/7455/chocolate-caramel-nut-cake-ii/', 'https://www.allrecipes.com/recipe/17678/chocolate-applesauce-cake-iii/', 'https://www.allrecipes.com/recipe/25641/tunnel-of-fudge-cake-iv/', 'https://www.allrecipes.com/recipe/26004/chocolate-walnut-cake/', 'https://www.allrecipes.com/recipe/256484/guinness-chocolate-cake-with-irish-cream-frosting/', 'https://www.allrecipes.com/recipe/19074/old-fashioned-fudge-cake/', 'https://www.allrecipes.com/recipe/8389/wacky-cake-viii/', 'https://www.allrecipes.com/recipe/7423/mayonnaise-cake-i/', 'https://www.allrecipes.com/recipe/8014/simple-n-delicious-chocolate-cake/', 'https://www.allrecipes.com/recipe/278157/chocolate-ganache-layer-cake/', 'https://www.allrecipes.com/recipe/7834/hot-fudge-pudding-cake-ii/', 'https://www.allrecipes.com/recipe/17829/chocolate-hazelnut-teacake/', 'https://www.allrecipes.com/recipe/17823/polish-style-chocolate-cake/', 'https://www.allrecipes.com/recipe/19118/german-chocolate-cake-frosting-ii/', 'https://www.allrecipes.com/recipe/270362/guinness-cupcakes-with-guinness-frosting/', 'https://www.allrecipes.com/recipe/25998/chocolate-mousse-cake-v/', 'https://www.allrecipes.com/recipe/7988/chocolate-chip-apple-cake/', 'https://www.allrecipes.com/recipe/15768/perfect-chocolate-cake/', 'https://www.allrecipes.com/recipe/275670/reduced-sugar-chocolate-bundt-cake-with-peppermint-glaze/', 'https://www.allrecipes.com/recipe/245740/vegan-devils-food-cake/', 'https://www.allrecipes.com/recipe/15782/chocolate-zucchini-cupcakes/', 'https://www.allrecipes.com/recipe/233917/linda-sues-chocolate-cake-vegan/', 'https://www.allrecipes.com/recipe/8003/muddy-chocolate-cheese-cake/', 'https://www.allrecipes.com/recipe/19717/coco-cola-cake/', 'https://www.allrecipes.com/recipe/218530/black-forest-cheesecake/', 'https://www.allrecipes.com/recipe/272476/flourless-chocolate-lava-cake/', 'https://www.allrecipes.com/recipe/235539/best-mug-cake-paleo/', 'https://www.allrecipes.com/recipe/217100/dianas-guinness-chocolate-cake-with-guinness-chocolate-icing/', 'https://www.allrecipes.com/recipe/72953/chocolate-lizzie-cake-with-caramel-filling/', 'https://www.allrecipes.com/recipe/7720/rum-and-raisin-cake/', 'https://www.allrecipes.com/recipe/278637/four-layer-mocha-cream-cake/', 'https://www.allrecipes.com/recipe/280222/chocolate-coconut-cake-pan-cake-with-peanut-butter-swirl/', 'https://www.allrecipes.com/recipe/7924/brownstone-front-chocolate-cake/', 'https://www.allrecipes.com/recipe/278927/fudgy-filled-cupcakes/', 'https://www.allrecipes.com/recipe/241039/healthy-chocolate-mug-cake/', 'https://www.allrecipes.com/recipe/52718/flourless-chocolate-cake-ii/', 'https://www.allrecipes.com/recipe/17405/german-chocolate-cake-ii/', 'https://www.allrecipes.com/recipe/7352/our-favorite-chocolate-cake/', 'https://www.allrecipes.com/recipe/7466/deep-chocolate-raspberry-cake/', 'https://www.allrecipes.com/recipe/271040/nutella-chocolate-cake/', 'https://www.allrecipes.com/recipe/245750/black-forest-cake-icing/', 'https://www.allrecipes.com/recipe/19084/potato-chocolate-cake/', 'https://www.allrecipes.com/recipe/247003/flourless-chocolate-espresso-cake/', 'https://www.allrecipes.com/recipe/213341/perfect-st-patricks-day-cake/', 'https://www.allrecipes.com/recipe/7735/german-chocolate-cake-i/', 'https://www.allrecipes.com/recipe/8463/beer-cake-ii/', 'https://www.allrecipes.com/recipe/7317/great-chocolate-cake/', 'https://www.allrecipes.com/recipe/8203/chocolate-italian-cream-cake/', 'https://www.allrecipes.com/recipe/261176/perfectly-chocolate-chocolate-cake/', 'https://www.allrecipes.com/recipe/24971/chocolate-muck-muck-cake/', 'https://www.allrecipes.com/recipe/261879/german-chocolate-cake-bites/', 'https://www.allrecipes.com/recipe/259994/ghirardelli-mini-bittersweet-chocolate-cakes/', 'https://www.allrecipes.com/recipe/259753/gluten-free-wacky-depression-era-chocolate-cake/', 'https://www.allrecipes.com/recipe/261679/little-chocolate-heart-cakes-with-pears/', 'https://www.allrecipes.com/recipe/17849/chocolate-cake-iii/', 'https://www.allrecipes.com/recipe/7833/homemade-chocolate-babka/', 'https://www.allrecipes.com/recipe/17378/very-easy-chocolate-cake/', 'https://www.allrecipes.com/recipe/277034/extra-dark-chocolate-cake-with-salted-caramel-sauce/', 'https://www.allrecipes.com/recipe/7929/hot-fudge-sundae-cake/', 'https://www.allrecipes.com/recipe/7821/chocolate-custard-cake/', 'https://www.allrecipes.com/recipe/240042/healthy-ish-chocolate-cake/', 'https://www.allrecipes.com/recipe/8426/special-chocolate-cake-ii/', 'https://www.allrecipes.com/recipe/8081/german-chocolate-sauerkraut-cake/', 'https://www.allrecipes.com/recipe/220285/hot-fudge-pudding-cake/', 'https://www.allrecipes.com/recipe/8390/tunnel-of-fudge-cake-ii/', 'https://www.allrecipes.com/recipe/279324/better-than-moms-german-chocolate-cake/', 'https://www.allrecipes.com/recipe/9285/chocolate-plum-pudding-cake/', 'https://www.allrecipes.com/recipe/17592/rich-chocolate-cake-ii/', 'https://www.allrecipes.com/recipe/149550/garbanzo-bean-chocolate-cake-gluten-free/', 'https://www.allrecipes.com/recipe/233314/mexican-chocolatesalted-caramel-cake-in-a-mug/', 'https://www.allrecipes.com/recipe/276078/homemade-red-velvet-cake-with-cream-cheese-frosting/', 'https://www.allrecipes.com/recipe/140772/easy-microwave-chocolate-cake/', 'https://www.allrecipes.com/recipe/25987/chocolate-cherry-cake-iv/', 'https://www.allrecipes.com/recipe/17998/christmas-chocolate-town-cake/', 'https://www.allrecipes.com/recipe/231356/brownie-cupcakes/', 'https://www.allrecipes.com/recipe/25566/aunt-joyces-chocolate-cake/', 'https://www.allrecipes.com/recipe/7261/texas-sheet-cake-i/', 'https://www.allrecipes.com/recipe/25630/rocky-road-cake/', 'https://www.allrecipes.com/recipe/25634/southern-style-chocolate-pound-cake/', 'https://www.allrecipes.com/recipe/76935/molten-chocolate-cakes-with-sugar-coated-raspberries/', 'https://www.allrecipes.com/recipe/8246/chocolate-cake-in-a-jar-i/', 'https://www.allrecipes.com/recipe/17995/dark-chocolate-cream-cheese-cake/', 'https://www.allrecipes.com/recipe/26011/claras-white-german-chocolate-cake/', 'https://www.allrecipes.com/recipe/7691/fabulous-fudge-ribbon-cake/', 'https://www.allrecipes.com/recipe/262841/no-egg-chocolate-mug-cake/', 'https://www.allrecipes.com/recipe/215016/triple-chocolate-tofu-brownies/', 'https://www.allrecipes.com/recipe/7959/mississippi-mud-cake-iii/', 'https://www.allrecipes.com/recipe/15706/chocolate-scotch-whiskey-cake/', 'https://www.allrecipes.com/recipe/8285/mayonnaise-cake-iii/', 'https://www.allrecipes.com/recipe/71691/mocha-sponge-cake/', 'https://www.allrecipes.com/recipe/257358/rice-flour-mexican-chocolate-cupcakes-gluten-free/', 'https://www.allrecipes.com/recipe/8420/chocolate-zucchini-cake-ii/', 'https://www.allrecipes.com/recipe/7302/the-best-chocolate-cake-you-ever-ate/', 'https://www.allrecipes.com/recipe/8198/boiled-chocolate-delight-cake/', 'https://www.allrecipes.com/recipe/7383/hollys-black-forest-cake/', 'https://www.allrecipes.com/recipe/8115/chocolate-mayonnaise-cake-ii/', 'https://www.allrecipes.com/recipe/8098/french-chocolate-cake/', 'https://www.allrecipes.com/recipe/276302/chocolate-lava-cake-with-coconut-and-almond/', 'https://www.allrecipes.com/recipe/7316/philadelphia-red-cake/', 'https://www.allrecipes.com/recipe/21266/old-fashioned-chocolate-cake/', 'https://www.allrecipes.com/recipe/8176/peanut-butter-fudge-cake/', 'https://www.allrecipes.com/recipe/263050/vegan-chocolate-cupcakes-with-vanilla-frosting/', 'https://www.allrecipes.com/recipe/233674/minute-chocolate-mug-cake/', 'https://www.allrecipes.com/recipe/15494/salad-dressing-cupcakes/', 'https://www.allrecipes.com/recipe/17377/chocolate-cupcakes/', 'https://www.allrecipes.com/recipe/75135/swedish-sticky-chocolate-cake-kladdkaka/', 'https://www.allrecipes.com/recipe/279132/grandma-jeans-buttermilk-chocolate-cake/', 'https://www.allrecipes.com/recipe/7251/chocolate-zucchini-cake-i/', 'https://www.allrecipes.com/recipe/7476/grandmas-chocolate-marvel-cake/', 'https://www.allrecipes.com/recipe/8421/chocolate-decadence-cake-ii/', 'https://www.allrecipes.com/recipe/7365/barbs-chocolate-cake/', 'https://www.allrecipes.com/recipe/17370/chocolate-cake-ii/', 'https://www.allrecipes.com/recipe/17499/chocolate-pudding-cake-iii/', 'https://www.allrecipes.com/recipe/80902/alannahs-chocolate-galaxy/', 'https://www.allrecipes.com/recipe/7659/deep-dark-chocolate-peppermint-cake/', 'https://www.allrecipes.com/recipe/260797/best-chocolate-cream-cheese-pound-cake/', 'https://www.allrecipes.com/recipe/7747/grandpops-special-chocolate-cake/', 'https://www.allrecipes.com/recipe/7636/halloween-layer-cake/', 'https://www.allrecipes.com/recipe/25615/texas-sheet-cake-vi/', 'https://www.allrecipes.com/recipe/242520/vegan-wacky-cake/', 'https://www.allrecipes.com/recipe/110312/sacher-torte/', 'https://www.allrecipes.com/recipe/270952/mocha-chia-cake/', 'https://www.allrecipes.com/recipe/8374/chocolate-macaroon-bundt-cake/', 'https://www.allrecipes.com/recipe/7530/mississippi-mud-cake-i/', 'https://www.allrecipes.com/recipe/258760/torta-caprese-con-le-noci-italian-chocolate-cake/', 'https://www.allrecipes.com/recipe/25640/tracys-favorite-three-hole-cake/', 'https://www.allrecipes.com/recipe/7548/dr-pepper-cake/', 'https://www.allrecipes.com/recipe/8086/black-forest-chocolate-cake/', 'https://www.allrecipes.com/recipe/7319/double-chocolate-cake-i/', 'https://www.allrecipes.com/recipe/7775/wacky-cake-iii/', 'https://www.allrecipes.com/recipe/7641/sauerkraut-surprise-cake/', 'https://www.allrecipes.com/recipe/7309/praline-chocolate-cake/', 'https://www.allrecipes.com/recipe/25582/chocolate-crazy-cake/', 'https://www.allrecipes.com/recipe/8095/black-forest-cake-i/', 'https://www.allrecipes.com/recipe/8221/black-bottom-cupcakes-i/', 'https://www.allrecipes.com/recipe/16480/fourteen-layer-chocolate-cake/', 'https://www.allrecipes.com/recipe/7475/crazy-cake/', 'https://www.allrecipes.com/recipe/19110/yogurt-chocolate-cake/', 'https://www.allrecipes.com/recipe/25609/my-moms-chocolate-cake/', 'https://www.allrecipes.com/recipe/7965/victory-chocolate-cake/', 'https://www.allrecipes.com/recipe/260283/easy-vegan-chocolate-cake/', 'https://www.allrecipes.com/recipe/7337/passover-brownie-cake/', 'https://www.allrecipes.com/recipe/7671/sourdough-chocolate-cake/', 'https://www.allrecipes.com/recipe/15503/grandma-gudgels-black-bottom-cupcakes/', 'https://www.allrecipes.com/recipe/260423/cassava-flour-chocolate-mayonnaise-cake/', 'https://www.allrecipes.com/recipe/232055/chocolate-buttermilk-layer-cake/', 'https://www.allrecipes.com/recipe/69133/hazelnut-truffle-cupcakes/', 'https://www.allrecipes.com/recipe/280733/dark-chocolate-beet-cake/', 'https://www.allrecipes.com/recipe/8282/red-velvet-cake-iv/', 'https://www.allrecipes.com/recipe/23583/pumpkin-chocolate-dessert-cake/', 'https://www.allrecipes.com/recipe/7606/caramel-nougat-cake-iv/', 'https://www.allrecipes.com/recipe/8334/chocolate-date-cake-i/', 'https://www.allrecipes.com/recipe/17899/chocolate-sheet-cake-i/', 'https://www.allrecipes.com/recipe/240560/chocolate-cake-in-a-mug/', 'https://www.allrecipes.com/recipe/7269/fabulous-fudge-chocolate-cake/', 'https://www.allrecipes.com/recipe/263646/best-ever-vegan-chocolate-mug-cake/', 'https://www.allrecipes.com/recipe/8193/chocolate-butterschnapps-cake/', 'https://www.allrecipes.com/recipe/228344/old-southern-chocolate-pecan-sheet-cake/', 'https://www.allrecipes.com/recipe/38283/tofu-chocolate-cake/', 'https://www.allrecipes.com/recipe/275698/the-real-red-velvet-cake/', 'https://www.allrecipes.com/recipe/17436/rich-chocolate-cake-i/', 'https://www.allrecipes.com/recipe/256094/slow-cooker-peanut-butter-fudge-cake/', 'https://www.allrecipes.com/recipe/7289/texas-sheet-cake-ii/', 'https://www.allrecipes.com/recipe/260785/mexican-chocolate-chile-cake/', 'https://www.allrecipes.com/recipe/7536/kellys-apple-cocoa-cake/', 'https://www.allrecipes.com/recipe/220980/chocolate-passover-sponge-cake/', 'https://www.allrecipes.com/recipe/257208/super-moist-chocolate-cake/', 'https://www.allrecipes.com/recipe/241040/10-minute-chocolate-mug-cake/', 'https://www.allrecipes.com/recipe/23056/texas-sheet-cake-v/', 'https://www.allrecipes.com/recipe/25605/mimis-300-dollar-chocolate-cake/', 'https://www.allrecipes.com/recipe/245576/dark-chocolate-souffle-cupcakes/', 'https://www.allrecipes.com/recipe/8277/mmmmmm-chocolate-cake/', 'https://www.allrecipes.com/recipe/7807/german-marble-cake/', 'https://www.allrecipes.com/recipe/278642/high-altitude-chocolate-cake/', 'https://www.allrecipes.com/recipe/7462/flourless-chocolate-roll/', 'https://www.allrecipes.com/recipe/7961/chocolate-graham-nut-cake/', 'https://www.allrecipes.com/recipe/232875/gluten-free-chocolate-cake/', 'https://www.allrecipes.com/recipe/44655/willie-cake/', 'https://www.allrecipes.com/recipe/7617/spintz-cake/', 'https://www.allrecipes.com/recipe/245320/chocolate-fig-cake/', 'https://www.allrecipes.com/recipe/222647/black-forest-cheesecakes/', 'https://www.allrecipes.com/recipe/15898/mamaws-devils-food-cake/', 'https://www.allrecipes.com/recipe/8004/pennsylvania-dutch-funny-cakes/', 'https://www.allrecipes.com/recipe/259922/fallen-chocolate-souffle-mini-cakes/', 'https://www.allrecipes.com/recipe/219907/amazing-slow-cooker-chocolate-cake/', 'https://www.allrecipes.com/recipe/7693/mocha-magic-torte/', 'https://www.allrecipes.com/recipe/212429/red-velvet-cupcakes/', 'https://www.allrecipes.com/recipe/17981/one-bowl-chocolate-cake-iii/', 'https://www.allrecipes.com/recipe/241447/gluten-free-chocolate-cake-with-coconut/', 'https://www.allrecipes.com/recipe/8158/non-dairy-chocolate-cake-with-german-chocolate-frosting/', 'https://www.allrecipes.com/recipe/8242/heavenly-hash-cake/', 'https://www.allrecipes.com/recipe/7442/mayonnaise-cake-ii/', 'https://www.allrecipes.com/recipe/8477/old-fashioned-red-devils-food-cake/', 'https://www.allrecipes.com/recipe/245745/red-devils-food-cake/', 'https://www.allrecipes.com/recipe/8444/black-forest-cake-ii/', 'https://www.allrecipes.com/recipe/242471/chocolate-coconut-cake-from-king-arthur-flour/', 'https://www.allrecipes.com/recipe/7393/hot-fudge-cake/', 'https://www.allrecipes.com/recipe/22953/dark-chocolate-cake-ii/', 'https://www.allrecipes.com/recipe/264609/the-best-chocolate-souffle-torte/', 'https://www.allrecipes.com/recipe/278159/chocolate-ganache-cake/', 'https://www.allrecipes.com/recipe/8096/boiled-cake/', 'https://www.allrecipes.com/recipe/141024/gluten-free-chocolate-cake-with-semi-sweet-chocolate-icing/', 'https://www.allrecipes.com/recipe/17622/moist-chocolate-cake/', 'https://www.allrecipes.com/recipe/26002/chocolate-sheet-cake-iii/', 'https://www.allrecipes.com/recipe/278981/grandmas-chocolate-texas-sheet-cake/', 'https://www.allrecipes.com/recipe/7457/sauerkraut-cake/', 'https://www.allrecipes.com/recipe/7514/microwave-mississippi-mud-cake-i/', 'https://www.allrecipes.com/recipe/7448/chocolate-sauerkraut-cake-i/', 'https://www.allrecipes.com/recipe/7394/crazy-chocolate-cake/', 'https://www.allrecipes.com/recipe/7681/midnight-moon-cake/', 'https://www.allrecipes.com/recipe/259901/italian-chocolate-and-ricotta-cake/', 'https://www.allrecipes.com/recipe/232342/moist-chocolate-layer-cake/', 'https://www.allrecipes.com/recipe/7828/dianes-german-chocolate-cake/', 'https://www.allrecipes.com/recipe/230780/warm-chocolate-peanut-butter-pudding-cake/', 'https://www.allrecipes.com/recipe/17714/hot-fudge-pudding-cake-iii/', 'https://www.allrecipes.com/recipe/65207/chocolate-float/', 'https://www.allrecipes.com/recipe/241038/microwave-chocolate-mug-cake/', 'https://www.allrecipes.com/recipe/276632/chocolate-yogurt-cake/', 'https://www.allrecipes.com/recipe/25960/best-moist-chocolate-cake/', 'https://www.allrecipes.com/recipe/8395/eggless-chocolate-cake-ii/', 'https://www.allrecipes.com/recipe/17653/lynns-carrot-cake/', 'https://www.allrecipes.com/recipe/241309/chef-johns-chocolate-decadence/', 'https://www.allrecipes.com/recipe/237504/chocolate-chip-sour-cream-cake/', 'https://www.allrecipes.com/recipe/276304/lava-cake/', 'https://www.allrecipes.com/recipe/244229/vegan-double-chocolate-peanut-butter-banana-cake/', 'https://www.allrecipes.com/recipe/7294/chocolate-cherry-upside-down-cake/', 'https://www.allrecipes.com/recipe/27443/german-sweet-chocolate-cake-ii/', 'https://www.allrecipes.com/recipe/7531/mississippi-mud-cake-ii/', 'https://www.allrecipes.com/recipe/7984/two-bowl-cake/', 'https://www.allrecipes.com/recipe/231893/idahoan-molten-lava-cakes/', 'https://www.allrecipes.com/recipe/254766/black-forest-cake-jell-o-shot/', 'https://www.allrecipes.com/recipe/7481/miami-beach-cake/', 'https://www.allrecipes.com/recipe/7685/wacky-cake-ii/', 'https://www.allrecipes.com/recipe/258319/black-forest-pancake-cake/', 'https://www.allrecipes.com/recipe/7377/prune-mocha-cake/', 'https://www.allrecipes.com/recipe/8117/texas-sheet-cake-iii/', 'https://www.allrecipes.com/recipe/15391/one-bowl-chocolate-cake-i/', 'https://www.allrecipes.com/recipe/25569/death-by-chocolate-v/', 'https://www.allrecipes.com/recipe/245743/red-devils-food-cake-with-lemon-frosting/', 'https://www.allrecipes.com/recipe/25570/devils-food-cake-ii/', 'https://www.allrecipes.com/recipe/8351/surprise-cake/', 'https://www.allrecipes.com/recipe/279642/instant-pot-torta-caprese-italian-flourless-chocolate-almond-cake/', 'https://www.allrecipes.com/recipe/241406/amazing-chocolate-beet-cake/', 'https://www.allrecipes.com/recipe/26018/cream-filled-cupcakes/', 'https://www.allrecipes.com/recipe/278639/double-chocolate-layer-cake/', 'https://www.allrecipes.com/recipe/25999/chocolate-pound-cake-iii/', 'https://www.allrecipes.com/recipe/276684/german-chocolate-texas-sheet-cake-with-coconut-pecan-frosting/', 'https://www.allrecipes.com/recipe/7942/special-chocolate-cake-i/', 'https://www.allrecipes.com/recipe/279362/waste-not-cake/', 'https://www.allrecipes.com/recipe/257191/rich-and-gooey-hot-chocolate-mousse-cake/', 'https://www.allrecipes.com/recipe/271118/chocolate-cupcakes-with-cream-cheese-oreo-buttercream-frosting/', 'https://www.allrecipes.com/recipe/215273/nairobi-chocolate-cake/', 'https://www.allrecipes.com/recipe/26003/simple-chocolate-strawberry-shortcake/', 'https://www.allrecipes.com/recipe/8050/rich-and-chocolaty-syrup-cake/', 'https://www.allrecipes.com/recipe/8260/chocolate-cake-in-a-jar-ii/', 'https://www.allrecipes.com/recipe/7312/chocolate-cake-i/', 'https://www.allrecipes.com/recipe/277291/baked-chocolate-mousse-cake/', 'https://www.allrecipes.com/recipe/21677/chocolate-date-cake-ii/', 'https://www.allrecipes.com/recipe/261678/heart-cake/', 'https://www.allrecipes.com/recipe/8354/chocolate-pinwheel-cake/', 'https://www.allrecipes.com/recipe/260741/halloween-chocolate-cupcakes-with-monster-peanut-butter-eyes/', 'https://www.allrecipes.com/recipe/8252/chocolate-angel-food-cake-i/', 'https://www.allrecipes.com/recipe/8309/zucchini-chocolate-orange-cake/', 'https://www.allrecipes.com/recipe/7425/red-velvet-cake-i/', 'https://www.allrecipes.com/recipe/256995/chocolate-and-guinness-cake/', 'https://www.allrecipes.com/recipe/17643/chocolate-zucchini-cake-iii/', 'https://www.allrecipes.com/recipe/25985/chocolate-cake-v/', 'https://www.allrecipes.com/recipe/7736/dark-chocolate-cake-i/', 'https://www.allrecipes.com/recipe/7744/chocolate-roll-ii/', 'https://www.allrecipes.com/recipe/264153/chocolate-beet-cake/', 'https://www.allrecipes.com/recipe/219964/chef-johns-chocolate-lava-cake/', 'https://www.allrecipes.com/recipe/256538/easy-flourless-chocolate-cake/', 'https://www.allrecipes.com/recipe/237736/gluten-free-moist-chocolate-cake/', 'https://www.allrecipes.com/recipe/7646/chocolate-buttermilk-cake/', 'https://www.allrecipes.com/recipe/170472/sneaky-mommys-chocolate-zucchini-cake/', 'https://www.allrecipes.com/recipe/17659/mocha-bundt-cake/', 'https://www.allrecipes.com/recipe/262543/seven-minute-gooey-chocolate-fudge-microwave-cake/', 'https://www.allrecipes.com/recipe/7808/chocolate-orange-marble-cake/', 'https://www.allrecipes.com/recipe/8376/chocolate-pound-cake-ii/', 'https://www.allrecipes.com/recipe/22388/tex-mex-sheet-cake/', 'https://www.allrecipes.com/recipe/8007/low-sugar-mocha-nut-cake/', 'https://www.allrecipes.com/recipe/273130/moist-chocolate-birthday-cake/', 'https://www.allrecipes.com/recipe/15392/wellesley-fudge-cake-i/', 'https://www.allrecipes.com/recipe/8327/chocolate-cherry-chip-cake/', 'https://www.allrecipes.com/recipe/238152/knock-your-socks-off-vegan-chocolate-cake/', 'https://www.allrecipes.com/recipe/17399/jans-chocolate-cake/', 'https://www.allrecipes.com/recipe/262582/easter-bird-nest-cupcakes/', 'https://www.allrecipes.com/recipe/269591/dark-and-creamy-chocolate-cake/', 'https://www.allrecipes.com/recipe/18180/microwave-mississippi-mud-cake-ii/', 'https://www.allrecipes.com/recipe/7867/moms-chocolate-cake/', 'https://www.allrecipes.com/recipe/259446/one-pan-cake/', 'https://www.allrecipes.com/recipe/7266/cocoa-apple-cake/', 'https://www.allrecipes.com/recipe/221852/delicious-chocolate-fondant/', 'https://www.allrecipes.com/recipe/257606/paleo-chocolate-lovers-mug-cake/', 'https://www.allrecipes.com/recipe/19082/quick-cake/', 'https://www.allrecipes.com/recipe/7433/baumkuchen/', 'https://www.allrecipes.com/recipe/216732/strawberry-chocolate-mini-cupcakes-with-white-chocolate-ganache/', 'https://www.allrecipes.com/recipe/17095/chocolate-oatmeal-cake/', 'https://www.allrecipes.com/recipe/245747/black-forest-cake-bars/', 'https://www.allrecipes.com/recipe/260058/hot-fudge-brownie-cake/', 'https://www.allrecipes.com/recipe/23733/chocolate-angel-food-cake-ii/', 'https://www.allrecipes.com/recipe/22955/chocolate-surprise-cupcakes/']

    print(len(new_links_list))
    print(new_links_list)
    recipes_dict = {}
    servings_list = []
    eggs_amount = []
    butter_amount = []
    sugar_lst = []
    for link in new_links_list:
        print("linkk", link)
        sleep(1.5)
        html_page = get_html_page_from_link(link)
        ingredient_list = get_ingredients_list_from_page(html_page)
        new_ing_lst = clean_ingredients(ingredient_list)
        print(new_ing_lst)
        eggs = get_eggs_num(new_ing_lst)
        eggs_amount.append(eggs)
        #
        butter = get_butter_num(new_ing_lst)
        butter_amount.append(butter)

        sugar = get_sugar_1(new_ing_lst)
        sugar_amount = get_sugar_in_numbers_1(sugar)
        sugar_lst.append(sugar_amount)

        recipes_dict[link] = new_ing_lst


        serving = get_servings_num_as_str(html_page)
        print(serving)
        servings_list.append(serving)
    print("recipes_dict", recipes_dict)
    sugar = get_sugar(recipes_dict)
    best_sugar_dict = get_sugar_in_numbers(sugar)
    sugar_avg = get_amount_avg(best_sugar_dict)
    print("sugar avg", sugar_avg)
    print("eggs", eggs_amount)
    print("butter", butter_amount)
    amounts_lst = amounts_in_lst(best_sugar_dict)
    print("servings_list", servings_list)
    print("sugar", sugar_lst)
    get_avg(servings_list, amounts_lst)
    return amounts_lst

#print(main_function())

def count_for_hist(amounts_lst):
    """Gets amounts list and return a short list: counts how much between 0-0.5, 0.5-1, etc. - for hist"""
    count_hist = [0]*9
    for i in amounts_lst:
        if i <= 0.5:
            count_hist[0] += 1
            continue
        elif i <= 1:
            count_hist[1] += 1
            continue
        elif i <= 1.5:
            count_hist[2] += 1
            continue
        elif i <= 2:
            count_hist[3] += 1
            continue
        elif i <= 2.5:
            count_hist[4] += 1
            continue
        elif i <= 3:
            count_hist[5] += 1
            continue
        elif i <= 3.5:
            count_hist[6] += 1
            continue
        elif i <= 4:
            count_hist[7] += 1
            continue
        elif i <= 4.5:
            count_hist[8] += 1
            continue
        elif i <= 5:
            count_hist[9] += 1
            continue
    return count_hist

print("ddd")
print(main_function())

































# print(len(a))
# print(a)