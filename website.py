import os

vc_pages = ["STOXX", "FTSE", "CAC", "DAX"]
l_pages  = ["France", "Germany", "Italy"]


vc_links = ["            <a href=\"/php/if/fm/GCM_files/LiquidityAndCorr/{}.php\">{}</a>,  \n".format(
    page.replace(" ", ""), page) for page in vc_pages]
vc_links[-1] = vc_links[-1][:-4] # Remove floating comma
l_links  = ["            <a href=\"/php/if/fm/GCM_files/LiquidityAndCorr/{}.php\">{}</a>,  \n".format(
    page.replace(" ", ""), page) for page in l_pages]
l_links[-1] = l_links[-1][:-4] # Remove floating comma


def make_page(graphs, page_name):
    os.chdir("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/")
    scripts = ["        <?php include(\"{}_script.html\"); ?>\n".format(
            graph) for graph in graphs]
    divs = ["        <?php include(\"{}_div.html\"); ?>\n".format(
            graph) for graph in graphs]
    with open("template.html", 'r') as page:
        page_str = "".join(page.read())
        page_str = page_str.replace("PAGE_TITLE", page_name)
        page_str = page_str.replace("PAGE_SCRIPTS", "".join(scripts))
        page_str = page_str.replace("PAGE_DIVS", "".join(divs))
        page_str = page_str.replace("VC_LINKS", "".join(vc_links))
        page_str = page_str.replace("L_LINKS", "".join(l_links))

    with open(page_name.replace(" ", "")+".php", 'w') as page:
        page.write(page_str)

def make_index():
    os.chdir("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/")
    with open("template.html", 'r') as page:
        page_str = "".join(page.read())
        page_str = page_str.replace("PAGE_TITLE", "Charts")
        page_str = page_str.replace("PAGE_SCRIPTS", "")
        page_str = page_str.replace("PAGE_DIVS", "")
        page_str = page_str.replace("VC_LINKS", "".join(vc_links))
        page_str = page_str.replace("L_LINKS", "".join(l_links))

    with open("INDEX.php", 'w') as page:
        page.write(page_str)

make_index()

for page in vc_pages:
    # Var and Cor pages
    if page == "STOXX":
        graphs = ["STOXX_summary", "STOXX_CallsOverPuts"] 
    elif page == "FTSE":
        graphs = ["FTSE_summary", "FTSE_CallsOverPuts"] 
    elif page == "CAC":
        graphs = ["CAC_summary", "CAC_CallsOverPuts"]
    elif page == "DAX":
        graphs = ["DAX_summary", "DAX_CallsOverPuts"]
    else:
        print page
    make_page(graphs, page)

for country in l_pages:
    # Liquidity pages
    if country == "France":
        graphs = ["tenor10countryFR", "tenor2countryFR", 
                    "tenor10countryFRvarsBID_ASKROUNDTRIP",
                    "tenor2countryFRvarsBID_ASKROUNDTRIP"]
    elif country == "Germany":
        graphs = ["tenor10countryDE", "tenor2countryDE"
                    "tenor10countryDEvarsBID_ASKROUNDTRIP",
                    "tenor2countryDEvarsBID_ASKROUNDTRIP"]
    elif country == "Italy":
        graphs = ["tenor10countryIT", "tenor2countryIT",
                    "tenor10countryITvarsBID_ASKROUNDTRIP",
                    "tenor2countryITvarsBID_ASKROUNDTRIP"]
    else:
        print country
    make_page(graphs, country)



