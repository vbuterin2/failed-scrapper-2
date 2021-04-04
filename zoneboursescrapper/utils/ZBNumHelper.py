from datetime import datetime


class ZBNumHelper:
    @staticmethod
    def nf():
        return "-"

    @staticmethod
    def pn(ns):
        """process number string"""
        """'1,23' -> 123"""
        try:
            ns = ns.replace(",", ".")
            ns = ns.replace(" ", "")
            return float(ns)
        except Exception as e:
            return ZBNumHelper.nf()

    @staticmethod
    def pdtDMY(dt):
        """process datetime (Date/Month/Year)"""
        try:
            return datetime.strptime(str(dt), "%d/%m/%Y").strftime("%Y-%m-%d %H:%M:%S.%f")
        except Exception as e:
            return ZBNumHelper.nf()

    @staticmethod
    def pdtDM(dt):
        """process datetime (Date/Month)"""
        try:
            return datetime.strptime(str(dt) + "/2021", "%d/%m/%Y").strftime("%Y-%m-%d %H:%M:%S.%f")
        except Exception as e:
            return ZBNumHelper.nf()

    @staticmethod
    def pde(df):
        """process data entry"""
        if len(df) == 2:
            return df
        elif len(df) == 1:
            return [df[0], ZBNumHelper.nf()]
        else:
            raise Exception("DEBUG: pde ƒ error. ")

    @staticmethod
    def prpn(rrn):
        """process_reduced_precision_number"""
        """3,31 M => 331000000"""

        try:
            rrn = rrn.replace(",", ".").replace(" ", "")
        except Exception as e:
            return ZBNumHelper.nf()

        try:
            n = float(rrn[:-1].strip(""))

            if "K" in rrn[-1]:
                n = n * 1000
            elif "M" in rrn[-1]:
                n = n * 1000 * 1000
            elif "B" in rrn[-1]:
                n = n * 1000 * 1000 * 1000

            return n
        except Exception as e:
            return ZBNumHelper.nf()

    @staticmethod
    def pmn(mn):
        """process_multiplication_number"""
        """-14,0x => 331"""
        try:
            mn = str(mn).strip("").replace(",", ".")
            mn = str(mn).replace(" ", "")
            mn = float(str(mn).replace("x", ""))

            return mn
        except Exception as e:
            return ZBNumHelper.nf()

    @staticmethod
    def ppn(pn):
        """process_percentage_number"""
        """98,8% -> float: 98.8"""
        try:
            pn = str(pn).strip("").replace(",", ".").replace("%", "").replace(" ", "")
            return float(pn)
        except Exception as e:
            return ZBNumHelper.nf()
