import copy
import unicodedata
from scrapy.utils.project import get_project_settings
import pandas as pd
import scrapy
from loginform import fill_login_form
from scrapy import Request
from zoneboursescrapper.utils.DataFormatter import DataFormatter
from zoneboursescrapper.utils.HtmlSaver import HtmlSaver
from bs4 import BeautifulSoup
import re
import lxml
from zoneboursescrapper.utils.TableParser import TableParser
from copy import deepcopy
from itertools import chain

from zoneboursescrapper.utils.ZBNumHelper import ZBNumHelper
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class ZoneboursespiderSpider(scrapy.Spider):
    name = 'zoneboursespider'
    allowed_domains = ['zonebourse.com']
    start_urls = []

    login_url = 'https://www.zonebourse.com/login/'

    login_user = 'forestfenghan@gmail.com'
    login_password = '111aaaAAA'

    def init_gspread(self):
        """TODO: Get companies to crawl from google sheet"""

        creds = None
        settings = get_project_settings()

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', settings.get('SCOPES'))
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', settings.get('SCOPES'))
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('sheets', 'v4', credentials=creds)
        self.output_sheet = self.service.spreadsheets()

        return ['ADOMOS-34555345',
                'AS-RAPIDO-PRET-19344321',
                '2CRSI-44358422',
                'AMOEBA-112388609',
                'CARREFOUR-4626',
                'CLARANOVA-SE-63216172',
                'DERICHEBOURG-4680',
                'ENERTIME-29688253',
                'EUTELSAT-COMMUNICATIONS-5147',
                'FERMENTALG-16118042',
                'FFP-4731',
                'GROUPE-LDLC-5107',
                'GROUPE-TERA-SA-61871287',
                'HF-COMPANY-5154',
                'HIPAY-GROUP-SA-23160245',
                'IMMERSION-25531721',
                'INNELEC-MULTIMEDIA-5076',
                'INVENTIVA-S-A-34031212',
                'KALRAY-S-A-44172573',
                'KERLINK-SA-27472140',
                'LYSOGENE-33951021',
                'MAKHEIA-GROUP-5091',
                'MCPHY-ENERGY-15933338',
                'NEURONES-5213',
                'NRJ-GROUP-4678',
                'ONCODESIGN-16113765',
                'QUADIENT-S-A-4674',
                'SCHNEIDER-ELECTRIC-SE-4699',
                'SOLOCAL-GROUP-24706781',
                'SUEZ-SA-3729241',
                'TF1-4714',
                'VALNEVA-SE-54466',
                'VERIMATRIX-60857003',
                'VISIATIV-16579012',
                'VOLUNTIS-43536396',
                'WITBE-27100924',
                'AB-VOLVO-6492152',
                'ABC-ARBITRAGE-5094',
                'ABIVAX-22387984',
                'ACCELL-GROUP-N-V-6310',
                'ADOCIA-9894600',
                'ADOCIA-9894600',
                'AHOLD-DELHAIZE-N-V-29752127',
                'AIRBUS-SE-4637',
                'AKKA-TECHNOLOGIES-SE-5129',
                'AKWEL-5052',
                'ALFEN-N-V-42452474',
                'ALSTOM-4607',
                'ALTAREA-5310',
                'AMUNDI-24827105',
                'ARCURE-55074783',
                'ASM-INTERNATIONAL-N-V-6312',
                'ATEME-16917716',
                'ATOS-SE-4612',
                'AUBAY-4706',
                'AURELIUS-EQUITY-OPPORTUNI-494695',
                'AURES-TECHNOLOGIES-28836488',
                'AURUBIS-436439',
                'AUSTEVOLL-SEAFOOD-ASA-1413089',
                'AXA-4615',
                'AXWAY-SOFTWARE-8174242',
                'BAIKOWSKI-49690175',
                'BALYO-35742472',
                'BASTIDE-LE-CONFORT-MEDICA-5023',
                'BATLA-MINERALS-50259',
                'BAVARIAN-NORDIC-A-S-1412846',
                'BETSSON-AB-58602255',
                'BHG-GROUP-AB-42529103',
                'BIGBEN-INTERACTIVE-5097',
                'BIOCORP-22824766',
                'BIOMERIEUX-37839085',
                'BIOPHYTIS-22837372',
                'BNP-PARIBAS-4618',
                'BOLLORE-SE-5155',
                'BONDUELLE-4730',
                'BONHILL-GROUP-PLC-45344010',
                'BOUYGUES-4620',
                'BPOST-SA-16193932',
                'CABASSE-GROUP-113108841',
                'CAPELLI-24301201',
                'CARBIOS-15262917',
                'CASINO-GUICHARD-PERRACHO-4627',
                'CAST-SA-5183',
                'CATANA-GROUP-5130',
                'CLARANOVA-SE-63216172',
                'COLAS-5225',
                'COVIVIO-HOTELS-5707',
                'CYAN-AG-42547867',
                'DAIMLER-AG-436541',
                'DBT-25531686',
                'DBV-TECHNOLOGIES-10189744',
                'DELTA-PLUS-GROUP-37879274',
                'DERICHEBOURG-4680',
                'DEUTSCHE-BORSE-AG-449617',
                'DEVOTEAM-S-A-4751',
                'EDENRED-6365724',
                'ENGIE-4995',
                'ESKER-6527812',
                'EUROFINS-SCIENTIFIC-SE-4753',
                'EUROMEDIS-GROUPE-5106',
                'EURONEXT-N-V-16725768',
                'EUTELSAT-COMMUNICATIONS-5147',
                'FASTNED-B-V-60225995',
                'FERMENTALG-16118042',
                'FFP-4731',
                'FIGEAC-AERO-17903015',
                'FIRST-SENSOR-AG-436573',
                'FLATEXDEGIRO-AG-31637144',
                'FLEURY-MICHON-107188193',
                'FNAC-DARTY-13449504',
                'FOCUS-HOME-INTERACTIVE-20757389',
                'GALAPAGOS-NV-6464',
                'GL-EVENTS-5696',
                'GROUPE-LDLC-5107',
                'GROUPE-TERA-SA-61871287',
                'GTT-GAZTRANSPORT-ET-TEC-15821825',
                'GUERBET-S-A-5011',
                'HEINEKEN-N-V-6283',
                'HELLA-GMBH-CO-KGAA-18474990',
                'HELLOFRESH-SE-38533857',
                'HIPAY-GROUP-SA-23160245',
                'IBERDROLA-S-A-355153',
                'ILIAD-S-A-4765',
                'IMMERSION-25531721',
                'INFOTEL-SA-5167',
                'INIT-INNOVATION-IN-TRAFFI-451128',
                'INNATE-PHARMA-35620',
                'INNELEC-MULTIMEDIA-5076',
                'INVENTIVA-S-A-34031212',
                'INVESTMENT-AB-LATOUR-PUB-35868236',
                'IPSEN-5137',
                'IPSOS-SA-4663',
                'IT-LINK-SA-5203',
                'JACQUET-METALS-5015',
                'KAUFMAN-BROAD-4768',
                'KERLINK-SA-27472140',
                'KONE-OYJ-1412480',
                'LA-FRANCAISE-DE-L-ENERGIE-28643001',
                'LACROIX-GROUP-5782',
                'LAFARGEHOLCIM-LTD-2956274',
                'LDC-31531420',
                'LINEDATA-SERVICES-SA-4770',
                'LLEIDANETWORKS-SERVEIS-TE-105515008',
                'LVMH-MOET-HENNESSY-LOUI-4669',
                'MAISONS-DU-MONDE-27862556',
                'MAKHEIA-GROUP-5091',
                'MANITOU-GROUP-4773',
                'MANUTAN-INTERNATIONAL-5211',
                'MCPHY-ENERGY-15933338',
                'MEDIAWAN-34473581',
                'MEMSCAP-16275',
                'MERCIALYS-5135',
                'MERCK-KGAA-436395',
                'MERSEN-9632901',
                'METROPOLE-TELEVISION-4670',
                'MINT-33822',
                'NACON-103932529',
                'NAVYA-44995305',
                'NEOEN-46633605',
                'NETGEM-4779',
                'NEXANS-4676',
                'NOVACYT-11681992',
                'NRJ-GROUP-4678',
                'OCTOPUS-BIOSAFETY-42379370',
                'ONCODESIGN-16113765',
                'ORANGE-4649',
                'ORAPI-5395',
                'OSE-IMMUNOTHERAPEUTICS-21120309',
                'POSTNL-N-V-8070432',
                'PREDILIFE-49553833',
                'PRISMAFLEX-INTERNATIONAL-5169',
                'PROSUS-N-V-66148584',
                'QUADIENT-S-A-4674',
                'QUANTUM-GENOMICS-16253203',
                'QUANTUM-GENOMICS-16253203',
                'RENAULT-4688',
                'RENO-DE-MEDICI-S-P-A-69034',
                'REPLY-S-P-A-38135655',
                'ROTHSCHILD-CO-5306',
                'SAMSE-5703',
                'SANOFI-4698',
                'SARTORIUS-STEDIM-BIOTECH-27471609',
                'SENSORION-21685779',
                'SERGEFERRARI-GROUP-16617776',
                'SESA-S-P-A-8253632',
                'SHOP-APOTHEKE-EUROPE-N-V-31620967',
                'SIGNIFY-N-V-27862555',
                'SOLOCAL-GROUP-24706781',
                'SOLUTIONS-30-SE-47041212',
                'SOMEC-S-P-A-43371375',
                'SOMFY-SA-31472055',
                'SOPRA-STERIA-GROUP-4707',
                'STMICROELECTRONICS-N-V-4710',
                'STRATEC-SE-23566602',
                'SUEZ-SA-3729241',
                'SWORD-GROUP-SE-5125',
                'TESSI-5041',
                'TF1-4714',
                'THALES-4715',
                'THERMADOR-GROUPE-43328026',
                'TIKEHAU-CAPITAL-34204863',
                'TIVOLY-5716',
                'TRIGANO-4718',
                'VALEO-27891158',
                'VALNEVA-SE-54466',
                'VAN-LANSCHOT-KEMPEN-N-V-6308',
                'VELCAN-HOLDINGS-SA-9426811',
                'VERALLIA-67015802',
                'VERIMATRIX-60857003',
                'VETOQUINOL-SA-36676',
                'VICAT-5009',
                'VINCI-SA-4725',
                'VIRBAC-5234',
                'VISCOFAN-S-A-75245',
                'VISIATIV-16579012',
                'VISIOMED-GROUP-8235236',
                'VIVENDI-SE-4727',
                'VOLUNTIS-43536396',
                'VOYAGEURS-DU-MONDE-32742',
                'WALLSTREET-ONLINE-AG-38481136',
                'WENDEL-4671',
                'WITBE-27100924',
                'X-FAB-SILICON-FOUNDRIES-S-34491290',
                'ZOOPLUS-AG-3015215',
                'ARCURE-55074783',
                'CAPELLI-24301201',
                'DBT-25531686',
                'DBV-TECHNOLOGIES-10189744']

    def start_requests(self):
        for i in self.init_gspread():
            self.start_urls.append("https://www.zonebourse.com/cours/action/" + i + "/")
        yield scrapy.Request(self.login_url, self.parse_login, dont_filter=True)

    def parse_login(self, response):
        data, url, method = fill_login_form(response.url, response.body,
                                            self.login_user, self.login_password)

        return scrapy.FormRequest(url, formdata=dict(data),
                                  method=method, callback=self.start_crawl)

    def start_crawl(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse_page1, dont_filter=True)

    def parse_page1(self, response):
        url = response.request.url
        link_to_company = url
        company_name = link_to_company.split("/action/")[-1].strip("/")
        html_saver = HtmlSaver(company_name=company_name, to_dir="saved_html")
        soup = BeautifulSoup(response.body.decode('utf-8', 'ignore'), 'lxml')
        html_saver.save_html(response, 1)
        data_dict = {}

        try:
            page1_table = soup.find("script", text=re.compile(".*function.*dfCurr.*")).find_next_sibling("table")
            for span_dfUSD_tag in page1_table.find_all("span", {'class', re.compile(".*dfUSD.*")}):
                span_dfUSD_tag.replace_with("")
            for span_dfEdCurr_tag in page1_table.find_all("span", {'class', re.compile(".*dfEdCurr.*")}):
                span_dfEdCurr_tag.replace_with("")

            dflist = []
            for t in page1_table.find_all("table"):
                dflist += TableParser.read_html(unicodedata.normalize("NFKD", t.prettify()))

            for i in dflist:
                data_dict = {**data_dict, **i.set_index(0).to_dict()[1]}

            data_dict = {**{
                'NOM': DataFormatter.get_text(soup.find("h1", {"style": re.compile(".+bold.+")})),
                'MNEMO': DataFormatter.get_text(soup.find("span", {'onclick': re.compile(".+code.+nemo.+")})),
                'LINK': link_to_company,
                'CODE': DataFormatter.get_text(soup.find("span", {'onclick': re.compile(".+code.+in.+")})),
                'PRICE': DataFormatter.get_text(soup.find("td", {'class', re.compile('.*fvPrice.+')})),
                'DEVISE': DataFormatter.get_text(soup.find("div", {'class': 'dfCCl'}).findChild("option", {'value': 'Cur'})),
                'UNIT': DataFormatter.get_text(soup.find("*", {'class', 'dfCur'}), error=['-'])[-1],
                'SECTEUR': DataFormatter.get_text(soup.find("a", {'href': re.compile(".+secteur.+")})),
                'DATE OF AGENDA': DataFormatter.get_text(soup.find("b", text=re.compile("Agenda")).find_parent("td").find("td", text=re.compile("\d\d\/\d\d"))),
                'TITLE OF AGENDA': DataFormatter.get_text(soup.find("b", text=re.compile("Agenda")).find_parent("td").find("td", {'class': 'newsColCT'}))
            }, **data_dict}
        except:
            data_dict = {**{'LINK': link_to_company}, **data_dict}

        yield scrapy.Request(url + "societe/", self.parse_page2, meta={'link_to_company': url, 'data': DataFormatter.format(data_dict)}, dont_filter=True)

    def parse_page2(self, response):
        data_dict = response.meta['data']
        link_to_company = response.meta['link_to_company']
        url = response.request.url
        company_name = link_to_company.split("/action/")[-1].strip("/")
        html_saver = HtmlSaver(company_name=company_name, to_dir="saved_html")
        soup = BeautifulSoup(response.body.decode('utf-8', 'ignore'), 'lxml')
        html_saver.save_html(response, 2)

        try:
            page2_table = soup.find("td", text=re.compile(".*tier.*")).find_parent("table").find_parent("table")

            for table in page2_table.find_all("table"):
                table.replace_with("")

            dflist = TableParser.read_html(unicodedata.normalize("NFKD", page2_table.prettify()))
            data_dict = {**data_dict, **{
                "Métier": dflist[0].to_dict()[0][0]
            }}
        except:
            data_dict = {**data_dict, **{
                "Métier": "-"
            }}

        yield scrapy.Request(link_to_company + "fondamentaux/", self.parse_page3, meta={'link_to_company': link_to_company, 'data': DataFormatter.format(data_dict)}, dont_filter=True)

    def parse_page3(self, response):
        data_dict = response.meta['data']
        url = response.request.url
        link_to_company = response.meta['link_to_company']
        company_name = link_to_company.split("/action/")[-1].strip("/")
        html_saver = HtmlSaver(company_name=company_name, to_dir="saved_html")
        soup = BeautifulSoup(response.body.decode('utf-8', 'ignore'), 'lxml')
        html_saver.save_html(response, 3)

        try:
            page3_tables = []
            for i in soup.find_all("table", {'class': re.compile(".*BordCollapseYear.*")}):
                page3_tables += TableParser.read_html(i.prettify())

            for count, value in enumerate(page3_tables):
                page3_tables[count] = page3_tables[count].set_index(0)
                page3_tables[count].columns = page3_tables[count].iloc[0]
                page3_tables[count] = page3_tables[count][1:]

            page3_data_dict = {}
            for i in page3_tables:
                page3_data_dict = {**page3_data_dict, **i.T.to_dict("dict")}

            for key, value in deepcopy(page3_data_dict).items():
                if 'EUR en Millions' in key:
                    page3_data_dict.pop(key)
                elif key[-1] == "1":
                    page3_data_dict.pop(key)
                    page3_data_dict[key[:-1]] = value
                elif key[-1] == "2":
                    page3_data_dict.pop(key)
                    page3_data_dict[key[:-1]] = value

            data_dict = {**data_dict, **TableParser.flatten(page3_data_dict)}
        except:
            data_dict = {**data_dict, **{}}

        yield scrapy.Request(link_to_company + "consensus/", self.parse_page4, meta={'link_to_company': url, 'data': DataFormatter.format(data_dict)}, dont_filter=True)

    def parse_page4(self, response):
        data_dict = response.meta['data']
        link_to_company = response.meta['link_to_company']
        company_name = link_to_company.split("/action/")[-1].strip("/")
        html_saver = HtmlSaver(company_name=company_name, to_dir="saved_html")
        soup = BeautifulSoup(response.body.decode('utf-8', 'ignore'), 'lxml')
        html_saver.save_html(response, 4)

        try:
            page4_table = soup.find("table", {'class': re.compile(".*Bord.*")})

            page4_data_dict = TableParser.read_html(page4_table.prettify())[0].set_index(0).to_dict("dict")[1]

            data_dict = {**data_dict, **page4_data_dict}
        except:
            data_dict = {**data_dict, **{}}

        for key, value in data_dict.items():
            converted = value

            value = str(value)

            dateDM = re.findall(r"^\d\d/\d\d$", value)
            dateDMY = re.findall(r"^\d\d/\d\d/\d\d\d\d$", value)
            number = re.findall(r"^[-\d ,]+[x%MKB]*$", value)
            euro_sign = re.findall(r".*\xa0€.*", value)

            if euro_sign:
                converted = float(ZBNumHelper.pn(value.strip("").replace("\xa0€", "")))
            elif dateDMY:
                converted = ZBNumHelper.pdtDMY(value)
            elif dateDM:
                converted = ZBNumHelper.pdtDM(value)
            elif number:
                just_number = re.findall(r"^[-\d ,]+$", value)
                reduced_precision_number = re.findall(r"^[-\d ,]+[MKB]$", value)

                multiplication_number = re.findall(r"^[-\d ,]+[x]$", value)
                percentage_number = re.findall(r"^[-\d ,]+[%]$", value)

                if reduced_precision_number:
                    converted = ZBNumHelper.prpn(value)
                elif multiplication_number:
                    converted = ZBNumHelper.pmn(value)
                elif percentage_number:
                    converted = ZBNumHelper.ppn(value)
                elif just_number:
                    converted = ZBNumHelper.pn(value)

            data_dict[key] = converted

        yield data_dict
