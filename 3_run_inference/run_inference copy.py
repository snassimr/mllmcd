import concurrent.futures
import subprocess

# Define the prompts and other parameters for the curl commands
prompts = [
    "the following is a python script that ssh into a remote linux box and pulls all the log files it can find, then moves them to a temp local dir, extracts all the logs (even the tar.gz ones), line by line, and then sorts them by time putting most recent logs at the top, and outputs it all as combined.log",
    # "the following is a bash script to backup a MySQL database, compress it, and move it to an AWS S3 bucket.",
    # "the following is a Python script to scrape a website for all its images and download them into a specified directory.",
    # "the following is a JavaScript function to fetch data from an API and display it on a webpage.",
    # "the following is a C program to read a file, count the number of words, and print the count."
]

def run_curl(prompt, index):
    command = [
        "curl", "-s", "-X", "POST", "http://0.0.0.0:8000/generate",
        "-H", "Content-Type: application/json",
        "-d", f'{{"prompt": "{prompt}", "max_tokens": 1000, "temperature": 0.5}}'
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result)
    return f"Output of command {index + 1}:\n{result.stdout}\n"

# Use ThreadPoolExecutor to run curl commands in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    futures = [executor.submit(run_curl, prompt, i) for i, prompt in enumerate(prompts)]
    for future in concurrent.futures.as_completed(futures):
        print(future.result())
