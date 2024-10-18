import os
import yaml
import re

def extract_domains_from_directory(directory, output_file):
    domains = set()
    valid_domain_pattern = re.compile(r'^[a-zA-Z0-9.-]+$')  # Valid domain format

    print(f"\nExtracting domains from directory: {directory}")

    for filename in os.listdir(directory):
        if filename.endswith('.yaml'):
            filepath = os.path.join(directory, filename)
            print(f"\nProcessing file: {filepath}")
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    data = yaml.safe_load(file)
                    if data is None:
                        print(f"Warning: The file {filepath} is empty or has invalid YAML content.")
                        continue
                    # Adjust the following based on the actual structure of your YAML files
                    rules = data.get('payload') or data.get('rules') or data.get('rule-provider', {}).get('rules')
                    if rules is None:
                        print(f"Warning: No 'payload' or 'rules' found in {filepath}.")
                        continue
                    for rule in rules:
                        if rule.startswith('DOMAIN-SUFFIX,') or rule.startswith('DOMAIN,'):
                            parts = rule.split(',', 1)
                            if len(parts) >= 2:
                                domain = parts[1].strip()
                                if valid_domain_pattern.match(domain):
                                    domains.add(domain)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file {filepath}: {e}")
            except Exception as e:
                print(f"Error processing file {filepath}: {e}")

    print(f"\nExtracted {len(domains)} unique domains")

    with open(output_file, 'w', encoding='utf-8') as file:
        for domain in sorted(domains):
            file.write(domain + '\n')

    print(f"\nGenerated domain list file: {output_file}")
    print(f"Number of domains written: {len(domains)}")
