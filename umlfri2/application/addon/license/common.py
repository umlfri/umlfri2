from collections import namedtuple


def osi_license_url(abbreviation):
    return "https://opensource.org/licenses/{0}".format(abbreviation)


class CommonLicense:
    __LicenseDescription = namedtuple('LicenseDescription', ('title', 'url', 'abbreviation'))
    
    __LICENSES = {
        "afl-3": __LicenseDescription("Academic Free License 3.0", osi_license_url, "AFL-3.0"),
        "agpl-3": __LicenseDescription("GNU Affero General Public License 3.0", osi_license_url, "AGPL-3.0"),
        "apl-1": __LicenseDescription("Adaptive Public License", osi_license_url, "APL-1.0"),
        "apache-2": __LicenseDescription("Apache License 2.0", osi_license_url, "Apache-2.0"),
        "apsl-2": __LicenseDescription("Apple Public Source License", osi_license_url, "APSL-2.0"),
        "artistic-2": __LicenseDescription("Artistic license 2.0", osi_license_url, "Artistic-2.0"),
        "aal": __LicenseDescription("Attribution Assurance Licenses", osi_license_url, "AAL"),
        "bsd-3-clause": __LicenseDescription("BSD 3-Clause \"New\" or \"Revised\" License", osi_license_url, "BSD-3-Clause"),
        "bsd-2-clause": __LicenseDescription("BSD 2-Clause \"Simplified\" or \"FreeBSD\" License", osi_license_url, "BSD-2-Clause"),
        "bsl-1": __LicenseDescription("Boost Software License", osi_license_url, "BSL-1.0"),
        "cecill-2.1": __LicenseDescription("CeCILL License 2.1", osi_license_url, "CECILL-2.1"),
        "catosl-1.1": __LicenseDescription("Computer Associates Trusted Open Source License 1.1", osi_license_url, "CATOSL-1.1"),
        "cddl-1": __LicenseDescription("Common Development and Distribution License 1.0", osi_license_url, "CDDL-1.0"),
        "cpal-1": __LicenseDescription("Common Public Attribution License 1.0", osi_license_url, "CPAL-1.0"),
        "cua-opl-1": __LicenseDescription("CUA Office Public License Version 1.0", osi_license_url, "CUA-OPL-1.0"),
        "eudatagrid": __LicenseDescription("EU DataGrid Software License", osi_license_url, "EUDatagrid"),
        "epl-1": __LicenseDescription("Eclipse Public License 1.0", osi_license_url, "EPL-1.0"),
        "ecos-2": __LicenseDescription("eCos License version 2.0", osi_license_url, "eCos-2.0"),
        "ecl-2": __LicenseDescription("Educational Community License, Version 2.0", osi_license_url, "ECL-2.0"),
        "efl-2": __LicenseDescription("Eiffel Forum License V2.0", osi_license_url, "EFL-2.0"),
        "entessa": __LicenseDescription("Entessa Public License", osi_license_url, "Entessa"),
        "eupl-1.1": __LicenseDescription("European Union Public License, Version 1.1", osi_license_url, "EUPL-1.1"),
        "fair": __LicenseDescription("Fair License", osi_license_url, "Fair"),
        "frameworx-1": __LicenseDescription("Frameworx License", osi_license_url, "Frameworx-1.0"),
        "fpl-1": __LicenseDescription("Free Public License 1.0.0", osi_license_url, "FPL-1.0.0"),
        "gpl-2": __LicenseDescription("GNU General Public License version 2.0", osi_license_url, "GPL-2.0"),
        "gpl-3": __LicenseDescription("GNU General Public License version 3.0", osi_license_url, "GPL-3.0"),
        "lgpl-2.1": __LicenseDescription("GNU Library or \"Lesser\" General Public License version 2.1", osi_license_url, "LGPL-2.1"),
        "lgpl-3": __LicenseDescription("GNU Library or \"Lesser\" General Public License version 3.0", osi_license_url, "LGPL-3.0"),
        "hpnd": __LicenseDescription("Historical Permission Notice and Disclaimer", osi_license_url, "HPND"),
        "ipl-1": __LicenseDescription("IBM Public License 1.0", osi_license_url, "IPL-1.0"),
        "ipa": __LicenseDescription("IPA Font License", osi_license_url, "IPA"),
        "isc": __LicenseDescription("ISC License", osi_license_url, "ISC"),
        "lppl-1.3c": __LicenseDescription("LaTeX Project Public License 1.3c", osi_license_url, "LPPL-1.3c"),
        "liliq-p-1.1": __LicenseDescription("Licence Libre du Québec - Permissive version 1.1", osi_license_url, "LiLiQ-P-1.1"),
        "liliq-r-1.1": __LicenseDescription("Licence Libre du Québec - Réciprocité version 1.1", osi_license_url, "LiLiQ-R-1.1"),
        "liliq-r+-1.1": __LicenseDescription("Licence Libre du Québec - Réciprocité forte version 1.1", osi_license_url, "LiLiQ-R+-1.1"),
        "lpl-1.02": __LicenseDescription("Lucent Public License Version 1.02", osi_license_url, "LPL-1.02"),
        "miros": __LicenseDescription("MirOS Licence", osi_license_url, "MirOS"),
        "ms-pl": __LicenseDescription("Microsoft Public License", osi_license_url, "MS-PL"),
        "ms-rl": __LicenseDescription("Microsoft Reciprocal License", osi_license_url, "MS-RL"),
        "mit": __LicenseDescription("MIT license", osi_license_url, "MIT"),
        "motosoto": __LicenseDescription("Motosoto License", osi_license_url, "Motosoto"),
        "mpl-2": __LicenseDescription("Mozilla Public License 2.0", osi_license_url, "MPL-2.0"),
        "multics": __LicenseDescription("Multics License", osi_license_url, "Multics"),
        "nasa-1.3": __LicenseDescription("NASA Open Source Agreement 1.3", osi_license_url, "NASA-1.3"),
        "ntp": __LicenseDescription("NTP License", osi_license_url, "NTP"),
        "naumen": __LicenseDescription("Naumen Public License", osi_license_url, "Naumen"),
        "ngpl": __LicenseDescription("Nethack General Public License", osi_license_url, "NGPL"),
        "nokia": __LicenseDescription("Nokia Open Source License", osi_license_url, "Nokia"),
        "nposl-3": __LicenseDescription("Non-Profit Open Software License 3.0", osi_license_url, "NPOSL-3.0"),
        "oclc-2": __LicenseDescription("OCLC Research Public License 2.0", osi_license_url, "OCLC-2.0"),
        "ogtsl": __LicenseDescription("Open Group Test Suite License", osi_license_url, "OGTSL"),
        "osl-3": __LicenseDescription("Open Software License 3.0", osi_license_url, "OSL-3.0"),
        "opl-2.1": __LicenseDescription("OSET Public License version 2.1", osi_license_url, "OPL-2.1"),
        "php-3": __LicenseDescription("PHP License 3.0", osi_license_url, "PHP-3.0"),
        "postgresql": __LicenseDescription("The PostgreSQL License", osi_license_url, "PostgreSQL"),
        "python-2": __LicenseDescription("Python License", osi_license_url, "Python-2.0"),
        "cnri-python": __LicenseDescription("CNRI Python license", osi_license_url, "CNRI-Python"),
        "qpl-1": __LicenseDescription("Q Public License", osi_license_url, "QPL-1.0"),
        "rpsl-1": __LicenseDescription("RealNetworks Public Source License V1.0", osi_license_url, "RPSL-1.0"),
        "rpl-1.5": __LicenseDescription("Reciprocal Public License 1.5", osi_license_url, "RPL-1.5"),
        "rscpl": __LicenseDescription("Ricoh Source Code Public License", osi_license_url, "RSCPL"),
        "ofl-1.1": __LicenseDescription("SIL Open Font License 1.1", osi_license_url, "OFL-1.1"),
        "simpl-2": __LicenseDescription("Simple Public License 2.0", osi_license_url, "SimPL-2.0"),
        "sleepycat": __LicenseDescription("Sleepycat License", osi_license_url, "Sleepycat"),
        "spl-1": __LicenseDescription("Sun Public License 1.0", osi_license_url, "SPL-1.0"),
        "watcom-1": __LicenseDescription("Sybase Open Watcom Public License 1.0", osi_license_url, "Watcom-1.0"),
        "ncsa": __LicenseDescription("University of Illinois/NCSA Open Source License", osi_license_url, "NCSA"),
        "upl": __LicenseDescription("Universal Permissive License", osi_license_url, "UPL"),
        "vsl-1": __LicenseDescription("Vovida Software License v. 1.0", osi_license_url, "VSL-1.0"),
        "w3c": __LicenseDescription("W3C License", osi_license_url, "W3C"),
        "wxwindows": __LicenseDescription("wxWindows Library License", osi_license_url, "WXwindows"),
        "xnet": __LicenseDescription("X.Net License", osi_license_url, "Xnet"),
        "zpl-2": __LicenseDescription("Zope Public License 2.0", osi_license_url, "ZPL-2.0"),
        "zlib": __LicenseDescription("zlib/libpng license", osi_license_url, "Zlib"),
    }
    
    def __init__(self, abbreviation):
        key = abbreviation.lower()
        if key in self.__LICENSES:
            description = self.__LICENSES[key]
            
            self.__abbreviation = description.abbreviation
            self.__title = description.title
            
            url = description.url
            if callable(url):
                url = url(description.abbreviation)
            self.__url = url
        else:
            self.__abbreviation = abbreviation
            self.__title = None
            self.__url = None
    
    @property
    def abbreviation(self):
        return self.__abbreviation
    
    @property
    def title(self):
        return self.__title
    
    @property
    def url(self):
        return self.__url
