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
#--------------------------------------------------------------------------------------- home page to state wise
state_list = []
ids = driver.find_elements("class name",'rtcBack')
print("State List :")
state_data = [ "s.No", "state name"]
print(state_data[0])
state_list.append(state_data)
coun = 0;
for ii in ids:
    coun = coun + 1     
    idsa = ii.find_elements("tag name", 'li')
    print(str(coun),".",ii.find_element("class name",'rtcName').text)
    state_data = [ str(coun), ii.find_element("class name",'rtcName').text]
    state_list.append(state_data)
    print(state_list[coun])

state_No = input("Please enter an STATE No: ")
selected_state = state_list[int(state_No)][1]
print("Selected state : ",state_list[int(state_No) - 1][1])
print("Route List :")
elem = driver.find_element("xpath",'//*[@id="Carousel"]/div['+state_No+']')
action = ActionChains(driver)
action.move_to_element(elem).click().perform() 
sleep(5)

#--------------------------------------------------------------------------------------page



page_div = driver.find_element("class name",'DC_117_paginationTable')
pages = page_div.find_elements("tag name",'div')

route_list_data = []
route_data = ["route link", "route Name","no of busses"]
route_list_data.append(route_data)
coun = 1
for pageno in pages:    
    print("lit of routes in page :",pageno.text)       
    action = ActionChains(driver)
    action.move_to_element(pageno).click().perform() 
    sleep(3)   
    ids = driver.find_elements("class name",'route_link')    
    for route_box in ids:          
        linktext = ''+ route_box.find_element("tag name",'a').text        
        pglink = route_box.find_element("tag name",'a').get_attribute('href')        
        buscount = route_box.find_element("class name",'totalRoutes').text
        print(str(coun)," . :", linktext," : ",route_box.find_element("tag name",'a').get_attribute('href')," No of Buses: ",buscount)
        route_data = [str(coun),route_box.find_element("tag name",'a').get_attribute('href'), linktext,buscount]
        route_list_data.append(route_data)        
        coun = coun + 1
        
route_no = input("Please enter an Route No: ")
selected_route = route_list_data[int(route_no) ][2]
selected_route_link = route_list_data[int(route_no)][1]
print("Selected state : ",route_list_data[int(route_no)][2]," : ", selected_route_link)
       

#--------------------------------------------------------------------------------------Loading data page
driver.get(selected_route_link)
sleep(10)
#---------------------------------------------------------------------------------------button clikc events
govt_data = driver.find_elements("class name",'group-data')
count = len(govt_data)
while(count):                
   print("button click-2")
   element = driver.find_element("xpath",'//*[@id="result-section"]/div['+str(count)+']/div/div[2]/div/div[4]/div[2]').click()
   count = count - 1
   sleep(3)
count = len(govt_data)



#--------------------------------------------------------------------------------------- Scroll down to the bottom of the page
last_height = driver.execute_script("return document.body.scrollHeight")
print("last_height: ",last_height)
pag  = 0
while True:
    if(pag >1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    pag = pag + 1
    print("last_height: ",last_height,pag )
    sleep(2)

#---------------------------------------------------------------------------------------open all ameeteies blok in page
amities = driver.find_elements("class name",'amenities-ul')   #//*[@id="14289108"]/div/div[2]/div[2]/div[2]/div/ul
for elem in amities :
   action = ActionChains(driver) 
   action.move_to_element(elem).click().perform() 
   sleep(1)

   
#---------------------------------------------------------------------------------------list of bus owners and there bus in bus-items class
inp_date = driver.find_elements("class name", 'bus-items')
count = int(len(inp_date))
print("no of UL",str(len(inp_date)),str(count))
#--------------------------------------------------------------------------------------- go to start home page
driver.find_element("tag name",'body').send_keys(Keys.CONTROL + Keys.HOME)
global bus_owners
bus_counts = 0;
total_bus_counts = 0;
for driversss in inp_date :
   li_list = driversss.find_elements("tag name", 'li')
   
   print ("-------------------------------------------------------------------------------------------------------------------------",str(count))
   if(int(count) <= 1):
      bus_owners = "private"
      print(str(count),bus_owners)
   else:
      bus_owners  = "Govt"
      print(str(count),bus_owners)
   print ("--------------------------------------------------------------",str(count),bus_owners,"------------------------------------------------")   
   print("no of UL",str(len(inp_date)),str(count),bus_owners)
   
   bus_counts = 0       
   for Li_bus in li_list:
      if((str(Li_bus.get_attribute('id')) != "") and (str(Li_bus.get_attribute('id')).isnumeric())):
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
                  print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",Li_bus.get_attribute('id'))                            
                  Li_bus_div_s = Li_bus.find_elements("class name", 'row-one')                            
                  for Li_bus_div in Li_bus_div_s:
                     ids_div_inner = Li_bus_div.find_elements("tag name", 'div')                                
                     for dd_inner in ids_div_inner:                                  
                           clss_valid =  dd_inner.get_attribute("class")
                           if (clss_valid.find('column') == -1):
                              clss_valids = clss_valid.split()
                              dict[clss_valids[0]] = dd_inner.text
                     
                  amenlist_ul = Li_bus.find_element("xpath",'//*[@id="'+dict["tripId"]+'"]/div/div[2]/div[2]/div[2]')
                  amenlist_li_s = amenlist_ul.find_elements("tag name",'li')
                  amities_data = ""
                  for amenlist_li in amenlist_li_s:
                      print("----",amenlist_li.text)
                      amities_data = amities_data + "," + amenlist_li.text
                      dict["amities"] = amities_data
                  print (amities_data)
                  print (dict)                     
                  sql = "INSERT INTO bus_details (trip_id, bus_owner,states,route_name,route_link,busname,bustype,departing_time,departing_loc,duration,reaching_time,reaching_loc,next_day,seats_available,seats_window,old_price,price,star_rating,no_pplaa,deals_new,amities) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                  val = (dict["tripId"],bus_owners,dict["state"],dict["route_name"],dict["route_link"],dict["travels"],dict["bus-type"],dict["dp-time"],dict["dp-loc"],dict["dur"],dict["bp-time"],dict["bp-loc"],dict["next-day-dp-lbl"],dict["seat-left"],dict["window-left"],dict["oldFare"],dict["fare"],dict["rating-sec"],dict["no-ppl"],dict["reddeals-sec"],dict["amities"])
                  print(sql)
                  print(val)
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
print (" moving to home Page")
sleep(5)
driver.back()

   


   
 
