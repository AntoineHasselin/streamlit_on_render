import pandas as pd


class date_search:

    def __init__(self, data, date):
        self.data = data
        self.date = date
        self.statut = False

    @staticmethod
    def format_str_to_date(date_to_format, _type: str = 'd-m-y'):
        import datetime
        if _type == 'd/m/y':
            return datetime.datetime.strptime(date_to_format, '%d-%m-%Y')

        elif _type == 'm/d/y':
            return datetime.datetime.strptime(date_to_format, '%m-%d-%Y')

        elif _type == 'y/m/d':
            return datetime.datetime.strptime(date_to_format, '%Y-%m-%d')

        elif _type == 'y/d/m':
            return datetime.datetime.strptime(date_to_format, '%Y-%d-%m')

        else:
            return datetime.datetime.strptime(date_to_format, '%d/%m/%Y')

    def return_date_exist(self):
        import datetime

        data: pd.DataFrame = self.data
        date: str = self.date
        column_name = 'Close'

        unknow_date = False

        # -----------------------------------------------------------------

        def _range_proxy_date():

            max_date = self.data.index.max()
            min_date = self.data.index.min()
            date_range_proxy = datetime.datetime.strptime(str(self.date), '%Y-%m-%d')

            delta_days = {'min_date': date_range_proxy - min_date,
                          'max_date': date_range_proxy - max_date}

            best_delta_date = min(delta_days.values())

            def find_key(dict_look, v):
                for k, val in dict_look.items():
                    if v == val:
                        return k
                return "Clé n'existe pas"

            date_to_take = find_key(delta_days, best_delta_date)

            return max_date if date_to_take == 'max_date' else min_date

        # -----------------------------------------------------------------

        def format_str_to_date(date_to_format, type: str = 'd/m/y'):

            if type == 'd/m/y':
                return datetime.datetime.strptime(date_to_format, '%d/%m/%Y')

            elif type == 'm/d/y':
                return datetime.datetime.strptime(date_to_format, '%m/%d/%Y')

            elif type == 'y/m/d':
                return datetime.datetime.strptime(date_to_format, '%Y/%m/%d')

            elif type == 'y/d/m':
                return datetime.datetime.strptime(date_to_format, '%Y/%d/%m')

            else:
                return datetime.datetime.strptime(date_to_format, '%d/%m/%Y')

        # -----------------------------------------------------------------

        def _bool_date_exist(data: pd.DataFrame, date: str) -> bool:

            try:
                data.loc[date][column_name][0]
                return True

            except:
                return False

        # ----------------------------------------------------------------

        def _search_proxy_date(data, date):
            i, running = 0, True

            while running:
                date_register = date + datetime.timedelta(i)
                i += 1

                if _bool_date_exist(data, str(date_register)[:10]):
                    running = False
                    return datetime.datetime.strftime(date_register, '%Y-%m-%d')

                elif i > 20:

                    running = False
                    unknow_date = True
                    return _range_proxy_date()

                else:
                    pass

        # -----------------------------------------------------------------

        if _bool_date_exist(data, date) is True:
            return date

        elif _bool_date_exist(data, date) is False:

            date_format = str(date)[8:10] + '/' + str(date)[5:7] + '/' + str(date)[:4]
            date_cal = format_str_to_date(date_format)
            date_register = date_cal
            i, running = 0, True
            assignment = False

            # ------------------------------------------------------------

            while running:
                date_register = date_register - datetime.timedelta(i)
                i += 1

                if _bool_date_exist(data, str(date_register)[:10]) is True:

                    running = False
                    return datetime.datetime.strftime(date_register, '%Y-%m-%d')

                elif i > 10:

                    running = False
                    assignment = True

                else:
                    pass

            if assignment:
                self.statut = True
                return _search_proxy_date(data, date_cal)

            # -------------------------------------------------------------

        else:
            print('Error function date')


"""

Exemple de code : 

date_look = date_search(data, '1999-01-01')
get_date = date_look._return_date_exist()
date_look.statut

"""