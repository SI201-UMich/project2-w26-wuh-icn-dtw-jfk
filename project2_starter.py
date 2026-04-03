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


    # print(f"html_path is: {html_path}")
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
        # print(title)
        collect_info2.append(info)
        collect_info.append(id_info)
    
    return_list = []

    # for x in range(10):
    for x in range(len(collect_info)): #change to length of collect_info instead of 10
        return_list.append((collect_info2[x], collect_info[x]))
    
    # print(return_list)
    return return_list


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
        soup = BeautifulSoup(html, "html.parser")

    policy_number = ""
    host_type = "regular"
    host_name = ""
    room_type = "Entire Room"
    location_rating = 0.0

    page_text = soup.get_text(" ", strip=True)

    # host_name, room_type
    host_match = re.search(r'((?:Entire|Private|Shared)[^\.]*?) hosted by\s*([A-Za-z &]+)', page_text, re.IGNORECASE)
    if host_match:
        subtitle = host_match.group(1).strip()
        host_name = host_match.group(2).strip()

        subtitle_lower = subtitle.lower()
        if "private" in subtitle_lower:
            room_type = "Private Room"
        elif "shared" in subtitle_lower:
            room_type = "Shared Room"
        else:
            room_type = "Entire Room"

    # host_type
    if "superhost" in page_text.lower():
        host_type = "Superhost"

    # policy_number
    policy_match = re.search(r'Policy number:\s*([^\s]+)', page_text, re.IGNORECASE)
    if policy_match:
        raw_policy = policy_match.group(1).strip()
        raw_lower = raw_policy.lower()

        if "pending" in raw_lower:
            policy_number = "Pending"
        elif "exempt" in raw_lower:
            policy_number = "Exempt"
        else:
            policy_number = raw_policy

    # location_rating
    location_match = re.search(
        r'Cleanliness\s+[0-9]\.?[0-9]?\s+Accuracy\s+[0-9]\.?[0-9]?\s+Communication\s+[0-9]\.?[0-9]?\s+Location\s+([0-9]\.?[0-9]?)',
        page_text,
        re.IGNORECASE
    )
    if location_match:
        location_rating = float(location_match.group(1))

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
    # f = open(f"{filename}", "x")
    # locationlist = []  
    # with open(f"{filename}", "a") as f:
    #     def myFunc(e):
    #         return e[5]
        
    #     for row in data:
    #         locationlist.append(row)
    #         locationlist.sort(key=myFunc)

    #     for x in range(len(data)):
    #         f.write(f"{locationlist[x]}\n")
    # f.close()
    
    # Suggestion from Yunchang:
    data_sorted = sorted(data, key=lambda row: row[6], reverse=True)

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "listing_title",
            "listing_id",
            "policy_number",
            "host_type",
            "host_name",
            "room_type",
            "location_rating"
        ])
        writer.writerows(data_sorted)
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
    outdict = {"Private Room": [0.0, 0], "Shared Room": [0.0, 0], "Entire Room": [0.0, 0]}
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
    invalid_list = []

    valid_pattern1 = r"20\d{2}-00\d{4}STR"
    valid_pattern2 = r"STR-000\d{4}"

    for row in data:
        listing_id = row[1]
        policy_number = row[2]

        if policy_number in ["Pending", "Exempt"]:
            continue

        if not (re.match(valid_pattern1, policy_number) or re.match(valid_pattern2, policy_number)):
            invalid_list.append(listing_id)
    
    return invalid_list
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
        self.assertEqual(len(self.listings), 18)
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        result={}
        for stuff in html_list:
            result[stuff]=get_listing_details(stuff)[stuff]
        self.assertEqual(result["467507"]["policy_number"],"STR-0005349")
        self.assertEqual(result["1944564"]["host_type"],"Superhost")
        self.assertEqual(result["1944564"]["room_type"],"Entire Room")
        self.assertAlmostEqual(result["1944564"]["location_rating"],4.9)

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
        for tup in self.detailed_data:
            self.assertEqual(len(tup), 7)
        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        self.assertEqual(self.detailed_data[-1], ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8))

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].
        output_csv(self.detailed_data, out_path)
        with open(out_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            firstline = next(reader)
            rows = list(reader)

        self.assertEqual(rows[0], ['Guesthouse in San Francisco', '49591060', 'STR-0000253', 'Superhost', 'Ingrid', 'Entire Room', '5.0'])

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        avg_ratings = avg_location_rating_by_room_type(self.detailed_data)

        rating = avg_ratings.get("Private Room")
        self.assertAlmostEqual(rating, 4.9)

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        invalid_listings = validate_policy_numbers(self.detailed_data)
        self.assertEqual(invalid_listings, ["16204265"])


def main():
    # detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    # output_csv(detailed_data, "airbnb_dataset.csv")
    pass


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
