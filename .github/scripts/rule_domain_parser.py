import os
import yaml
import re
import requests

def download_yaml_files(source_file, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(source_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    print(f"Downloading: {line}")
                    response = requests.get(line, timeout=30)
                    response.raise_for_status()
                    filename = os.path.join(output_directory, os.path.basename(line))
                    with open(filename, 'w', encoding='utf-8') as yaml_file:
                        yaml_file.write(response.text)
                except requests.RequestException as e:
                    print(f"Failed to download {line}: {e}")

def extract_domains_from_directory(directory, output_file):
    domains = set()
    valid_domain_pattern = re.compile(r'^[a-zA-Z0-9.-]+$')  # Valid domain format

    for filename in os.listdir(directory):
        if filename.endswith('.yaml'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                try:
                    data = yaml.safe_load(file)
                except yaml.YAMLError as e:
                    print(f"Failed to parse YAML file {filepath}: {e}")
                    continue
                if data and 'payload' in data:
                    for rule in data['payload']:
                        if rule.startswith('DOMAIN-SUFFIX,') or rule.startswith('DOMAIN,'):
                            parts = rule.split(',')
                            if len(parts) >= 2:
                                domain = parts[1].strip()
                                if valid_domain_pattern.match(domain):
                                    domains.add(domain)

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as file:
        for domain in sorted(domains):
            file.write(domain + '\n')

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(script_dir))
    
    source_file = os.path.join(repo_root, 'source', 'china_list.txt')
    output_directory = os.path.join(repo_root, 'yaml_files')
    output_file = os.path.join(repo_root, 'china.list')

    # Check if source_file exists
    if not os.path.exists(source_file):
        print(f"Error: Source file {source_file} does not exist.")
        exit(1)

    # Download YAML files
    download_yaml_files(source_file, output_directory)
    # Extract domains and write to output file
    extract_domains_from_directory(output_directory, output_file)

    print(f"Domain list has been generated and saved to {output_file}")
