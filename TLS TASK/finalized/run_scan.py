import subprocess
import os

def run_testssl(url):
    """Run testssl.sh for a given URL synchronously and save the output to a file."""
    # Sanitize the URL to create a valid filename (removes special characters)
    sanitized_url = url.replace('://', '_').replace('/', '_').replace('.', '_')
    
    # Output file name based on the sanitized URL for text output
    output_file = f"scan_{sanitized_url}.txt"
    
    # Output CSV file name based on the sanitized URL
    csvfile = f"./scan_output/scan_{sanitized_url}.csv"

    # Print that we're starting the scan for the current URL
    print(f"Starting testssl.sh for {url}...")
    print('\toutput file will be -> '+csvfile)

    # Prepare the command with the --csvfile flag (automatically added)
    command = ['./testssl.sh', '--csvfile', csvfile, '--htmlfile', 'scan_{sanitized_url}.html', url]

    try:
        # Run the testssl.sh command synchronously and capture output
        result = subprocess.run(
            command, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        # Write the text output (from stdout) to the corresponding .txt file
        #with open(output_file, 'w') as f:
        #    f.write(result.stdout.decode())
        
        print(f"testssl.sh results for {url} saved to {output_file} and {csvfile}")
    
    except subprocess.CalledProcessError as e:
        # Handle errors and write error details to the output file
        with open(output_file, 'w') as f:
            f.write(f"Error running testssl.sh on {url}: {e.stderr.decode()}")
        print(f"Error running testssl.sh on {url}. See {output_file} for details.")

def read_urls(file_path):
    """Read URLs from the given file."""
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls]

def main():
    # Path to the file containing URLs
    urls_file = 'urls.txt'

    # Read URLs from file
    urls = read_urls(urls_file)
    
    # Run testssl.sh on each URL sequentially
    for url in urls:
        run_testssl(url)

if __name__ == "__main__":
    # Run the main function synchronously
    main()
