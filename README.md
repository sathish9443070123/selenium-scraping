# python selenium-scraping and display data uing streamlit.

Redbus scraping using python and selenium
this code will scrap the buses of a given city to city.
1. initallly i will read the list of states in resbus.in and get the state id to get the routes
2. get list of all routes in the state by reading each pages and then get the route id to get the busess
3. this part read the govt bus and private bus list with all ameties listed and store in DB
4. afte compeleting the details page will back to homae page for next scaraping

format and elements used to retrive data:
elem_keys = { 'st_list': {"fmt": 'class name', "emt": 'rtcBack'}

              'st_list_div': {"fmt": 'class name', "emt": 'rtcName'},
            
              'st_div': {"fmt": 'xpath', "emt": '//*[@id="Carousel"]/div[<value>]'},
              
              'route_page_div': {"fmt": 'class name', "emt": 'DC_117_paginationTable'}, 
              
              'route_page_no': {"fmt": 'tag name', "emt": 'div'},   
              'route_div': {"fmt": 'class name', "emt": 'route_link'},
              'route_link': {"fmt": 'tag name', "emt": 'a'},   
              'route_bus_count': {"fmt": 'class name', "emt": 'totalRoutes'},
              'govt_buses': {"fmt": 'class name', "emt": 'group-data'},
              'govt_buses_button': {"fmt": 'xpath', "emt": '//*[@id="result-section"]/div[<value>]/div/div[2]/div/div[4]/div[2]'},
              'amenites_ul': {"fmt": 'class name', "emt": 'amenities-ul'},
              'bus_items_ul': {"fmt": 'class name', "emt": 'bus-items'},
              'bus_delatisl_li': {"fmt": 'tag name', "emt": 'li'},
              'bus_deltails_div': {"fmt": 'class name', "emt": 'row-one'},
              'bus_delatisl_div': {"fmt": 'tag name', "emt": 'div'},
              'amenlist_ul_path': {"fmt": 'xpath', "emt": '//*[@id="<value>"]/div/div[2]/div[2]/div[2]'},    
              'amenlist_ul_li': {"fmt": 'tag name', "emt": 'li'}} 
flow of scraping

#--------------------------------------------------main function----------------------------------
"""
        intially we load redbus.in home page in driver.get method. first we retrive states lited in home page. after navigating the state page we retrive
    route under the state. each page page contains 10 route details with name  and , number of buses, and minimum price , we retive name, link, number of buss.
    after user input we load the bus of route he/she selected and process the data.after competion of data collection page will automatically goes back to rout list page
    sleected state. User can collect another route buses or press - 0  to goto state(home page). Ether user can select next state and follow above procedures to collect
    the date, or press - 0  to exit the code.
"""
def find_elem_s(contents,find_details):
    try:
        ids = contents.find_elements(find_details["fmt"],
                                     find_details["emt"])
    except:
        print("error in data (find_elem_s): ",find_details["fmt"],find_details["emt"])
    return ids

def find_elem_one(contents,find_details):
    try:
        ids = contents.find_element(find_details["fmt"],
                                     find_details["emt"])
    except:
        print("error in data (find_elem_one): ",find_details["fmt"],find_details["emt"])
    return ids

def find_elem_one_replace(contents,find_details,rp_char):
    try:        
        ids = contents.find_element(find_details["fmt"], find_details["emt"].replace('<value>',rp_char))
    except:
        print("error in data (find_elem_one_replace)", find_details["fmt"],find_details["emt"])
    return ids

def link_click(contents,elem_click,sleep_time):
    try:        
        action = ActionChains(contents)
        action.move_to_element(elem_click).click().perform() 
        sleep(sleep_time)
    except:
        print("error in click event")
        
    get_state_list()  
          gets state list from home page  using 'st_list', 'st_list_div' 
    state_No = select_state()   
          click the state box 'st_div': {"fmt": 'xpath', "emt": '//*[@id="Carousel"]/div[<value>]'},
    open_routes_page(state_No)   
          st_div': {"fmt": 'xpath', "emt": '//*[@id="Carousel"]/div[<value>]'},   using xpath we find the carousel div of selected input, open the
          link by link_click function. xpath is same for all states and only the "div" numbers is changes
    get_routes_list()
          after loading of route list page we can see 10 routes per page
              'route_page_div': {"fmt": 'class name', "emt": 'DC_117_paginationTable'},   pagination link are placed in a main div of dc_117_pagination  
              'route_page_no': {"fmt": 'tag name', "emt": 'div'},       after reading the pagination div we take each page link and pag number
              'route_div': {"fmt": 'class name', "emt": 'route_link'},   each route is under a calss name route link 
              'route_link': {"fmt": 'tag name', "emt": 'a'},     we get get the anchor link details from each route_link class
              'route_bus_count': {"fmt": 'class name', "emt": 'totalRoutes'},  from each route _lik we also take no of buses in theat rout by reading totalroutes class

    route_no = get_route_inp()
    goto_bus_page(route_no)
          after geting user input we retrive the url from route_data_list and open the page in driver and wait for 10 sec
    opn_govt_bus_list()
          govt_buses': {"fmt": 'class name', "emt": 'group-data'},  :    intially govt bus are hidden to open we use group-data class                 
          'govt_buses_button': {"fmt": 'xpath', "emt": '//*[@id="result-section"]/div[<value>]/div/div[2]/div/div[4]/div[2]'}
          from group-data class we use xpath for find the button and click the button in reversal way to over come the page loding event 
    scroll_pages()
    open_amentes()
          'amenites_ul': {"fmt": 'class name', "emt": 'amenities-ul'}, using class name amenities-ul we can explore all amenities of bus, so that we can pull the datas 
    get_bus_datas()
              'bus_items_ul': {"fmt": 'class name', "emt": 'bus-items'},  each bus groups are under bus-items class ul
              'bus_delatisl_li': {"fmt": 'tag name', "emt": 'li'},  each bus deatils are under the Li tag each bus have a ID mentioning like travelid
              'bus_deltails_div': {"fmt": 'class name', "emt": 'row-one'},  each like have 3 rows and row one contains bus details
              'bus_delatisl_div': {"fmt": 'tag name', "emt": 'div'}, each data is enclosed under divs by readinf the div annd it attributes we get data and its variable
              'amenlist_ul_path': {"fmt": 'xpath', "emt": '//*[@id="<value>"]/div/div[2]/div[2]/div[2]'},   this will give us the amenites UL control    
              'amenlist_ul_li': {"fmt": 'tag name', "emt": 'li'}}    under the above xpath we can read each amnities in li
              after collectinf alldas with is class name ad data variable we stre it in dictonary for clasifiaction of data.
              clasifed data is passed to mysql query for savinf in table
     
            

