import subprocess
import ssl
import socket
from OpenSSL import crypto
import re


# 读取文件
def read_domains_file(file_name):
    try:
        with open(file_name, 'r') as file:
            domains = [line.strip().split("\t") for line in file.readlines()]
            for domain_pair in domains:
                print(f"Read domain and CNAME: {domain_pair}")
        return domains
    except FileNotFoundError:
        print(f"{file_name} not found!")
        return []


# 使用 nslookup查询IP
def nslookup(cname):
    try:
        # 使用subprocess运行nslookup
        result = subprocess.run(['nslookup', cname], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"nslookup command failed with: {result.stderr}")
            return None

        # 提取第一个IPv4地址
        pattern = r"Addresses:.*?(\d{1,3}(?:\.\d{1,3}){3})"
        match = re.search(pattern, result.stdout, re.DOTALL)
        if match:
            ipv4_address = match.group(1)
            print(f"First IPv4 address found for {cname}: {ipv4_address}")
            return ipv4_address
        else:
            print(f"No IPv4 address found for {cname}.")
            return None
    except Exception as e:
        print(f"Error during nslookup for {cname}: {e}")
        return None


# 测试输出块, 打印nslookup的输出
"""
def nslookuptest(cname):
    try:
        result = subprocess.run(['nslookup', cname], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"nslookup command failed with: {result.stderr}")
            return None

        print("Complete output:")
        print(result.stdout)

        return None
    except Exception as e:
        print(f"Error during nslookup for {cname}: {e}")
        return None
"""


# 获取证书信息
def get_certificate_serial_number(ip, hostname, port=443):
    try:
        context = ssl.create_default_context()
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # 禁用 TLS 1.0 和 1.1
        context.check_hostname = False  # 禁用主机名检查

        with socket.create_connection((ip, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
                cert = sslsock.getpeercert(binary_form=True)
                x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, cert)
                serial_number = x509.get_serial_number()
                return format(serial_number, 'X')
    except Exception as e:
        print(f"Error fetching SSL certificate for {hostname} ({ip}): {e}")
        return None


# main
def main():
    domains = read_domains_file('domains.txt')
    if not domains:
        return

    # 创建hosts_mapped.txt文件，保存域名CNAME和IP的映射关系
    with open('hosts_mapped.txt', 'w') as f_out, open('result.txt', 'w') as f_cert:
        for domain, cname in domains:
            print(f"Looking up {cname} (CNAME) for domain {domain}...")
            ip = nslookup(cname)
            if ip:
                print(f"Resolved IP for {cname} (CNAME): {ip}")
                f_out.write(f"{ip}\t{domain}\n")

                # 检查SSL证书
                serial_number = get_certificate_serial_number(ip, domain)
                if serial_number:
                    cert_info = f"Domain: {domain}, CertNumber: {serial_number}"
                    print(cert_info)
                    f_cert.write(cert_info + "\n")
                else:
                    error_info = f"ERROR: Could not retrieve SSL certificate for {domain} ({ip})"
                    print(error_info)
                    f_cert.write(error_info + "\n")

            else:
                ipmap_error_info = f"ERROR: Could not resolve IP for {cname}, domain name is {domain}"
                print(ipmap_error_info)
                f_cert.write(ipmap_error_info + "\n")


if __name__ == "__main__":
    main()
    # nslookuptest(”example“)

# Version 1.0.1
# Copyright (c) 2024 ChaoDang
'''
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
