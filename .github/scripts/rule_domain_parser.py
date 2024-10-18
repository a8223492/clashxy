import os
import requests

def download_yaml_files(source_file, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

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
                except requests.RequestException as e:
                    print(f"Failed to download {line}: {e}")

def extract_domains_from_directory(directory, output_file):
    domains = set()

    for filename in os.listdir(directory):
        if filename.endswith('.yaml'):
            with open(os.path.join(directory, filename), 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('  - DOMAIN-SUFFIX,') or line.startswith('  - DOMAIN,'):
                        domain = line.split(',', 1)[1].strip()
                        domains.add(domain)

    with open(output_file, 'w') as file:
        for domain in sorted(domains):
            file.write(domain + '\n')

    print(f"Extracted {len(domains)} unique domains")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(script_dir))
    
    source_file = os.path.join(repo_root, 'source', 'china_list.txt')
    output_directory = os.path.join(repo_root, 'yaml_files')
    output_file = os.path.join(repo_root, 'china.list')

    if not os.path.exists(source_file):
        print(f"Error: Source file {source_file} does not exist.")
        exit(1)

    download_yaml_files(source_file, output_directory)
    extract_domains_from_directory(output_directory, output_file)

    print(f"Domain list has been generated and saved to {output_file}")
