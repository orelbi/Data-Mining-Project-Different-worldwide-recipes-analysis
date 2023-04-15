
from bs4 import BeautifulSoup
import requests
import re
from time import sleep
import json
import numpy



""" website UK (british) gets links for chocolate cakes recipes. then, it 
calculates and print sugar amounts (and avg), butter amounts, eggs amounts, and
servings num  (as lists)"""

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
    print(link)
    url_text = requests.get(link[1:-1]).text
    #print(link)
    #print(url_text)

    html_page = BeautifulSoup(url_text, 'lxml')
    #print("byyy", link)
    return html_page


def get_sugar_list_from_page(html_page):
    """Gets a web_page and returns the sugar list from it"""
    sugar_list = []
   # ingredients = html_page.findAll('span', itemprop_="ingredients")
    ingredients = str(html_page).split("span")

    for ing in ingredients:
       # print(str(ing))
        if "sugar" in ing and "ingredients" in ing:
            new_ing = str(ing)
            sugar_list.append(new_ing)
    return sugar_list


def clean_sugar(sugar_list):
    """Gets sugar list, returns just the amount"""
    new_sugar_lst = []
    numberrr = "1234567890"
    amount_sum = 0
    for sentence in sugar_list:
        ezer = 0
        amount = ""
        if "reviewBody" in sentence:
            break
        elif "DOCTYPE" in sentence:
            continue
        for letter in sentence:
            if letter in numberrr:
                ezer = 1
                amount += letter
            elif ezer == 1 and letter == "g":
                amount_sum += int(amount)
                break
            elif ezer == 1 and letter == "t":
                amount_sum += (int(amount) * 10.5)
                break
    print("amount_sum", amount_sum)
    print("sugar_lst", sugar_list)
    return amount_sum

    # for i in ingredient_list:
        # x = i.split("\n")
        # y = x[1]
      #  new_sugar_lst.append(y[48:])
    # return new_sugar_lst

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
    ser_text = html_page.find('span', class_="accent").text
    real_ser = ser_text[1:-1]

    if "1" in real_ser or "2" in real_ser or "3" in real_ser or "4" in real_ser or "5" in real_ser or "6" in real_ser or "7" in real_ser or "8" in real_ser or "9" in real_ser or "0" in real_ser:
        real_ser_in_number = int(real_ser)
        print(real_ser_in_number)
        return real_ser_in_number
    else:
        print("not good", real_ser)
        return "0"
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
        if int(servings[i]) != 0:
            new_amounts.append(int(sugar_amounts[i])/int(servings[i]))
        elif int(servings[i]) == 0:
            new_amounts.append(0)
    av = numpy.average(new_amounts)

    print(new_amounts)
    print(av)

def get_eggs_from_page(html_page):
    """Gets a web_page and returns the eggs list from it"""
    eggs_ing = "0"
   # ingredients = html_page.findAll('span', itemprop_="ingredients")
    ingredients = str(html_page).split("span")

    for ing in ingredients:
       # print(str(ing))
        if "egg" in ing and "ingredients" in ing and len(ing) < len("eggs_mess  data-original=2 eggs itemprop=ingredients>2 eggs<eggs_mess  data-original=2 eggs itemprop=ingredients>2 eggs</") :
            eggs_ing = str(ing)
            break
    return eggs_ing


def clean_eggs(eggs_mess):
    if eggs_mess == "0":
        return 0
    else:
        counter = 0
        eggs_amount = ""
        for letter in eggs_mess:
            if letter in "1234567890":
                counter += 1
                eggs_amount += letter
            elif letter not in "1234567890" and counter != 0:
                return int(eggs_amount)
        return int(eggs_amount)

####### butter


def get_butter_from_page(html_page):
    """Gets a web_page and returns the eggs list from it"""
    butter_ing = "0"
   # ingredients = html_page.findAll('span', itemprop_="ingredients")
    ingredients = str(html_page).split("span")

    for ing in ingredients:
       # print(str(ing))
        if "butter" in ing and "ingredients" in ing and len(ing) < len("eggs_mess  data-original=2 eggs itemprop=ingredients>2 eggs<eggs_mess  data-original=2 eggs itemprop=ingredients>2 eggs</") :
            butter_ing = str(ing)
            break
    print("butter_ing", butter_ing)
    return butter_ing


def clean_butter(butter_mess):
    if butter_mess == "0":
        return 0
    else:
        counter = 0
        butter_amount = ""
        for letter in butter_mess:
            if letter in "1234567890":
                counter += 1
                butter_amount += letter
            elif letter not in "1234567890" and counter != 0:
                return float(butter_amount)
        if butter_amount == "":
            butter_amount = 100
        return float(butter_amount)
    ########################

def main_function(new_links_list):
    #new_links_list = get_recipes_links(urli,493)
    print(len(new_links_list))
    print(new_links_list)
    recipes_dict = {}
    servings_list = []
    amounts_lst = []
    eggs_amounts = []
    butter_amounts = []
    for link in new_links_list:
        print("now", link)
        sleep(1.5)
        html_page = get_html_page_from_link(link)
        print("2")
        serving = get_servings_num_as_str(html_page)
        servings_list.append(serving)

        eggs_mess = get_eggs_from_page(html_page)
        eggs_clean = clean_eggs(eggs_mess)
        print("eggs_mess", eggs_mess)
        print("eggs clean'", eggs_clean)
        eggs_amounts.append(eggs_clean)

        butter_mess = get_butter_from_page(html_page)
        butter_clean = clean_butter(butter_mess)
        print("butter_mess", butter_mess)
        print("butter_clean", butter_clean)
        butter_amounts.append(butter_clean)

        sugar_list = get_sugar_list_from_page(html_page)
        print("3")
        sugar_amount = clean_sugar(sugar_list)
        amounts_lst.append(sugar_amount)
        recipes_dict[link] = sugar_amount
        serving = get_servings_num_as_str(html_page)
    print(recipes_dict)
    # sugar = get_sugar(recipes_dict)
    # best_sugar_dict = get_sugar_in_numbers(sugar)
    # sugar_avg = get_amount_avg(best_sugar_dict)
    # print(sugar_avg)
    # amounts_lst = amounts_in_lst(best_sugar_dict)
    print("servings", servings_list)
    print("sugar", amounts_lst)
    print("eggs", eggs_amounts)
    print("butter", butter_amounts)

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

new_links_list = ['"http://allrecipes.co.uk/recipe/18892/easy-chocolate-cake-with-chocolate-icing.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/38468/white-chocolate---raspberry-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/12189/my-infallible-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/37149/dairy-free-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8008/30-minute-chocolate-cake-with-quick-chocolate-icing.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/42066/simple-chocolate-fridge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/6793/chocolate-surprise-fairy-cakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/7514/chocolate-cup-cakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4666/vegan-chocolate-cake.aspx?o_is=Hub_TopRecipe_4" ', '"http://allrecipes.co.uk/recipe/45163/healthy-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4534/egg-free-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/42439/decadent-flourless-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/45852/chocolate-banana-and-peach-loaf-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/26639/dark-chocolate-and-raspberry-cake.aspx?o_is=Hub_TopRecipe_4" ', '"http://allrecipes.co.uk/recipe/8421/whisky-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/40130/indulgent-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/39853/chocolate-fudge-cake-with-chocolate-ganache.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8547/never-fail-chocolate-mousse-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8423/eggless-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8763/lois--7-minute-gooey-chocolate-fudge-cake.aspx?o_is=Hub_TopRecipe_2" ', '"http://allrecipes.co.uk/recipe/35657/deluxe-chocolate-fridge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35987/no-bake-chocolate-orange-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/17062/chocolate-olive-oil-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35793/choco-prince-biscuit-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35634/gluten-free-chocolate-sponge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18765/simple-dairy-free-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/29511/easy-chocolate-heaven-cupcakes-or-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/45139/chocolate-fruit-and-nut-fridge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/46718/unicorn-chocolate-birthday-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35819/chocolate-cupcakes-with-nutella--buttercream-icing.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/31168/whisky-chocolate-truffle-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35635/gluten-free-chocolate-cake-with-mascarpone-cream-and-berries.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/46357/chocolate-chip-chocolate-loaf-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/29455/chocolate-fridge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35014/chocolate-chip-madeira-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/26231/chocolate-and-banana-mini-sponge-cakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/32945/terrys-chocolate-orange-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4829/chocolate-mousse-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18869/marbled-chocolate-orange-cake.aspx?o_is=Hub_TopRecipe_5" ', '"http://allrecipes.co.uk/recipe/34332/chocolate-fudge-cake-traybake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/39531/gluten-free-chocolate-mug-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/7622/5-minute-chocolate-mug-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18821/chocolate-cupcakes-with-caramel-icing.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/42422/gluten-free-coconut-oil-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/31120/bel-s-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/27316/chocolate-covered-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/24410/delicious-and-moist-fresh-cream-chocolate-fudge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4526/passover-chocolate-sponge-cake.aspx?o_is=Hub_TopRecipe_4" ', '"http://allrecipes.co.uk/recipe/34447/rich-chocolate-hazelnut-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/22501/chocolate-birthday-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/39264/chocolate-fudge-cake-s.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8048/cheeky-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/17706/white-chocolate-layer-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/12187/vegan-glazed-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/24637/lauren-s-chocolate-mug-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/45357/two-chocolate-mug-cakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/480/chocolate-cherry-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/47387/flourless-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/37254/flourless-chocolate-mousse-cake-with-dulce-de-leche.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/52677/chocolate-cake-with-coffee-yoghurt.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35424/cream-filled-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4526/passover-chocolate-sponge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/40496/mint-chocolate-chip-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/19129/one-dish-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/34137/simple-but-scrumptious-white-chocolate-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/16595/rich-chocolate-mousse-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/13842/classic-chocolate-mousse-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/16998/baked-chocolate-orange-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35096/chocolate-and-ricotta-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/36962/chocolate-chunk-loaf-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/16502/fudgy-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/42704/black-forest-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/34557/chocolate-chip-loaf-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/17241/chocolate-and-orange-cup-cakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/41620/chocolate-brownie-teacup-cakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/33569/vegan-chocolate-courgette-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/13024/easy-peasy-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/9969/boozy-double-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8429/courgette-chocolate-orange-cake.aspx?o_is=Hub_TopRecipe_1" ', '"http://allrecipes.co.uk/recipe/18858/gluten-free-chocolate-mousse-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18890/no-frills-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/25173/chocolate-mouse-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/25726/easy-chocolate-fudge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/11264/chocolate-and-orange-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18913/classic-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/34692/white-chocolate-chip-loaf-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/20340/tropical-chocolate-carrot-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18859/no-bake-chocolate-mousse-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/14480/italian-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8420/1-bowl-chocolate-cake.aspx?o_is=Hub_TopRecipe_1" ', '"http://allrecipes.co.uk/recipe/35774/chocolate-orange-cheesecake-with-chocolate-icing.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4517/dark-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/7625/orietta-s-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/39665/chocolate-oreo-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/26772/storecupboard-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/12203/heavenly-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/6722/gluten-free-chocolate-cake.aspx?o_is=Hub_TopRecipe_4" ', '"http://allrecipes.co.uk/recipe/26005/easy-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/10133/no-bake-chocolate-biscuit-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/33135/easy-and-tasty-chocolate-mug-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/52200/rich-gluten-free-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/12934/8-minute-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/30611/my-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4956/easy-flourless-chocolate-cake.aspx?o_is=Hub_TopRecipe_1" ', '"http://allrecipes.co.uk/recipe/25346/cranberry-and-apple-baked-white-chocolate-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/45977/gluten-free-chocolate-espresso-mug-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18771/cherry-chocolate-upside-down-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/50310/chocolate-and-strawberry-jelly-marble-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8468/white-chocolate-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18891/beth-s-moist-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/31983/chocolate-malteser-reg--cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/19445/egg-free--dairy-free-and-nut-free-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/34688/chocolate-orange-cupcakes-with-a-twist.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/31774/chocolate-sandwich-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/31435/chocolate-and-vanilla-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/43082/gluten-free-chocolate-and-cayenne-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/44547/gluten-free-advocaat-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/31820/grandi-s-chocolate-mousse-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18010/chocolate--peanut-and-banana-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/6217/chocolate-muffin-spider-cakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/31432/microwave-small-chocolate-cupcake-brownies.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/30542/white-and-milk-chocolate-cheesecake.aspx?o_is=Hub_TopRecipe_5" ', '"http://allrecipes.co.uk/recipe/19791/moist-vegan-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4534/egg-free-chocolate-cake.aspx?o_is=Hub_TopRecipe_5" ', '"http://allrecipes.co.uk/recipe/26077/easter-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/39898/gluten-free-coconut--white-chocolate--and-cherry-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/16273/moist-chocolate-cake-with-dark-chocolate-sauce.aspx?o_is=Hub_TopRecipe_3" ', '"http://allrecipes.co.uk/recipe/40981/yummy-gluten-free-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/36266/chocolate-and-almond-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/30256/large-chocolate-sponge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/34928/chocolate-orange-marble-cake.aspx?o_is=Hub_TopRecipe_4" ', '"http://allrecipes.co.uk/recipe/23404/chocolate-biscuit-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/29532/easy-banana-chocolate-chip-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/17486/shake-n-bake-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35001/perfect-chocolate-loaf-cake.aspx?o_is=Hub_TopRecipe_2" ', '"http://allrecipes.co.uk/recipe/4956/easy-flourless-chocolate-cake.aspx?o_is=Hub_TopRecipe_2" ', '"http://allrecipes.co.uk/recipe/39305/gran-s-chocolate-biscuit-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/40141/gluten-free-chocolate-chip-bundt-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35995/dark-chocolate-and-chilli-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/39156/gluten-free-chocolate-fudge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35410/simple-and-easy-chocolate-sponge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/25153/always-perfect-chocolate-sponge-cake.aspx?o_is=Hub_TopRecipe_3" ', '"http://allrecipes.co.uk/recipe/39524/flourless-chocolate-mousse-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/43880/white-chocolate-key-lime-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/16143/delicious-eggless-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/16088/heather-s-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/13151/chocolate-cake-with-ganache.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/38993/double-chocolate-strong-mint-cup-cakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/7079/rich-and-easy-egg-free-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4510/chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/12300/lightning-fast-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/6133/white-chocolate-and-raspberry-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35117/white-chocolate-and-strawberry-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/39280/gluten-free-chocolate-chickpea-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/24256/oreo-reg--and-white-chocolate-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/43591/chocolate-chip-courgette-loaf-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/41509/banana-chocolate-chip-cupcakes-with-cream-cheese-frosting.aspx?o_is=Hub_TopRecipe_3" ', '"http://allrecipes.co.uk/recipe/9402/very-chocolatey-chocolate-mousse-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/41090/chocolate-marshmallow-crispy-cakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/34764/chocolate-madeira-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/6041/chocolate-and-beetroot-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35433/vegan-chocolate-fudge-cake.aspx?o_is=Hub_TopRecipe_4" ', '"http://allrecipes.co.uk/recipe/32239/egg-free-chocolate-fudge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/28667/chocolate-and-guinness-reg--cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/15802/spiced-chocolate-banana-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/55326/walnut-chocolate-loaf-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8428/elizabeth-s-chocolate-lover-s-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/38323/decadent-chocolate-mousse-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/34289/dark-choco-orange-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4641/chocolate-courgette-fairy-cakes-with-chocolate-icing.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/45811/easy-peasy-super-moist-dairy-free-chocolate-cake-.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/13140/three-layer-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/32013/chocolate-pyramid-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18761/syd-s-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/36240/fabulous-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4686/chocolate-pudding-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8426/no-fail-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/28083/double-layer-pear-and-chocolate-mousse-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/28268/double-chocolate--peanut-butter-and-banana-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8543/gorgeous-chocolate-mousse-cake.aspx?o_is=Hub_TopRecipe_5" ', '"http://allrecipes.co.uk/recipe/32456/mum-s-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18847/dairy-free-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/41612/chocolate-and-cherry-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/38773/easy-peasy-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/50284/ale-s-white-chocolate-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/38280/gluten-free-chocolate-spiderweb-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/16804/chocolate-topped-orange-and-almond-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/29622/easy-chocolate-fridge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/12513/orange-and-white-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18369/chocolate-brownie-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/32768/egg-free-chocolate-sponge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/24904/creamy-white-chocolate-cheesecake.aspx?o_is=Hub_TopRecipe_3" ', '"http://allrecipes.co.uk/recipe/46035/chocolate-mascarpone-layer-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/19149/buttercream-chocolate-cupcakes.aspx?o_is=Hub_TopRecipe_5" ', '"http://allrecipes.co.uk/recipe/653/double-chocolate-fairy-cakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/31967/scrummy-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8763/lois--7-minute-gooey-chocolate-fudge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/11972/chocolate-and-coffee-cupcakes-with-baileys-reg--buttercream.aspx?o_is=Hub_TopRecipe_1" ', '"http://allrecipes.co.uk/recipe/47138/chocolate-cupcakes-with-chocolate-icing.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/34488/orange-and-chocolate-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/29346/tasty-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/28234/ellen-s-perfect-raspberry-and-white-chocolate-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/25188/chocolate-guinness-reg--cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/16790/easy-peasy-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/16573/devilish-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/6535/raspberry-and-white-chocolate-cheesecake.aspx?o_is=Hub_TopRecipe_1" ', '"http://allrecipes.co.uk/recipe/23955/wickedly-dark-chocolate-and-chilli-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/45699/vegan-chocolate-and-peanut-butter-banana-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/32123/banana--chocolate-chip-and-fudge-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/25880/chocolate-beetroot-cake-with-chocolate-icing.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/54892/amarettini-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/44699/dark-chocolate-butternut-squash-loaf-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/31544/fig-and-chocolate-olive-oil-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/39510/gluten-free-chocolate-coconut-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/52328/chocolate-sandwich-cake-with-mascarpone-filling.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4527/molten-chocolate-cakes.aspx?o_is=Hub_TopRecipe_4" ', '"http://allrecipes.co.uk/recipe/8351/rich-dark-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/7115/rich-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/41191/easy-chocolate-fudge-layer-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/26455/best-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/26032/white-chocolate-and-lime-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/13513/bat-shaped-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/12009/chocolate-orange-cake.aspx?o_is=Hub_TopRecipe_3" ', '"http://allrecipes.co.uk/recipe/46217/halloween-spider-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/6544/white-chocolate-and-passion-fruit-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18901/double-chocolate-layer-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/12262/chocolate-mousse-cake-with-raspberry-filling.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/38366/chocolate-sponge-delicious-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/33086/chocolate-fudge-layer-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/46270/my-favourite-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/7396/easy-peasy-chocolate-fairy-cakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/39010/fairy-cakes-with-baileys-irish-cream---chocolate-chips-.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/44650/monster-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/479/no-bake-white-chocolate-cheesecake.aspx?o_is=Hub_TopRecipe_2" ', '"http://allrecipes.co.uk/recipe/39908/gluten-free-dark-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/9495/gluten-free-chocolate-cake-with-dark-chocolate-icing.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/10590/easiest-chocolate-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/17062/chocolate-olive-oil-cake.aspx?o_is=Hub_TopRecipe_1" ', '"http://allrecipes.co.uk/recipe/18038/oaty-banana-chocolate-chip-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/6039/choco-nut-decadence-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/42908/gluten-free-chocolate-and-polenta-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/37535/pear-and-chocolate-chip-loaf-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/34990/supreme-chocolate-fridge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/44665/chocolate-cupcakes-with-halloween-toppers.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/6135/black-magic-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/21824/strawberry-chocolate-mousse-cake.aspx?o_is=Hub_TopRecipe_3" ', '"http://allrecipes.co.uk/recipe/19292/sinful-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/42515/nutty-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8117/choco-coco-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/32166/double-chocolate-sponge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4775/one-bowl-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/11336/boozy-chocolate-sponge-cake.aspx?o_is=Hub_TopRecipe_5" ', '"http://allrecipes.co.uk/recipe/35803/moist-chocolate-chunk-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/41621/chocolate-peanut-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/54527/molten-chocolate-lava-mini-cakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/50837/pandoro-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/19924/chocolate-fudge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/12047/ultimate-chocolate-and-hazelnut-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/19270/chocolate-orange-layer-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35622/vegan-and-gluten-free-cinnamon-hot-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/19712/chocolate-and-cherry-layer-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/25881/chilli-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/26341/banana-cake-with-dark-chocolate.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/45959/vegan-and-gluten-free-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/85/no-bake-chocolate-cheesecake.aspx?o_is=Hub_TopRecipe_2" ', '"http://allrecipes.co.uk/recipe/27020/chocolate-cherry-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/11336/boozy-chocolate-sponge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/16906/super-easy-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/9400/no-bake-chocolate-and-chestnut-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/20760/rita-s-chocolate-fudge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/40845/chocolate-dream-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/51029/op-ra--french-chocolate-sponge-cake-.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/32183/fudgy-flourless-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/537/gooey-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/22351/rich-flourless-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/46898/chocolate-cake-with-oil.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/2223/basic-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/7117/white-chocolate-cheesecake-with-blueberry-sauce.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/50087/chocolate-cake-with-mascarpone-filling.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/19131/one-tin-chocolate-chip-cake.aspx?o_is=Hub_TopRecipe_5" ', '"http://allrecipes.co.uk/recipe/34497/blueberry-white-chocolate-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/19993/chocolate-chestnut-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/39895/gluten-free-karleksmums-cake--large---spiced-chocolate-fondant-.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/25153/always-perfect-chocolate-sponge-cake.aspx?o_is=Hub_TopRecipe_1" ', '"http://allrecipes.co.uk/recipe/31637/vanilla-and-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/25877/chocolate-sponge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4507/baileys-reg--chocolate-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/32581/easy-moist-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18402/buttermilk-chocolate-cake-with-chocolate-fudge-icing.aspx?o_is=Hub_TopRecipe_4" ', '"http://allrecipes.co.uk/recipe/31794/guinness--chocolate-cupcakes-with-baileys--icing.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/50401/simple-microwave-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/38706/gluten-free-and-dairy-free-chocolate-chiffon-sponge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8847/lily-vanilli-s-dark-chocolate-and-avocado-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18842/chocolate-mousse-sponge-finger-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/30995/delicous-chocolate-cupcakes-with-vanilla-frosting.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/28231/white-and-dark-chocolate-pistachio-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/29064/yoghurt-and-chocolate-chip-loaf-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/6221/fategg-s-far-too-chocolalatey-cake-.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/12927/easy-moist-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/40894/orange---dark-chocolate-chip-ring-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/37828/chocolate-oreo-reg--cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/695/berry-white-chocolate-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/16730/death-by-chocolate-cake.aspx?o_is=Hub_TopRecipe_3" ', '"http://allrecipes.co.uk/recipe/46992/chocolate-buttermilk-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/19263/rum-and-chocolate-mousse-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18014/banana-chocolate-chip-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/38801/chocolate-cake-in-a-mug.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18012/chocolate-chip-banana-cake.aspx?o_is=Hub_TopRecipe_2" ', '"http://allrecipes.co.uk/recipe/37302/gluten-free-chocolate-raspberry-cream-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/33845/12-gorgeous-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/37470/toasted-hazelnut-and-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/41065/gluten-free-chocolate-quinoa-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35179/easiest-one-bowl-banana-and-chocolate-chip-loaf-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4956/easy-flourless-chocolate-cake.aspx?o_is=Hub_TopRecipe_3" ', '"http://allrecipes.co.uk/recipe/35433/vegan-chocolate-fudge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/44968/ferrero-rocher--chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/10588/baileys-chocolate-fudge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/25734/easy-white-chocolate-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/34331/deluxe-chocolate-fudge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18836/chocolate-fudge-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/18855/chocolate-coffee-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/37814/priscilla-s-chocolate-hedgehog-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/6196/guinness-reg--and-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/32632/gluten-free-triple-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/34762/chocolate-orange-tunis-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/17106/rich-chocolate-cup-cakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/34922/chocolatey-biscuit-fridge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35320/easy-chocolate-sandwich-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/29066/chocolate-coffee-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/20783/one-bowl-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/46105/mini-vanilla-cheesecakes-with-chocolate-ganache.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/25945/chocolate-bar-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/46946/red-wine-chocolate-pound-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/12476/chocolate-cake-torte.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/19245/chocolate-cake-with-cream-cheese-icing.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/45226/white-chocolate-and-green-tea-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/28077/prague-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/43732/scrumchus-chocolate-mug-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/19380/easy-egg-free-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8796/carnation-chocolate-fudge-cake.aspx?o_is=Hub_TopRecipe_5" ', '"http://allrecipes.co.uk/recipe/50958/vegan-chocolate-and-raisin-fridge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/35311/chocolate-ganache-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/5048/carrot-cupcakes-with-white-chocolate-cream-cheese-icing.aspx?o_is=Hub_TopRecipe_3" ', '"http://allrecipes.co.uk/recipe/8420/1-bowl-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/50870/gluten-free--sugar-free-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/29388/chocolate-finger-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/50991/chocolate-banana-oat-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/23391/chocolate-orange-fondant-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/9398/chocolate-and-hazelnut-meringue-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/24811/chocolate-melt-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/24487/yummy-white-chocolate-cheesecake.aspx?o_is=Hub_TopRecipe_4" ', '"http://allrecipes.co.uk/recipe/14879/pumpkin-and-chocolate-chip-loaf-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/50714/chocolate-chip-pound-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/46791/vegan-halloween-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/23436/apple-and-chocolate-chip-loaf-cake.aspx?o_is=Hub_TopRecipe_4" ', '"http://allrecipes.co.uk/recipe/47004/chocolate-sponge-loaf-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/45540/my-chocolate-orange-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/25093/really-simple-chocolate-sponge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/25517/indulgent-6-minute-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/16272/raw-chocolate-cheesecake.aspx?o_is=Hub_TopRecipe_4" ', '"http://allrecipes.co.uk/recipe/684/flourless-chocolate-cake.aspx?o_is=Hub_TopRecipe_3" ', '"http://allrecipes.co.uk/recipe/12575/chocolate-curry-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/32051/two-minute-chocolate-microwave-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/44657/sticky--gooey--yummy-chocolate-and-fudge-cupcakes---.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/124/easy-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/20121/chocolate-layer-refrigerator-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/47386/chocolate-and-banana-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/27497/chocolate-mars-reg--bar-crispy-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/23640/eggless-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/39248/chocolate-carrot-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/4666/vegan-chocolate-cake.aspx?o_is=Hub_TopRecipe_3" ', '"http://allrecipes.co.uk/recipe/4676/chocolate-fairy-cakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/10573/basic-chocolate-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/32874/triple-chocolate-fridge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/29876/chocolate-biscuit-fridge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/23965/slow-cooker-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/21577/chocolate-and-coffee-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/19805/two-layer-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/22295/warm-flourless-chocolate-cake-with-caramel-sauce.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/32360/blueberry-and-white-chocolate-loaf-cake-with-lemon-drizzle.aspx?o_is=Hub_TopRecipe_5" ', '"http://allrecipes.co.uk/recipe/12367/flourless-french-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/6464/hugh-fearnley-whitingstall-s-chestnut-and-chocolate-truffle-cake.aspx?o_is=Hub_TopRecipe_5" ', '"http://allrecipes.co.uk/recipe/27808/chocolate-cupcakes.aspx?o_is=Hub_TopRecipe_2" ', '"http://allrecipes.co.uk/recipe/8427/chocolate-raspberry-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/25836/steph-s-white-chocolate-and-ginger-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/31728/orange-and-chocolate-cake.aspx?o_is=Hub_TopRecipe_2" ', '"http://allrecipes.co.uk/recipe/18810/chocolate-tiffin-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/10576/chocolate-cheesecake-brownies.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/25876/pear-and-chocolate-upside-down-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/13039/no-bake-chocolate-cupcakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8424/chocolate-cake-with-chocolate-buttercream.aspx?o_is=Hub_TopRecipe_1" ', '"http://allrecipes.co.uk/recipe/34901/easter-chocolate-fudge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8547/never-fail-chocolate-mousse-cake.aspx?o_is=Hub_TopRecipe_2" ', '"http://allrecipes.co.uk/recipe/553/chocolate-fudge-beetroot-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/46445/chocolate-cake-in-the-microwave.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/23280/chocolate-cupcakes-with-nutella-icing.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/31739/milky-bar-cheesecake--white-chocolate-cheesecake-.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/25747/extra-chocolaty-vegan-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/19576/delicious-gluten-free-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/42313/chocolate-christmas-giant-brownie-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/29683/chocolate-sandwich-cake-with-chocolate-buttercream.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/16272/raw-chocolate-cheesecake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8341/rum-mocha-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/17897/simple-chocolate-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/27306/mini-chocolate-orange-cakes.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/8543/gorgeous-chocolate-mousse-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/11385/banana-cream-chocolate-sponge-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/17648/easy-chocolate-chip-cake.aspx?o_is=LV" ', '"http://allrecipes.co.uk/recipe/46274/gluten-free-chocolate-almond-cake.aspx?o_is=LV" ']
print(main_function(new_links_list))

































# print(len(a))
# print(a)