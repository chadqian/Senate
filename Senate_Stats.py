import xml.etree.cElementTree as ET
import urllib.request
import csv
import copy

def Senatechecker(url, Senate_stats_dict):
    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
    opener = AppURLopener()
    response = opener.open(url)
    tree = ET.parse(response)
    root = tree.getroot()
    newroot = root[len(root)-1]
    Senate_dict = {}
    r_yea = 0
    r_nay = 0
    d_yea = 0
    d_nay = 0
    new_Senate_stats_dict = copy.deepcopy(Senate_stats_dict)
    for senator in newroot:
        if senator[1].text != "Barkley":
            if senator[5].text == "Yea":
                Senate_dict[senator[0].text] = (senator[3].text, 1)
                if senator[3].text == "R":
                    r_yea += 1
                else:
                    d_yea += 1
            elif senator[5].text == "Nay":
                Senate_dict[senator[0].text] = (senator[3].text, 0)
                if senator[3].text == "R":
                    r_nay += 1
                else:
                    d_nay += 1
            else:
                Senate_dict[senator[0].text] = (senator[3].text, -1)
        else:
            Senate_dict[senator[0].text] = (senator[3].text, -1)
    for Senator in Senate_dict:
        if Senator not in new_Senate_stats_dict:
            new_Senate_stats_dict[Senator] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if r_yea + r_nay != 0 and d_yea + d_nay != 0:
            if Senate_dict[Senator][1] != -1:
                new_Senate_stats_dict[Senator][4] = new_Senate_stats_dict[Senator][4]+1
                current = new_Senate_stats_dict[Senator][4]
                if Senate_dict[Senator][0] == "R":
                    if Senate_dict[Senator][1] == 0:
                        new_Senate_stats_dict[Senator][0] = (new_Senate_stats_dict[Senator][0]*(current-1)+(r_nay-1-r_yea)/(r_yea+r_nay-1))/current
                        new_Senate_stats_dict[Senator][2] = (new_Senate_stats_dict[Senator][2]*(current-1)+(d_nay-d_yea)/(d_yea+d_nay))/current
                    elif Senate_dict[Senator][1] == 1:
                        new_Senate_stats_dict[Senator][0] = (new_Senate_stats_dict[Senator][0]*(current-1)+(r_yea-1-r_nay)/(r_yea+r_nay-1))/current
                        new_Senate_stats_dict[Senator][2] = (new_Senate_stats_dict[Senator][2]*(current-1)+(d_yea-d_nay)/(d_yea+d_nay))/current
                    if (Senate_dict[Senator][1] == 0 and r_nay > r_yea) or (Senate_dict[Senator][1] == 1 and r_yea > r_nay):
                        new_Senate_stats_dict[Senator][1] = new_Senate_stats_dict[Senator][1]+1
                    if (Senate_dict[Senator][1] == 0 and d_nay > d_yea) or (Senate_dict[Senator][1] == 1 and d_yea > d_nay):
                        new_Senate_stats_dict[Senator][3] = new_Senate_stats_dict[Senator][3]+1
                if Senate_dict[Senator][0] == "D" or Senate_dict[Senator][0] == "I" or Senate_dict[Senator][0] == "ID":
                    if Senate_dict[Senator][1] == 0:
                        new_Senate_stats_dict[Senator][0] = (new_Senate_stats_dict[Senator][0]*(current-1)+(d_nay-1-d_yea)/(d_yea+d_nay-1))/current
                        new_Senate_stats_dict[Senator][2] = (new_Senate_stats_dict[Senator][2]*(current-1)+(r_nay-r_yea)/(r_yea+r_nay))/current
                    elif Senate_dict[Senator][1] == 1:
                        new_Senate_stats_dict[Senator][0] = (new_Senate_stats_dict[Senator][0]*(current-1)+(d_yea-1-d_nay)/(d_yea+d_nay-1))/current
                        new_Senate_stats_dict[Senator][2] = (new_Senate_stats_dict[Senator][2]*(current-1)+(r_yea-r_nay)/(r_yea+r_nay))/current
                    if (Senate_dict[Senator][1] == 0 and d_nay > d_yea) or (Senate_dict[Senator][1] == 1 and d_yea > d_nay):
                        new_Senate_stats_dict[Senator][1] = new_Senate_stats_dict[Senator][1]+1
                    if (Senate_dict[Senator][1] == 0 and r_nay > r_yea) or (Senate_dict[Senator][1] == 1 and r_yea > r_nay):
                        new_Senate_stats_dict[Senator][3] = new_Senate_stats_dict[Senator][3]+1
                if (r_yea > r_nay and d_yea < d_nay) or (r_yea < r_nay and d_yea > d_nay):
                    new_Senate_stats_dict[Senator][9] = new_Senate_stats_dict[Senator][9]+1
                    current = new_Senate_stats_dict[Senator][9]
                    if Senate_dict[Senator][0] == "R":
                        if Senate_dict[Senator][1] == 0:
                            new_Senate_stats_dict[Senator][5] = (new_Senate_stats_dict[Senator][5]*(current-1)+(r_nay-1-r_yea)/(r_yea+r_nay-1))/current
                            new_Senate_stats_dict[Senator][7] = (new_Senate_stats_dict[Senator][7]*(current-1)+(d_nay-d_yea)/(d_yea+d_nay))/current
                        elif Senate_dict[Senator][1] == 1:
                            new_Senate_stats_dict[Senator][5] = (new_Senate_stats_dict[Senator][5]*(current-1)+(r_yea-1-r_nay)/(r_yea+r_nay-1))/current
                            new_Senate_stats_dict[Senator][7] = (new_Senate_stats_dict[Senator][7]*(current-1)+(d_yea-d_nay)/(d_yea+d_nay))/current
                        if (Senate_dict[Senator][1] == 0 and r_nay > r_yea) or (Senate_dict[Senator][1] == 1 and r_yea > r_nay):
                            new_Senate_stats_dict[Senator][6] = new_Senate_stats_dict[Senator][6]+1
                        if (Senate_dict[Senator][1] == 0 and d_nay > d_yea) or (Senate_dict[Senator][1] == 1 and d_yea > d_nay):
                            new_Senate_stats_dict[Senator][8] = new_Senate_stats_dict[Senator][8]+1
                    if Senate_dict[Senator][0] == "D" or Senate_dict[Senator][0] == "I" or Senate_dict[Senator][0] == "ID":
                        if Senate_dict[Senator][1] == 0:
                            new_Senate_stats_dict[Senator][5] = (new_Senate_stats_dict[Senator][5]*(current-1)+(d_nay-1-d_yea)/(d_yea+d_nay-1))/current
                            new_Senate_stats_dict[Senator][7] = (new_Senate_stats_dict[Senator][7]*(current-1)+(r_nay-r_yea)/(r_yea+r_nay))/current
                        elif Senate_dict[Senator][1] == 1:
                            new_Senate_stats_dict[Senator][5] = (new_Senate_stats_dict[Senator][5]*(current-1)+(d_yea-1-d_nay)/(d_yea+d_nay-1))/current
                            new_Senate_stats_dict[Senator][7] = (new_Senate_stats_dict[Senator][7]*(current-1)+(r_yea-r_nay)/(r_yea+r_nay))/current
                        if (Senate_dict[Senator][1] == 0 and d_nay > d_yea) or (Senate_dict[Senator][1] == 1 and d_yea > d_nay):
                            new_Senate_stats_dict[Senator][6] = new_Senate_stats_dict[Senator][6]+1
                        if (Senate_dict[Senator][1] == 0 and r_nay > r_yea) or (Senate_dict[Senator][1] == 1 and r_yea > r_nay):
                            new_Senate_stats_dict[Senator][8] = new_Senate_stats_dict[Senator][8]+1
    return new_Senate_stats_dict

def Senate(year):
    Senate_vote_dict = {}
    session = (year - 1787) // 2
    part = 2 - (year%2)
    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
    opener = AppURLopener()
    big_url = "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_" + str(session) + "_" + str(part) + ".xml"
    response = opener.open(big_url)
    tree = ET.parse(response)
    root = tree.getroot()
    if year == 1993:
        bill = int(root[2][0][0].text)
    else:
        bill = int(root[3][0][0].text)
    begin_url = "https://www.senate.gov/legislative/LIS/roll_call_votes/vote" + str(session) + str(part) + "/vote_" + str(session) + "_" + str(part) + "_00"
    for i in range(1, bill + 1, 1):
        if i < 10:
            url_name = begin_url + "00" + str(i) + ".xml"
        elif i > 99:
            url_name = begin_url + str(i) + ".xml"
        else:
            url_name = begin_url + "0" + str(i) + ".xml"
        print(i)
        Senate_vote_dict = Senatechecker(url_name, Senate_vote_dict)
    return Senate_vote_dict

def Senate_analysis(beginning_year, length):
    Senate_stats = []
    for l in range(length):
        temp_dict = Senate(beginning_year + l)
        for key, val in temp_dict.items(): 
            Senate_stats.append([key] + [str(beginning_year+l)] + val) 
    file_name = 'Comprehensive_Senate_Stats_' + str(beginning_year) + '-' + str(beginning_year+length-1) +'.csv'
    with open(file_name, 'w', newline='') as csvfile:
        Senators = csv.writer(csvfile)
        Senators.writerow(['Senator', 'Year', 'Partisan Index, All Votes', 'Partisan Votes, All Votes', 'Bipartisan Index, All Votes', 'Bipartisan Votes, All Votes', 'Total Votes', 'Partisan Index, Divided Votes', 'Partisan Votes, Divided Votes', 'Bipartisan Index, Divided Votes', 'Bipartisan Votes, Divided Votes', 'Total Divided Votes'])
        for row in Senate_stats:
            Senators.writerow(row)  
