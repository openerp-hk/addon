import calendar
import datetime
import time


class DateUtil:

    def get_days(self, begin_date, end_date):
        # 计算两个日期之间的天数
        if begin_date == end_date:
            return 1
        begin_date = datetime.datetime.strptime(begin_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        return (end_date - begin_date).days

    def get_between_day(self, begin_date, end_date):
        # 根据开始日期、结束日期计算出两个时间段之间的天数
        date_list = []
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        return date_list

    def get_bill_date(self, start_date_str):

        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        current_date = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date()

        if start_date.__le__(current_date):
            return 0

        return (start_date - current_date).days

    def get_between_month(self, begin_date, end_date):
        # 根据开始日期、结束日期计算出两个时间段之间的月
        date_array = []
        current_date = begin_date
        date_array.append(str(begin_date))
        while current_date.__lt__(end_date):
            last_date = current_date + datetime.timedelta(
                days=calendar.monthrange(current_date.year, current_date.month)[1])
            if last_date.__ge__(end_date):
                date_array.append(str(end_date))
            else:
                date_array.append(str(last_date))
            current_date = last_date

        return date_array

    def get_date_for_step(self, begin_date, end_date, step):
        # 根据开始日期、结束日期 步长来计算两个时间段之间的日期
        quarter_array = []
        # 计算出两个时间段之间的月分
        date_array = self.get_between_month(begin_date, end_date)
        if step == 1:
            return date_array

        # 根据步长计算出日期
        for i in range(0, len(date_array), step):
            quarter_array.append(date_array[i])

        if quarter_array[-1] != date_array[-1]:
            quarter_array.append(date_array[-1])
        return quarter_array

    def get_between_year(self, begin_date, end_date):
        # 根据开始日期、结束日期计算两个时间段之间的年
        year_array = []
        for year in range(begin_date.year, end_date.year + 1):
            year_array.append(str(year) + "-" + str(begin_date.month) + "-" + str(begin_date.day))
        return year_array

    def get_pay_date_data(self):
        """创建缴费日期数据"""
        pay_date_data = []
        for item in range(1, 29):
            pay_date_data.append((str(item), str(item) + "号"))
        return pay_date_data

    def get_date_for_month(self, date_str):
        # 获取日期的月份

        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        return str(date.month) + "月"

    def get_date_end_day(self, start_date_str, end_date_str, last_end_date):
        #
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()

        if start_date.month == end_date.month:
            return end_date

        if end_date.__eq__(last_end_date):
            return end_date
        else:
            return end_date + datetime.timedelta(days=(-1))

    def get_date_split(self, start_date, end_date):
        array = []
        if start_date.__lt__(end_date):
            array.append(str(start_date.strftime('%Y-%m-%d')))
            if start_date.day != 1:
                start_date_str = str(start_date.year) + "-" + str(start_date.month) + "-" + str(
                    calendar.monthrange(start_date.year, start_date.month)[1])
                current_start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d') + datetime.timedelta(days=1)
                array.append(start_date_str)
                array.append(str(current_start_date.date()))

            if end_date.day != calendar.monthrange(end_date.year, end_date.month)[1]:
                start_date_str = str(end_date.year) + "-" + str(end_date.month) + "-01"
                array.append(
                    str((datetime.datetime.strptime(start_date_str, '%Y-%m-%d') + datetime.timedelta(days=-1)).date()))
                array.append(start_date_str)
                array.append(str(end_date))
            else:
                array.append(str(end_date))

        return array

    def timestamp_to_datetime(self, time_stamp):
        time_stamp = time_stamp/1000
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))

