# For the purposes of this code
# https://www.collegestudentapartments.com/college/university-of-virginia-charlottesville-virginia/apartments/ was the
# website used to scrap the appt info
import csv
import re
#creates raw html data code string
def ScrapHtmlCode(website):
    from lxml import html
    from lxml.etree import tostring
    import requests
    # request website
    page = requests.get(website)
    # make tree out html code
    tree = html.fromstring(page.content)
    import html
    # return byte string of tree
    return (str(tostring(tree)))
#takes html code with website links on it and puts them in a set
def getwebsites(HtmlCode):
    # take html code split and strip
    code = HtmlCode.strip().split('  ')
    # empty set of appts
    appts = set()
    # for elements in code
    for ele in code:
        # find all websites that are properties and put it into a set
        pattern = re.compile('https:[^"]*', )
        allmatches = set(pattern.findall(ele))
        for match in allmatches:
            if ('collegestudentapartments.com/property' in match):
                # if match add to appts
                appts.add(match)
    return (appts)

def getinfo(webpage):
    # A dict of dicts
    # {Appt Title{Title:X, Adress:Y, Number:(ZZZ) YYY-XXXX , Distance:Z, Description:W, Units{}},{Appt Title2{ Title:X, Adress:Y...}}
    apptinfo={}
    # take link out of all links
    for link in getwebsites(webpage):
        # take html from each link, which are the sites individual pages
        info = (ScrapHtmlCode(link))

        # get title
        pattern = re.compile('title>([^|]*) UVA')
        match = pattern.search(info)
        title=match.group(1)
        apptinfo[match.group(1)]={"Title":match.group(1)}

        # group 1 adress, group 2 city, group 3 postal code
        pattern = re.compile('streetAddress">(.*)<\/span>, <span itemprop="addressLocality">([^<]*)<\/.*postalCode">([\d]+)')
        match = pattern.search(info)
        apptinfo[title]["Address"]=match.group(1)+", "+match.group(2)+ ", VA "+match.group(3)

        # get appt telephone number
        pattern = re.compile('\([\d]+\) [\d]+-\d+')
        match = pattern.search(info)
        # If cant find number it will be null
        try:
            apptinfo[title]["Number"]=match.group(0)
        except:
            apptinfo[title]["Number"] = "---"

        # What is the distance from grounds
        try:
            pattern = re.compile('(\d*.\d*||\d*)<\/span> Miles From Campus')
            match = pattern.search(info)
            apptinfo[title]["Distance"]=match.group(1).strip(">")+" miles from Grounds"
        except:
            apptinfo[title]["Distance"] = "---"

        # Description of appt
        try:
            pattern = re.compile('og:description" content="([^"]*)')
            match = pattern.search(info)
            apptinfo[title]["Description"]=match.group(1)
        except:
            apptinfo[title]["Description"] = "---"

        #This is gonna be pretty difficult to follow
        #gonna basically put another dict of dicts in the dict :(
        # Units{untit name{Title:X,beds:Y,:Size:Z, Prince:W}}

        pattern = re.compile('class="rentalGridRow([^;]*)')
        match = pattern.findall(info)
        for unit in match:
            try:
                # Get the unit name and put in front of dict and in the title spot
                pattern = re.compile('name.{0,11}>([^<]*)')
                Umatch = pattern.search(unit)
                apptinfo[title]["Units"] = {Umatch.group(1):{"Title":Umatch.group(1)}}
                Unit=Umatch.group(1)
                if Unit=='':
                    apptinfo[title]["Units"] = {"Untitled": {"Title": "Untitled"}}
                    Unit = "Untitled"
            except:
                # If cant find unit name put untitled
                apptinfo[title]["Units"] = {"Untitled": {"Title": "Untitled"}}
                Unit="Untitled"
            try:
                # Find number of beds
                pattern = re.compile('beds.*longText">(\d)')
                match = pattern.search(unit)
                apptinfo[title]["Units"][Unit]["Beds"] = match.group(1)
            except:
                # Cant find anything put null
                apptinfo[title]["Units"][Unit]["Beds"] = "---"
            try:
                # Find number of baths
                pattern = re.compile('baths.*longText">(\d)')
                match = pattern.search(unit)
                apptinfo[title]["Units"][Unit]["Baths"] = match.group(1)
            except:
                # Cant find anything put null
                apptinfo[title]["Units"][Unit]["Baths"] = "---"
            try:
                # Find the size of the unit
                pattern = re.compile('sqft">([^<]*)')
                match = pattern.search(unit)
                apptinfo[title]["Units"][Unit]["Size"] = match.group(1)
            except:
                # Cant find anything put null
                apptinfo[title]["Units"][Unit]["Size"] = "---"
            try:
                # Find the price of the individual unit
                pattern = re.compile('rent">([^<]*)')
                match = pattern.search(unit)
                apptinfo[title]["Units"][Unit]["Price"] = match.group(1)
            except:
                # Cant find anything put null
                apptinfo[title]["Units"][Unit]["Price"] = "---"
        # apptinfo[title]["Description"]=match.group(1)
    return(apptinfo)
# Take in two parameters which are dicts of info and create a csv listing the info in the dict
def writecsv(first, second):
    with open('apartment_data.csv', 'w') as csvfile:
        # Titles of the the csv
        fieldnames = ['Apartment Name', 'Company', 'Location', 'Price', 'Size', 'Bedrooms', 'Furnished', 'Pets',
                      'Bathrooms', 'Description', 'Number', 'Distance to Grounds']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # Accomadations need to made later to take in account for the units. For now I just took the first unit size, price, beds and baths
        # First is the first dict of the info on the page
        for appt in first.values():
            writer.writerow(
                {'Apartment Name': appt['Title'], 'Company': '---', 'Location': appt['Address'],
                 'Price': appt['Units'][(list(appt['Units'])[0])]['Price'],
                 'Size': appt['Units'][(list(appt['Units'])[0])]['Size'],
                 'Bedrooms': appt['Units'][(list(appt['Units'])[0])]['Beds'], 'Furnished': '---', 'Pets': '---',
                 'Bathrooms': appt['Units'][(list(appt['Units'])[0])]['Baths'],
                 'Description': appt['Description'], 'Number': appt['Number'], 'Distance to Grounds': appt['Distance']})
        # second is the second dict of info on the page
        for appt in second.values():
            writer.writerow(
                {'Apartment Name': appt['Title'], 'Company': '---', 'Location': appt['Address'],
                 'Price': appt['Units'][(list(appt['Units'])[0])]['Price'],
                 'Size': appt['Units'][(list(appt['Units'])[0])]['Size'],
                 'Bedrooms': appt['Units'][(list(appt['Units'])[0])]['Beds'], 'Furnished': '---', 'Pets': '---',
                 'Bathrooms': appt['Units'][(list(appt['Units'])[0])]['Baths'],
                 'Description': appt['Description'], 'Number': appt['Number'], 'Distance to Grounds': appt['Distance']})
    return None

# Get all the links and appt titles from both pages from this website
firstpage=(ScrapHtmlCode('https://www.collegestudentapartments.com/college/university-of-virginia-charlottesville-virginia/apartments/'))
secondpage=(ScrapHtmlCode('https://www.collegestudentapartments.com/college/university-of-virginia-charlottesville-virginia/apartments/?page=2'))
# Get a dict of all info from the html links from the first and second page
first_page_appt_info= (getinfo(firstpage))
second_page_appt_info= (getinfo(secondpage))
# Write CSV from the info in the first and second page
writecsv(first_page_appt_info,second_page_appt_info)