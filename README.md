
# Solution Take-Home Assignement

## Explanation

#### Stream
I had to start by finding a way to iterate through a 20GB JSON file for this assignment. The task involved identifying URLs related to Anthem PPO NY, and no post-processing was required. My approach was to scan through the file, locate the corresponding URLs, and then save them to a CSV file. There will be duplicates, but in a real-world scenario, I could implement a batch process later on to remove them.

To iterate through the JSON file, I utilized the "ijson" library and "csv" to save the output to a CSV file iteratively.

#### Parsing JSON

To carefully analyze the data, I created some small samples of the JSON file that would allow me to understand the data better. (See an example of `sample_input.json` in the EDA folder.) I created more of them but could not upload them to GitHub because of their size.

The following step consisted of identifying which URLs I need to keep track of.

##### 1. Identify ANTHEM PPO

To identify the plans corresponding to ANTHEM PPO, I built a regex on the that would check if ANTHEM...PPO is in the plan_name. This idea came after finding some examples of that I found on the JSON, such as "ANTHEM BLUE ACCESS PPO HSA - THE CULVER EDUCATIONAL FOUNDATION - ANTHEM"


##### 2. Identify NY

Once I had all the in-network files realted to ANTHEM PPO, the next step consisted of identifying those who were from NY.


The urls were composed of some KEYPAIR and EXPIRATION tokens that were not meaningul. The important part was the before .gz file.

In the below example for BCBS Tennessee, we can see that the number 890 is constant accross both URLs. The number the difference lies in B0 to D0, therefore my intuition is that B0 and D0 are related to the network and 890_58 to the plan and state.
```json
{
    "description": "BCBS Tennessee, Inc. : Network P",
    "location": "https://anthembcca.mrf.bcbs.com/2024-05_890_58B0_in-network-rates_52_of_60.json.gz"
},
{
    "description": "BCBS Tennessee, Inc. : Network C",
    "location": "https://anthembcca.mrf.bcbs.com/2024-05_890_58D0_in-network-rates_33_of_60.json.gz"
}
```
The URL has variations in the `anthembc` prefix, which changes based on the location. For instance, "anthembcca" and "anthembcbsoh." I found it puzzling that the URL for California contained "BCBS Tennessee." Even after downloading the in-network file, the reporting_entity_name still appeared as BCBS Tennessee. I assumed that the "anthembcca" prefix was only for hosting purposes, as the files were the same for different prefixes, such as `anthembcca` and `anthembcbsoh`.

The "description" field was not very helpful, as the only instance related to New York that I found in the extracted samples was "Highmark BCBS Western NY," which is not part of ANTHEM. Therefore, after examining the files, I decided to filter based on the plan corresponding to ANTHEM in New York. After reviewing the "In-Network Negotiated Rates Files" description, I found that the code 240_39B0 and 240_39F0 corresponded to ANTHEM in New York: `Empire BlueCross BlueShield`


##### 3. ANTHEM EIN Lookup

When using this tool I realized that there was a pattern per state, for instance New York had 39FO, Tennesse 58D0 and etc, which helped be come to previous conclusion.

In addition to the description above, the file can be used to verify if the PLAN NAME EIN is associated with an ANTHEM plan by checking if it's included in the NY list. Due to time constraints, I was unable to explore other solutions, but I'm considering using the EIN number of the providers for this purpose, although I'm not sure how to proceed.

## Time Distribution
Data Analysis: 1h
Code: 30min
Writing: 40min

## Script
### Requirements
Create Conda environemt from .yml. Python 3.10.14 was used
```bash
conda env create -f env.yaml
```
### Execution

Change the below **INPUT_FILE_PATH** accordingly.

Example:

INPUT_FILE = "../2024-05-01_anthem_index.json"

OUTPUT_FILE = "ANTHEM_PPO_NY_URLS.csv"

```bash
python stream_main.py ../2024-05-01_anthem_index.json ANTHEM_PPO_NY_URLS.csv
```

### Execution time 

Total execution time: 38.31 seconds

On a MAC M1 PRO

## Improvements
After extracting the URL, the next step consists of creating an ETL process to remove deduplication in batch processing, possibly every hour. 

I would deploy this solution as this:

 STREAM JSON => STORAGE => BATCH PROCESSING JOB for post-processing (remove duplicates, check for FP suing ENI Lookup website)
