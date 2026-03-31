# SI 201 HW4 (Library Checkout System)
# Your name:
# Your student id:
# Your email:
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================

    filehandle = open(html_path)
    soup = BeautifulSoup(filehandle, 'html.parser')

    collect_info = []
    title_list2 = soup.find_all('div', class_='t1jojoys')
    collect_info2 = []
    idregexp = 'id="title_(\d+)"'
    for title in title_list2:
        info = title.text
        regtitle = str(title)
        try:
            #id_info = re.findall(idregexp, regtitle)
            id_info = re.findall(idregexp, regtitle)[0] #removed [] from tuple list
        except:
            print("whoops")
            id_info = 00000
        print(title)
        collect_info2.append(info)
        collect_info.append(id_info)
    
    return_list = []

    # for x in range(10):
    for x in range(len(collect_info)): #change to length of collect_info instead of 10
        return_list.append((collect_info2[x], collect_info[x]))
    
    print(return_list)
    return return_list
    
    # filehandle = open(html_path)
    # soup = BeautifulSoup(filehandle, 'html.parser')
    # title_list = soup.find_all('a')
    # collect_info = []
    # for title in title_list:
    #     href = title.get('href')
    #     if href and '/rooms/' in href:
    #         listing_id = href.split('/rooms/')[1].split('?')[0]
    #         listing_title = title.get_text()
    #         collect_info.append((listing_title, listing_id))
    
    # title_list2 = soup.find_all('div', class_='t1jojoys')
    # collect_info2 = []
    # for title in title_list2:
    #     info = title.text
    #     collect_info2.append(info)
    # print(collect_info2)
    # return collect_info2
    

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    base_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(base_path, "html_files", f"listing_{listing_id}.html")
    with open(filename, encoding="utf-8-sig") as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')

    policy_number = ""
    host_type = "regular"
    host_name = ""
    room_type = ""
    location_rating = 0.0
    
    # Host Name & Room Type
    for h2 in soup.find_all('h2'):
        text = h2.get_text(" ", strip=True)

        match = re.search(r"hosted by\s+(.+)", text, re.IGNORECASE)
        if match:
            host_name = match.group(1).strip()

            # Room Type
            if "private" in text.lower():
                room_type = "Private Room"
            elif "shared" in text.lower():
                room_type = "Shared Room"
            else:            
                room_type = "Entire Room"

            break

        # Host Type
        if "superhost" in text.lower():
            host_type = "Superhost"

        # Policy Number
        for li in soup.find_all('li'):
            text = li.get_text(" ", strip=True).lower()
            if "policy" in text:
                raw = li.get_text(" ", strip=True)
                raw = text.split(":")[-1].strip()
                raw = raw.split("Response")[0].strip()

                if "pending" in raw.lower():
                    policy_number = "Pending"
                elif "exempt" in raw.lower():
                    policy_number = "Exempt"
                else:
                    policy_number = raw

                break
        
        # Location Rating
        match = re.search(r'([0-9.]+) out of 5', html)
        if match:
            location_rating = float(match.group(1))
        else:
            location_rating = 0.0
    

    return {
        listing_id: {
            "policy_number": policy_number,
            "host_type": host_type,
            "host_name": host_name,
            "room_type": room_type,
            "location_rating": location_rating
        }
    }

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    listing = load_listing_results(html_path)
    result = []
    for title, id in listing:
        detail_id = get_listing_details(id)
        detail = detail_id[id]
        policy = detail["policy_number"]
        hosttype = detail["host_type"]
        hostname = detail["host_name"]
        roomtype = detail["room_type"]
        location_rating = detail["location_rating"]
        tup = (title, id, policy, hosttype, hostname, roomtype, location_rating)
        result.append(tup)
    return result
   
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    outdict = {"Private room": [0.0, 0], "Shared room": [0.0, 0], "Entire room": [0.0, 0]}
    for each in data:
        if each[6] == 0.0:
            continue
        else:
            lst = outdict[each[5]]
            lst[0] += each[6]
            lst[1] += 1
    returnning = {}
    for room_type, (total, count) in outdict.items():
        if count > 0:
            returnning[room_type] = total / count
        else:
            returnning[room_type] = 0.0
    return returnning

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        pass

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        pass

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        pass

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].

        os.remove(out_path)
        pass

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        pass

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        pass


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
