import os
import yaml
import re

def extract_domains_from_directory(directory, output_file):
    domains = set()
    valid_domain_pattern = re.compile(r'^[a-zA-Z0-9.-]+$')  # 域名的有效格式

    for filename in os.listdir(directory):
        if filename.endswith('.yaml'):
            with open(os.path.join(directory, filename), 'r') as file:
                data = yaml.safe_load(file)
                # 从规则中提取域名
                for rule in data.get('rules', []):
                    if rule.startswith('DOMAIN-SUFFIX,') or rule.startswith('DOMAIN,'):
                        domain = rule.split(',')[1].strip()
                        if valid_domain_pattern.match(domain):  # 只添加符合格式的域名
                            domains.add(domain)

    # 写入到输出文件中
    with open(output_file, 'w') as file:
        for domain in sorted(domains):
            file.write(domain + '\n')

if __name__ == "__main__":
    # 提取域名并写入输出文件
    extract_domains_from_directory('yaml_files', 'china.list')
