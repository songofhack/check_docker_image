import argparse
import re
import sys


class VulnDBCLIParser:

    # -- Public methods

    # CVEDBCLIParser Constructor
    def __init__(self):
        super(VulnDBCLIParser, self).__init__()
        self.parser = argparse.ArgumentParser(prog='vuln_db.py', description='Your personal CVE/BID database.')
        self.parser.add_argument('--init', action='store_true',
                                 help='initializes your local database with all CVEs provided by NIST publications and '
                                      'with all BugTraqs Ids (BIDs) downloaded from the "http://www.securityfocus.com/" '
                                      'pages (See my project "bidDB_downloader" '
                                      '[https://github.com/eliasgranderubio/bidDB_downloader] for details). '
                                      'If this argument is present, first all CVEs/BIDs of your local database will be '
                                      'removed and then, will be inserted again with all updated CVEs/BIDs.')
        self.parser.add_argument('--bid', type=int,
                                 help='all product with this BugTraq Id (BID) vulnerability will be shown')
        self.parser.add_argument('--cve', help='all products with this CVE vulnerability will be shown')
        self.parser.add_argument('--product', help='all CVE/BID vulnerabilities of this product will be shown')
        self.parser.add_argument('--product_version',
                                 help='extra filter for product query about its CVE/BID vulnerabilities. If this '
                                      'argument is present, the "--product" argument must be present too')
        self.parser.add_argument('--only_check', action='store_true',
                                 help='only checks if "--product" with "--product_version" has CVE/BID vulnerabilities '
                                      'but they will not be shown')
        self.parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0',
                                 help='show the version message and exit')
        self.args = self.parser.parse_args()
        self.__verify_args()

    # -- Getters

    # Gets if initialization is required
    def is_initialization_required(self):
        return self.args.init

    # Gets if product check is requested
    def is_only_product_check(self):
        return self.args.only_check

    # Gets CVE value
    def get_cve(self):
        return self.args.cve

    # Gets BID value
    def get_bid(self):
        return self.args.bid

    # Gets the product
    def get_product(self):
        return self.args.product

    # Gets the product version
    def get_product_version(self):
        return self.args.product_version

    # -- Private methods

    # Verify command line arguments
    def __verify_args(self):
        if not self.args.init and not self.args.only_check and not self.args.cve and not self.args.product \
                and not self.args.product_version and not self.args.bid:
            print(self.parser.prog + ': error: missing arguments.', file=sys.stderr)
            exit(1)
        elif self.args.init and (self.args.only_check or self.args.cve or self.args.product \
                                 or self.args.product_version or self.args.bid):
            print(self.parser.prog + ': error: argument --init: this argument must be alone.', file=sys.stderr)
            exit(1)
        elif self.args.cve:
            if self.args.init or self.args.only_check or self.args.product or self.args.product_version or \
                    self.args.bid:
                print(self.parser.prog + ': error: argument --cve: this argument must be alone.', file=sys.stderr)
                exit(1)
            else:
                regex = r"(CVE-[0-9]{4}-[0-9]{4})"
                search_obj = re.search(regex, self.args.cve)
                if not search_obj or len(search_obj.group(0)) != len(self.args.cve):
                    print(self.parser.prog + ': error: argument --cve: The cve format must look like to CVE-2002-1234.',
                          file=sys.stderr)
                    exit(2)
        elif self.args.bid:
            if self.args.init or self.args.only_check or self.args.product or self.args.product_version or \
                    self.args.cve:
                print(self.parser.prog + ': error: argument --bid: this argument must be alone.', file=sys.stderr)
                exit(1)
            else:
                if self.args.bid <= 0:
                    print(self.parser.prog + ': error: argument --bid: The bid argument must be greater than zero.',
                          file=sys.stderr)
                    exit(2)
        elif (self.args.product_version or self.args.only_check) and not self.args.product:
            print(self.parser.prog + ': error: arguments --product_version/--only_check: these arguments requiere the '
                                     '--product argument.', file=sys.stderr)
            exit(1)
