from bs4 import BeautifulSoup
import requests
import re
from time import sleep
import json
"""The code gets a link (from the british web) and print all the recipes links (in this case, chocolate cakes) """

url_main = "http://allrecipes.co.uk/recipes/tag-994/chocolate-cake-recipes.aspx?o_is=DH_1"


def get_html_from_link(link):
    """Gets a url link and return its web page """ # page with list of recipes
    url_text = requests.get(link).text
    html_page = BeautifulSoup(url_text, 'lxml')
    print("ddd", link)
    return html_page


def get_html_from_link2(link):
    """Gets a url link and return its web page """ # page with list of recipes
    print("now?")
    url_text = requests.get(link).text
    print("oooo")
    html_page = BeautifulSoup(url_text, 'lxml')
    print("ddd", link)
    return html_page


def get_url_links(url_main):
    """Gets a website address and returns a list for (chocolate cake) recipes by cakes type- each one has its own recipes list"""
    """(Returns pages of recipes by types)"""
    # html = get_html_from_link(url_main)
    links_mess = url_main.findAll('a', class_="hubPhoto")
    cakes_types_url_links = []
    for link1 in links_mess:
        x = str(link1).split("href=")
        y = x[1][1:]
        z = y.split("img")
        clean_link = z[0][:-4]
        cakes_types_url_links.append(clean_link)
    return cakes_types_url_links


def get_recipes_links(html_page):
    """gets a list of recipes from the same type and returns the links of
     recipes"""
    links = html_page.findAll('div', class_="col-sm-7")
    links_list_1_page = []
    for i in links:
        x = str(i).split("href=")
        y = x[1].split("itemprop")
        z = y[0]
        links_list_1_page.append(z)
    return links_list_1_page


def link_for_second_page(html_page_main):
    """gets a html_page, returnd the link for the second page"""
    butt = html_page_main.find('button', class_="showMore")
    x = str(butt).split("href=")
    print("x", x)
    try:
        y = x[1].split(">See all")
        z = y[0][1:-2]
    except:
        z = False
    return z


def link_for_next_page(html_page):
    next_b = html_page.find("a", class_="button pageNext")
    x = str(next_b).split("href=")
    y = x[1][:-4]
    return y


def find_first_page(main_html):
    next_b = main_html.find("a", class_="hubPhoto")
    x = str(next_b).split("href=")
    y = x[1]
    z = y.split(">")
    the_link = z[0][1:-1]
    # print(str(next_b))
    # print(main_html)
    print("there was a problem", the_link)
    return the_link
    #y = x[1][:-4]


def collect_htmls_for_pages_from_same_type(cake_type_link):
    """gets a link for type of cakes, returns all the pages as htmls"""
    # links_list = [cake_type_link] # first page link
    main_html = get_html_from_link(cake_type_link)
    second_page = link_for_second_page(main_html) # second page link
    while not second_page:
        cake_type_link = find_first_page(main_html)
        main_html = get_html_from_link(cake_type_link)
        second_page = link_for_second_page(main_html)

    second_page_html = get_html_from_link(second_page) # second page html
    links_list = [cake_type_link, second_page] # list of links with first and second pages links
    htmls_list = [main_html, second_page_html] # list of htmls(from the previous links list) with first and second html pages
    num_helper = 2
    number_pages = second_page_html.find("div", class_="pageCount").text # num of pages
    str_num = number_pages[4:]
    int_num = int(str_num)
    the_page = second_page_html
    while num_helper < int_num:
        sleep(1.5)
        the_link = link_for_next_page(the_page)[1:-1]
        the_page = get_html_from_link(the_link)
        links_list.append(the_link)
        htmls_list.append(the_page)
        num_helper += 1
    return htmls_list


# p2 = "http://allrecipes.co.uk/recipes/tag-6406/chocolate-sponge-cake-recipes.aspx?page=2"
# p3 = "http://allrecipes.co.uk/recipes/tag-6406/chocolate-sponge-cake-recipes.aspx?page=3&o_is=LV_Pgntn"
# #def get_link_second_page()
# link = "http://allrecipes.co.uk/recipes/tag-6406/chocolate-sponge-cake-recipes.aspx?o_is=DH_1"
#
# link2 = "http://allrecipes.co.uk/recipes/tag-3472/chocolate-cupcakes.aspx?o_is=DH_3"
# html_page_main = get_html_from_link(link2)
# get_recipes_links(html_page_main)
# link_for_next_page(html_page_main)

URL = "http://allrecipes.co.uk/recipes/tag-994/chocolate-cake-recipes.aspx?o_is=LV_BC"


def main_function(URL):
    url_html = get_html_from_link(URL) # מקבל את העמוד הראשון כHTML שבו קישורים לסוגי עוגות שוקולד שונים
    cakes_type_links = get_url_links(url_html) # מתוך העמוד מוציאים רשימת לינקים לסוגי עוגות - כל אחד מהם עמודים בפני עצמם
    all_recipes_links = []
    for cake_type in cakes_type_links:
        htmls_list = collect_htmls_for_pages_from_same_type(cake_type)
        for html in htmls_list:
            new_links = get_recipes_links(html)
            for new_link in new_links:
                all_recipes_links.append(new_link)
            #all_recipes_links.append(new_links)
    print(all_recipes_links)
    return all_recipes_links


main_function(URL)










# t_link = link_for_second_page(link)
# h_t= get_recipe_html_from_link(t_link)
# n_t = link_for_next_page(h_t)
# print(n_t)


#print(link_for_next_page(html_second))
#http://allrecipes.co.uk/recipes/tag-6406/chocolate-sponge-cake-recipes.aspx?page=2
#http://allrecipes.co.uk/recipes/tag-3107/fudge-cake-recipes.aspx?page=2