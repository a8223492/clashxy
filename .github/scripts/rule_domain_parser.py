import os
import requests
import sys

def download_yaml_files(source_file, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    print(f"Downloading YAML files to: {output_directory}")

    with open(source_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    print(f"Downloading: {line}")
                    response = requests.get(line, timeout=30)
                    response.raise_for_status()
                    filename = os.path.join(output_directory, os.path.basename(line))
                    with open(filename, 'w') as yaml_file:
                        yaml_file.write(response.text)
                    print(f"Downloaded: {filename}")
                except requests.RequestException as e:
                    print(f"Failed to download {line}: {e}")

    print("\nDownloaded files:")
    for filename in os.listdir(output_directory):
        print(f"- {filename}")

def extract_domains_from_directory(directory, output_file):
    domains = set()

    print(f"\nExtracting domains from directory: {directory}")

    for filename in os.listdir(directory):
        if filename.endswith('.yaml'):
            filepath = os.path.join(directory, filename)
            print(f"\nProcessing file: {filepath}")
            try:
                with open(filepath, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line.startswith('  - DOMAIN-SUFFIX,') or line.startswith('  - DOMAIN,'):
                            print(f"Matched line: {line}")
                            domain = line.split(',', 1)[1].strip()
                            domains.add(domain)
            except Exception as e:
                print(f"Error processing file {filepath}: {e}")

    print(f"\nExtracted {len(domains)} unique domains")

    with open(output_file, 'w') as file:
        for domain in sorted(domains):
            file.write(domain + '\n')

    print(f"\nGenerated domain list file: {output_file}")
    print(f"Number of domains written: {len(domains)}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(script_dir))
    
    source_file = os.path.join(repo_root, 'source', 'china_list.txt')
    output_directory = os.path.join(repo_root, 'yaml_files')
    output_file = os.path.join(repo_root, 'china.list')

    print(f"Source file: {source_file}")
    print(f"Output directory: {output_directory}")
    print(f"Output file: {output_file}")

    if not os.path.exists(source_file):
        print(f"Error: Source file {source_file} does not exist.")
        sys.exit(1)

    try:
        download_yaml_files(source_file, output_directory)
        extract_domains_from_directory(output_directory, output_file)
        print(f"Domain list has been generated and saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    print("Script execution completed successfully.")
