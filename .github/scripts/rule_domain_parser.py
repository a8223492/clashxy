import os
import requests

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

    print("\nDownloaded files and folder structure:")
    for root, dirs, files in os.walk(output_directory):
        level = root.replace(output_directory, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            print(f"{sub_indent}{file}")

    print("\nContents of downloaded files:")
    for filename in os.listdir(output_directory):
        filepath = os.path.join(output_directory, filename)
        print(f"\nFile: {filepath}")
        with open(filepath, 'r') as file:
            print(file.read())

def extract_domains_from_directory(directory, output_file):
    domains = set()

    print(f"\nExtracting domains from directory: {directory}")

    for filename in os.listdir(directory):
        if filename.endswith('.yaml'):
            filepath = os.path.join(directory, filename)
            print(f"\nProcessing file: {filepath}")
            with open(filepath, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('  - DOMAIN-SUFFIX,') or line.startswith('  - DOMAIN,'):
                        print(f"Matched line: {line}")
                        domain = line.split(',', 1)[1].strip()
                        domains.add(domain)

    print("\nExtracted unique domains:")
    for domain in sorted(domains):
        print(domain)

    with open(output_file, 'w') as file:
        for domain in sorted(domains):
            file.write(domain + '\n')

    print(f"\nGenerated domain list file: {output_file}")
    print("Contents of the generated file:")
    with open(output_file, 'r') as file:
        print(file.read())

    print(f"Extracted {len(domains)} unique domains")

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
        exit(1)

    download_yaml_files(source_file, output_directory)
    extract_domains_from_directory(output_directory, output_file)

    print(f"Domain list has been generated and saved to {output_file}")
