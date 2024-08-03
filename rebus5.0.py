"""
Redbus scraping using python and selenium
this code will scrap the buses of a given city to city.
1. initallly i will read the list of states in resbus.in and get the state id to get the routes
2. get list of all routes in the state by reading each pages and then get the route id to get the busess
3. this part read the govt bus and private bus list with all ameties listed and store in DB
4. afte compeleting the details page will back to homae page for next scaraping

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 
from time import sleep
import pandas as pd
import mysql.connector
from mysql import connector
import warnings
warnings.filterwarnings('ignore')

service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.redbus.in")
sleep(5)
mydb = mysql.connector.connect(
                  host=" 127.0.0.1",
                  user="root",
                  password="",
                  database="redbus"
        )
mycursor = mydb.cursor()


elem_keys = { 'st_list': {"fmt": 'class name', "emt": 'rtcBack'},
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


state_data_list = []
route_data_list = []
selected_state = ""
selected_state = ""
selected_route = ""
selected_route_link  = ""
#--------------------------------------------------------------------------------------- selenium events -----------------------------------------------------#

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

"""
#-------------------------------------------------------------Get List of all states---------------------------------------------------------------------
              'st_list': {"format": 'class name', "element": 'rtcBack'}  Every state is under the class name rtcback
              'st_list_div': {"fmt": 'class name', "emt": 'rtcName'}    inside rtcback we get name of that state in rtcname class
              after reading each data from the rtcback and rtc name then stored in a state_data_list
                  
"""
def get_state_list():
    try: 
        global state_data_list
        print("State List :")
        state_div_s = find_elem_s(driver,elem_keys['st_list']) 
        state_data = [ "s.No", "state name"]    
        state_data_list.append(state_data)
        state_count = 0;
        for state_div in state_div_s:
            state_count = state_count + 1
            state_name =  find_elem_one(state_div,
                                        elem_keys['st_list_div']).text  
            print(str(state_count),".",state_name)
            state_data = [ str(state_count), state_name]
            state_data_list.append(state_data)
        print("Total_states", len(state_data_list)-1)
    except:
        print("error in statelist")
#----------------------------------------------Get user input of state number-----------------------------------------------    
def select_state():
    global state_list, selected_state
    state_No = input("Please enter a STATE No: ")
    return state_No
"""-------------------------------------------------------click event for state div------------------------------------------
            'st_div': {"fmt": 'xpath', "emt": '//*[@id="Carousel"]/div[<value>]'},   using xpath we find the carousel div of selected input, open the
            link by link_click function. xpath is same for all states and only the "div" numbers is changes
"""
              
def open_routes_page(state_No):
    try:
        selected_state = state_data_list[int(state_No)][1]
        print("Selected state : ",selected_state)   
        elem = find_elem_one_replace(driver,elem_keys['st_div'],state_No)
        link_click(driver, elem, 5)
    except:
        print("error in open routes page")
    

#------------------------------------------------------------Route list page---------------------------------------------------------
"""
        after loading of route list page we can see 10 routes per page
              'route_page_div': {"fmt": 'class name', "emt": 'DC_117_paginationTable'},   pagination link are placed in a main div of dc_117_pagination  
              'route_page_no': {"fmt": 'tag name', "emt": 'div'},       after reading the pagination div we take each page link and pag number
              'route_div': {"fmt": 'class name', "emt": 'route_link'},   each route is under a calss name route link 
              'route_link': {"fmt": 'tag name', "emt": 'a'},     we get get the anchor link details from each route_link class
              'route_bus_count': {"fmt": 'class name', "emt": 'totalRoutes'},  from each route _lik we also take no of buses in theat rout by reading totalroutes class
"""
              
def get_routes_list():
    try:
        global route_data_list
        print("Route List :")
        page_div = find_elem_one(driver,elem_keys['route_page_div'])   
        pages = find_elem_s(page_div,elem_keys['route_page_no'])
        route_data_list = []
        route_data = ["route link", "route Name","no of busses"]
        route_data_list.append(route_data)
        route_count = 1
        for pageno in pages:    
            print("lit of routes in page :",pageno.text)
            link_click(driver, pageno, 3)     
            route_boxs = find_elem_s(driver,
                                     elem_keys['route_div'])   
            for route_box in route_boxs:
                link_element = find_elem_one(route_box,
                                             elem_keys['route_link'])          
                linktext = ''+ link_element.text        
                pglink = link_element.get_attribute('href')        
                buscount = find_elem_one(route_box,
                                         elem_keys['route_bus_count']).text
                #print(str(route_count)," . : ", linktext," : ",pglink, ", No of Buses: ",buscount)
                route_data = [str(route_count),pglink,
                              linktext,buscount]
                route_data_list.append(route_data)        
                route_count = route_count + 1
        print("Total Routes :", len(route_data_list)-1)
    except:
        print("error in routes list")
#----------------------------------------------Get user input of route number-----------------------------------------------
            
def get_route_inp():
    count = 0
    for routes in route_data_list:
        if(count >= 1):
            print(routes[0]," . : ", routes[1]," : ",routes[2],
                  ", No of Buses: ",routes[3])
        count = count + 1
    
    route_no = input("Please enter an Route No: ")
    return route_no
    
       

#-------------------------------------------------------------Loading data page---------------------------------------------------------
"""
                    after geting user input we retrive the url from route_data_list and open the page in driver and wait for 10 sec
"""
def goto_bus_page(route_no):
    try:
        selected_route = route_data_list[int(route_no) ][2]
        selected_route_link = route_data_list[int(route_no)][1]
        print("Selected state : ",route_data_list[int(route_no)][2]," : ", selected_route_link)
        print("Pagw loading :",selected_route)
        driver.get(selected_route_link)
        sleep(10)
    except:
        print("error in goto bus page")




#--------------------------------------------------------------------button clikc events-----------------------------------------------
"""
                 govt_buses': {"fmt": 'class name', "emt": 'group-data'},  :    intially govt bus are hidden to open we use group-data class                 
              'govt_buses_button': {"fmt": 'xpath', "emt": '//*[@id="result-section"]/div[<value>]/div/div[2]/div/div[4]/div[2]'}
                    :   from group-data class we use xpath for find the button and click the button in reversal way to over come the page loding event 
              
"""
        
def opn_govt_bus_list():    
    govt_data = find_elem_s(driver, elem_keys['govt_buses'])
    count = len(govt_data)
    print("open govt bus datas:",count)
    while(count): 
       element = find_elem_one_replace( driver,elem_keys['govt_buses_button'],str(count)).click()
       count = count - 1
       sleep(3)
    



#--------------------------------------------------------------------------------------- Scroll down to the bottom of the page
def scroll_pages():
    last_height = driver.execute_script("return document.body.scrollHeight")
    print("Page scolling")
    pag  = 0
    while True:
        if(pag >1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        pag = pag + 1
        #print("last_height: ",last_height,pag )
        sleep(2)
    driver.find_element("tag name",'body').send_keys(Keys.CONTROL + Keys.HOME)
    
#---------------------------------------------------------------------------------------open all ameeteies blok in page
"""
    'amenites_ul': {"fmt": 'class name', "emt": 'amenities-ul'}, using class name amenities-ul we can explore all amenities of bus, so that we can pull the datas 
"""              
def open_amentes():
    amities = find_elem_s(driver, elem_keys['amenites_ul'])
    print("open all amenities", len(amities))
    for elem in amities :
       action = ActionChains(driver) 
       action.move_to_element(elem).click().perform() 
       sleep(1)

#-------------------------------------------------------get bus datas and store in db----------------------
"""
              'bus_items_ul': {"fmt": 'class name', "emt": 'bus-items'},  each bus groups are under bus-items class ul
              'bus_delatisl_li': {"fmt": 'tag name', "emt": 'li'},  each bus deatils are under the Li tag each bus have a ID mentioning like travelid
              'bus_deltails_div': {"fmt": 'class name', "emt": 'row-one'},  each like have 3 rows and row one contains bus details
              'bus_delatisl_div': {"fmt": 'tag name', "emt": 'div'}, each data is enclosed under divs by readinf the div annd it attributes we get data and its variable
              'amenlist_ul_path': {"fmt": 'xpath', "emt": '//*[@id="<value>"]/div/div[2]/div[2]/div[2]'},   this will give us the amenites UL control    
              'amenlist_ul_li': {"fmt": 'tag name', "emt": 'li'}}    under the above xpath we can read each amnities in li
              after collectinf alldas with is class name ad data variable we stre it in dictonary for clasifiaction of data.
              clasifed data is passed to mysql query for savinf in table

"""
def get_bus_datas():
    #---------------------------------------------------------------------------------------list of bus owners and there bus in bus-items class
    bus_data_ULS = find_elem_s(driver, elem_keys['bus_items_ul'])       
    count = int(len(bus_data_ULS))
    print("no of UL",str(len(bus_data_ULS)),str(count))
    #--------------------------------------------------------------------------------------- go to start home page
    driver.find_element("tag name",'body').send_keys(Keys.CONTROL + Keys.HOME)
    global bus_owners
    bus_counts = 0;
    total_bus_counts = 0;
    for driversss in bus_data_ULS :
       li_list = find_elem_s(driversss, elem_keys['bus_delatisl_li'])    
       
       print ("-------------------------------------------------------------------------------------------------------------------------",str(count))
       if(int(count) <= 1):
          bus_owners = "private"
          print(str(count),bus_owners)
       else:
          bus_owners  = "Govt"
          print(str(count),bus_owners)
       print ("--------------------------------------------------------------",str(count),bus_owners,"------------------------------------------------")   
       
       
       bus_counts = 0       
       for Li_bus in li_list:
          if((str(Li_bus.get_attribute('id')) != "")
             and (str(Li_bus.get_attribute('id')).isnumeric())):
                      dict ={}
                      dict["state"]=selected_state
                      dict["route_name"]=selected_route
                      dict["route_link"]="dummy"
                      dict["gp"] = bus_owners
                      dict["next-day-dp-lbl"] = "none"
                      dict["oldFare"] = "0"
                      dict["no-ppl"] = "none"
                      dict["reddeals-sec"] = "none"
                      dict["window-left"] = "none"
                      dict["tripId"] = Li_bus.get_attribute('id')                  
                      dict["rating-sec"] = "none"
                      dict["amities"] = "none"
                      print("-----",Li_bus.get_attribute('id'))                            
                      Li_bus_div_s = find_elem_s(Li_bus,
                                                 elem_keys['bus_deltails_div'])                                 
                      for Li_bus_div in Li_bus_div_s:
                         ids_div_inner = find_elem_s(Li_bus_div,
                                                     elem_keys['bus_delatisl_div'])                                      
                         for dd_inner in ids_div_inner:                                  
                               clss_valid =  dd_inner.get_attribute("class")
                               if (clss_valid.find('column') == -1):
                                  clss_valids = clss_valid.split()
                                  dict[clss_valids[0]] = dd_inner.text
                         
                      amenlist_ul = find_elem_one_replace(Li_bus,
                                                        elem_keys['amenlist_ul_path'],dict["tripId"])                                                   
                      amenlist_li_s = find_elem_s(amenlist_ul,
                                                  elem_keys['amenlist_ul_li'])     
                      amities_data = ""
                      for amenlist_li in amenlist_li_s:                     
                          amities_data = amities_data + "," + amenlist_li.text
                          dict["amities"] = amities_data
                      #print (amities_data)
                      #print (dict)                     
                      sql = "INSERT INTO bus_details (trip_id, bus_owner,states,route_name,route_link,busname,bustype,departing_time,departing_loc,duration,reaching_time,reaching_loc,next_day,seats_available,seats_window,old_price,price,star_rating,no_pplaa,deals_new,amities) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                      val = (dict["tripId"],bus_owners,dict["state"],dict["route_name"],dict["route_link"],dict["travels"],dict["bus-type"],dict["dp-time"],dict["dp-loc"],dict["dur"],dict["bp-time"],dict["bp-loc"],dict["next-day-dp-lbl"],dict["seat-left"],dict["window-left"],dict["oldFare"],dict["fare"],dict["rating-sec"],dict["no-ppl"],dict["reddeals-sec"],dict["amities"])
                      #print(sql)
                      #print(val)
                      mycursor.execute(sql, val)
                      mydb.commit()
                      bus_counts =  bus_counts + 1
                      mylast_id = mycursor.lastrowid
                      print (str(mylast_id),val) 
       count = count  - 1                           
       print ("Owner :",bus_owners," total buses :",bus_counts)
       total_bus_counts = total_bus_counts + bus_counts
    print ("state :",dict["state"] ,"route :",dict["route_name"] ,"Total buses :",total_bus_counts)
    print (" moving to route List page")
    driver.back()
    sleep(5)
    driver.back()

#--------------------------------------------------main function----------------------------------
"""
        intially we load redbus.in home page in driver.get method. first we retrive states lited in home page. after navigating the state page we retrive
    route under the state. each page page contains 10 route details with name  and , number of buses, and minimum price , we retive name, link, number of buss.
    after user input we load the bus of route he/she selected and process the data.after competion of data collection page will automatically goes back to rout list page
    sleected state. User can collect another route buses or press - 0  to goto state(home page). Ether user can select next state and follow above procedures to collect
    the date, or press - 0  to exit the code.
"""
looping_main =1 
while(looping_main):
    get_state_list()
    state_No = select_state()
    if(state_No.isnumeric()
       and int(state_No) <= len(state_data_list)):
        if(int(state_No) != 0):
            open_routes_page(state_No)
            get_routes_list()
            looping_routes =1 
            while(looping_routes):
                route_no = get_route_inp()
                if(int(route_no) == 0):
                    print(" moving to home page")
                    driver.back()
                    sleep(5)
                    looping_routes = 0
                else:
                    goto_bus_page(route_no)
                    opn_govt_bus_list()
                    scroll_pages()
                    open_amentes()
                    get_bus_datas()
        else:
            print(" thank you scraping redbus datas")
            looping_main = 0
            break
        





   


   
 
