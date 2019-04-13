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
            pattern = re.compile('itemprop="description">([^<]*)')
            match = pattern.search(info)
            apptinfo[title]["Description"]=match.group(1)
        except:
            apptinfo[title]["Description"] = "---"
        #     Get image of appt
        try:
            pattern = re.compile('og:image" content="([^"]*)')
            match = pattern.search(info)
            apptinfo[title]["Image"]=match.group(1)
        except:
            apptinfo[title]["Image"] = "---"
        #This is gonna be pretty difficult to follow
        #gonna basically put another dict of dicts in the dict :(
        # Units{untit name{Title:X,beds:Y,:Size:Z, Prince:W}}

        pattern = re.compile('bold"><td class(.*?)<\/td><\/tr>')
        match = pattern.findall(info)
        apptinfo[title]["Units"]={}
        for unit in match:
            try:
                # Get the unit name and put in front of dict and in the title spot
                pattern = re.compile('name.*?>(.*?)<')
                Umatch = pattern.search(unit)
                apptinfo[title]["Units"].update({title+": "+Umatch.group(1):{"Title":Umatch.group(1)}})
                Unit=title+": "+Umatch.group(1)
                if Unit==title+": ":
                    apptinfo[title]["Units"].update({title+": "+"Untitled": {"Title": "Untitled"}})
                    Unit = title+": "+"Untitled"
            except:
                # If cant find unit name put untitled
                apptinfo[title]["Units"].update({title + ": " + "Untitled": {"Title": "Untitled"}})
                Unit=title+": "+"Untitled"
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
                apptinfo[title]["Units"][Unit]["Price"] = (match.group(1)).replace("$","")
            except:
                # Cant find anything put null
                apptinfo[title]["Units"][Unit]["Price"] = "---"
        # apptinfo[title]["Description"]=match.group(1)
    return(apptinfo)
# Take in two parameters which are dicts of info and create a csv listing the info in the dict
def writecsv(first, second):
    with open('apartment_data.csv', 'w') as csvfile:
        # Titles of the the csv
        fieldnames = ['Apartment Name', 'Company', 'Location', 'Price', 'Size', 'Bedrooms', 'Furnished', 'Pets', 'Description',
                      'Bathrooms', 'Number', 'Distance to Grounds','Image']
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
                 'Description': appt['Description'],
                 'Bathrooms': appt['Units'][(list(appt['Units'])[0])]['Baths'],
                  'Number': appt['Number'], 'Distance to Grounds': appt['Distance'], 'Image':appt['Image']})
        # second is the second dict of info on the page
        for appt in second.values():
            writer.writerow(
                {'Apartment Name': appt['Title'], 'Company': '---', 'Location': appt['Address'],
                 'Price': appt['Units'][(list(appt['Units'])[0])]['Price'],
                 'Size': appt['Units'][(list(appt['Units'])[0])]['Size'],
                 'Bedrooms': appt['Units'][(list(appt['Units'])[0])]['Beds'], 'Furnished': '---', 'Pets': '---',
                 'Description': appt['Description'],
                 'Bathrooms': appt['Units'][(list(appt['Units'])[0])]['Baths'],
                  'Number': appt['Number'], 'Distance to Grounds': appt['Distance'],'Image':appt['Image']})
        writer.writerow({'Apartment Name': 'The Flats', 'Company': 'Asset Campus Housing',
                         'Location': '853 W Main St, Charlottesville, VA 22903', 'Price': '$1720', 'Size': '3',
                         'Bedrooms': 'Yes', 'Furnished': 'Yes',
                         'Pets': 'The Flats at West Village is moments from UV, & UVA Medical Center offering the most convenient student living in the area! The Downtown Mall is also right outside your door, perfect for anyone looking for convenience to work, school, and play. At The Flats at West Village, our luxury Charlottesville apartments feature modern furniture packages (at no additional cost), washers and dryers, private bedrooms, and complimentary water, cable, and internet. Unique to our community, our 1, 2, 3, & 4 bedroom floor plans have been enhanced to include queen beds and stackable dressers, providing our residents with ample space! Entertain your entourage in the social backdrop of our resort-style swimming pool, fire pits, fitness center & activity rooms. Walk to local shops and restaurants, while experiencing all that West Main has to offer.',
                         'Description': '---', 'Bathrooms': '---', 'Number': '---',
                         'Distance to Grounds': '0.9 miles from Grounds',
                         'Image': 'http://www.flatsatwestvillage.com/sites/flatsatwestvillage.com/files/styles/width_1024/public/1_1.jpg?itok=97yRmZ8J'})
        writer.writerow({'Apartment Name': 'Venable', 'Company': 'RealProperty',
                         'Location': 'Venable Apartments, 13th St NW, Charlottesville, VA 22903', 'Price': '1200',
                         'Size': '2', 'Bedrooms': 'No', 'Furnished': 'No',
                         'Pets': 'Venable Court is conveniently located on the UVA Corner, featuring large living spaces, and balconies. Walk to class or catch the UTS just steps from your door. Bike storage on site, as well as in-unit laundry machines! ',
                         'Description': '---', 'Bathrooms': '---', 'Number': '---',
                         'Distance to Grounds': '0.9 miles from Grounds',
                         'Image': 'https://images1.apartments.com/i2/jj3M6yaao1sb9uUdveDSGuB1dShq16n8wKGKJgw03mM/117/venable-court-apartments-charlottesville-va-primary-photo.jpg'})
        writer.writerow({'Apartment Name': 'Grandmarc', 'Company': 'GreyStar',
                         'Location': '301 15th St NW, Charlotteville, VA 22903', 'Price': '$1620', 'Size': '4',
                         'Bedrooms': 'Yes', 'Furnished': 'No',
                         'Pets': 'GrandMarc at the Corner offers 1, 2, and 4-bedroom apartments near the University of Virginia. We’re right in the the middle of all the great things that make the Charlottesville community unique and lovable. You’re never far away from fun or your classes- we are at the center of it all! GrandMarc at the Corner wants you to have the best experience possible. ',
                         'Description': '---', 'Bathrooms': '---', 'Number': '---',
                         'Distance to Grounds': '0.8 miles from Grounds',
                         'Image': 'https://cimg5.ibsrv.net/ibimg/www.apartmentratings.com/650x350_85-1/s/v/1/sv1jqv0X7QZ.jpg'})
        writer.writerow({'Apartment Name': '1800 Jefferson Park Avenue', 'Company': 'Nest Realty',
                         'Location': '1800 Jefferson Park Avenue, Charlottesville, VA 22903', 'Price': '$1500',
                         'Size': '3', 'Bedrooms': 'No', 'Furnished': 'No',
                         'Pets': "1800 JPA stands as one of the tallest buildings in Charlottesville and one of the most popular places to live for someone looking for an affordable place to live within walking distance of UVA's Grounds or Medical Center. If you are considering UVA real estate, 1800 JPA should be on your radar. The community is comprised of a main 10-story 'Tower' and 4 'Garden' buildings. All condominiums are a stone's throw from UVA and units on the higher floors of the Tower offer either mountain views or views of Scott Stadium. Amenities include laundry facilities, reserved parking, and a community pool.",
                         'Description': '---', 'Bathrooms': '---', 'Number': '---',
                         'Distance to Grounds': '0.6 miles from Grounds',
                         'Image': 'https://ap.rdcpix.com/1748032062/410a8c9d8b96f39afe644116471fd811l-m0xd-w1020_h770_q80.jpg'})
    return None


def writeunits(first, second):
    with open('units_data.csv', 'w') as csvfile:
        # Titles of the the csv
        fieldnames = ['Apartment','Unit Name','Price', 'Size', 'Bedrooms',
                      'Bathrooms']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # Accomadations need to made later to take in account for the units. For now I just took the first unit size, price, beds and baths
        # First is the first dict of the info on the page
        for appt in first.values():
            # for unit in appt:
            for unit in appt["Units"]:
                unit_dict = (appt["Units"][unit])
                writer.writerow(
                    {'Apartment': unit[0:len(appt["Title"])],
                     'Unit Name':unit_dict["Title"],
                     'Price': unit_dict['Price'],
                     'Size': unit_dict['Size'],
                     'Bedrooms': unit_dict['Beds'],
                     'Bathrooms': unit_dict['Baths']})
        # second is the second dict of info on the page
        for appt in second.values():
            # for unit in appt:
            for unit in appt["Units"]:
                unit_dict = (appt["Units"][unit])
                writer.writerow(
                    {'Apartment': unit[0:len(appt["Title"])],
                     'Unit Name':unit_dict["Title"],
                     'Price': unit_dict['Price'],
                     'Size': unit_dict['Size'],
                     'Bedrooms': unit_dict['Beds'],
                     'Bathrooms': unit_dict['Baths']})
    return None

# Get all the links and appt titles from both pages from this website
firstpage=(ScrapHtmlCode('https://www.collegestudentapartments.com/college/university-of-virginia-charlottesville-virginia/apartments/'))
secondpage=(ScrapHtmlCode('https://www.collegestudentapartments.com/college/university-of-virginia-charlottesville-virginia/apartments/?page=2'))
# Get a dict of all info from the html links from the first and second page
first_page_appt_info= (getinfo(firstpage))
second_page_appt_info= (getinfo(secondpage))
# Write CSV from the info in the first and second page
writecsv(first_page_appt_info,second_page_appt_info)
writeunits(first_page_appt_info,second_page_appt_info)
