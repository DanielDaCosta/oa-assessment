import ijson
import re
import csv
import time
import sys

def check_if_plan_is_anthem_ppo(plan_name: str) -> bool:
    # Check if plan_name has ATHEM ... PPO
    pattern = re.compile(r'ANTHEM.*PPO', re.DOTALL | re.IGNORECASE)
    match = pattern.search(plan_name)
    return True if match else False


def filter_url_based_on_ANTHEM_NY(url: str, code_empire:str = "254_39") -> bool:
    # break URL in 2  
    parts = url.split('.gz?')

    if len(parts) < 2:
        return False
    
    # Example: https://anthembcbsky.mrf.bcbs.com/2024-05_254_39B0_in-network-rates_1_of_10.json.gz?
    first_part_url = parts[0]

    # Check if it's "Empire BlueCross BlueShield"
    if code_empire in first_part_url:
        return True
    else:
        return False



if __name__ == '__main__':


    # INPUT_FILE = "../2024-05-01_anthem_index.json"
    # OUTPUT_FILE = "ANTHEM_PPO_NY_URLS.csv"
    if len(sys.argv) != 3:
        print("Usage: python script.py INPUT_FILE OUTPUT_FILE")
        sys.exit(1)

    INPUT_FILE = sys.argv[1]
    OUTPUT_FILE = sys.argv[2]


    # START TIMER
    start_time = time.time()

    with open(INPUT_FILE, 'r') as file, open(OUTPUT_FILE, 'w', newline='') as csvfile:

        # Output file
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["URL"])
        
        # Iterating over each reporting structure
        reporting_structure = ijson.items(file, 'reporting_structure.item')
        i = 0
        for report in reporting_structure:
            
            # Analyze for ANTHEM PPO
            has_anthem_ppo = False
            for reporting_plans in report['reporting_plans']:

                # Get plan_name
                plan_name = reporting_plans.get('plan_name')
                if plan_name:
                    check_if_plan_is_ANTHEM_PPO = check_if_plan_is_anthem_ppo(plan_name)
                    if check_if_plan_is_ANTHEM_PPO:
                        has_anthem_ppo = True

            # If plan_name is ANTHEM PPO search for NY state
            # !! ANTHEM in NY is called "Empire BlueCross BlueShield"
            # Need to find the in_network files for this particular name

            # "Empire BlueCross BlueShield" => code 254 39__
            if has_anthem_ppo:
                for network_file in report.get('in_network_files'):

                    # Need to fier for
                    url_location = network_file.get('location')
                    if url_location:
                        is_NY = filter_url_based_on_ANTHEM_NY(url_location)
                        if is_NY:
                            csv_writer.writerow([url_location])

    # END TIMER
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time:.2f} seconds")