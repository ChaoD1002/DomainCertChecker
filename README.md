# Domain SSL Verification Tool

This tool automates the process of fetching IP addresses for domains using their CNAMEs and checks the SSL certificates associated with these domains.

## Version 1.0.1 Update
- Added Error output directly into result.txt

## Features

- Resolve IPv4 addresses for domain names via CNAME lookup.
- Retrieve and display SSL certificate serial numbers for the resolved IP addresses.
- Outputs the IP and domain relationship and SSL certificate details to text files.

## Requirements

- Python 3.x
- OpenSSL library
	+ You can find more information about the usage of OpenSSL here, including how to output the certificate's expiration date and other details, to modify the get_certificate_serial_number function in the code for application in more scenarios. **https://docs.openssl.org/3.0/man1/openssl-x509/**
- subprocess, ssl, socket, re Python modules (usually included with standard Python installation)

## Installation

Clone this repository or download the script directly. Ensure that you have Python installed on your system. To install Python, visit:

https://www.python.org/downloads/

To install required Python libraries, run the following command:

bash
pip install pyOpenSSL


## Usage

Ensure that domains.txt is in the same directory as the script or modify the script to point to the correct path. 
**The domains.txt should contain domains and their respective CNAMEs separated by a tab, one pair per line.**
+ You can find the Domain - CNAME pairs at the group shared files or email attachments.

Example domains.txt content:

**example.com	cdn.example.com**

**anotherdomain.com	cdn.anotherdomain.com**

Run the script from the command line:

python domainCertChecker.py


The script will output results to hosts_mapped.txt and result.txt:

+ hosts_mapped.txt will contain resolved IPs and domains.
+ result.txt will contain SSL certificate number for these domains, and the error information if the scrpit cannot work with the domain-cname pair.
+ You can find the excepted cert number at the group shared files.

## Troubleshooting

+ Ensure that all domains in domains.txt are correctly formatted and accessible.
+ Check Python and OpenSSL installation if you encounter any errors related to missing libraries.
+ If nslookup fails, ensure your internet connection is active and the domain names are correct.

## MIT License

Copyright (c) 2024 ChaoDang

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
