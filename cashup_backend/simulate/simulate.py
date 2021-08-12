from data import models
from datetime import timedelta


class Simulate:
    def __init__(self):
        self.count = 0
        self.re_buy_amount_rate = 1
        self.work = 'work_one_1_0'
        self.buy_option = 0
        self.sell_option = 0
        self.re_buy_time = 4
        self.loss_cut_time = 999
        self.trade_option = 'close'
        self.buy_rate = 0
        self.sell_rate = 0
        self.search_amount = 100
        self.max_price_list = []
        self.min_price_list = []
        self.long_result_list = []
        self.short_result_list = []
        self.trade_limit = 0
        self.small_long_result_dict = {
            'trade_count': 0,
            'single_trade_count': 0,
            'big_amount_count': 0,
            'single_big_amount_count': 0,
            'max_amount': 0,
            'max_earning_rate': 0,
            'min_earning_rate': 0,
            'max': 0,
            'min': 0,
            'sum_earning_rate': 0,
            'small_max_earning_rate': 0,
            'small_min_earning_rate': 0,
            'small_max': 0,
            'small_min': 0,
            'small_sum_earning_rate': 0
        }

        self.long_result_dict = {
            'trade_count': 0,
            'single_trade_count': 0,
            'big_amount_count': 0,
            'single_big_amount_count': 0,
            'max_amount': 0,
            'max_earning_rate': 0,
            'min_earning_rate': 0,
            'max': 0,
            'min': 0,
            'sum_earning_rate': 0,
            'small_max_earning_rate': 0,
            'small_min_earning_rate': 0,
            'small_max': 0,
            'small_min': 0,
            'small_sum_earning_rate': 0,
            'max_trade_count': 0
        }

    def order_price(self, flag, element):
        if flag:
            if len(self.min_price_list) == 0:
                return element.min_price
            return min(self.min_price_list) if min(self.min_price_list) < element.min_price else element.min_price

        else:
            if len(self.max_price_list) == 0:
                return element.max_price
            return max(self.max_price_list) if max(self.max_price_list) > element.max_price else element.max_price

    def can_buy(self, trade_list, price, flag):
        if len(trade_list) > 0:
            if flag:
                tmp = []
                for i in trade_list:
                    tmp.append(i['buy_price'])
                # print(str(tmp) + ", " + str(price))
                if min(tmp) > price:
                    return True
                else:
                    return False
            else:
                tmp = []
                for i in trade_list:
                    tmp.append(i['buy_price'])
                # print(str(tmp) + ", " + str(price))
                if max(tmp) < price:
                    return True
                else:
                    return False
        else:
            return True

    def balance_trade(self, flag, result_dict, trade_dict):
        if flag:
            earning_rate = trade_dict['earning_rate'] * (trade_dict['amount'] / 1000) * 100
            max_rate = trade_dict['max'] * (trade_dict['amount'] / 1000) * 100
            min_rate = trade_dict['min'] * (trade_dict['amount'] / 1000) * 100
        else:
            earning_rate = trade_dict['earning_rate']
            max_rate = trade_dict['max']
            min_rate = trade_dict['min']

        result_dict['trade_count'] += 1
        if trade_dict['amount'] > result_dict['max_amount']:
            result_dict['max_amount'] = trade_dict['amount']
        if earning_rate > result_dict['max_earning_rate']:
            result_dict['max_earning_rate'] = earning_rate
        if earning_rate < result_dict['min_earning_rate']:
            result_dict['min_earning_rate'] = earning_rate
        if max_rate > result_dict['max']:
            result_dict['max'] = max_rate
        if min_rate < result_dict['min']:
            result_dict['min'] = min_rate
        result_dict['sum_earning_rate'] += earning_rate
        trade_dict['earning_rate'] = round(earning_rate, 3)
        trade_dict['max'] = round(max_rate, 3)
        trade_dict['min'] = round(min_rate, 3)

    def calculate_earning_rate(self, position, buy_price, now_price):
        if position:
            if buy_price > now_price:
                return -((round((buy_price - now_price) / buy_price, 4)) * 100)
            else:
                return (round(now_price / buy_price, 4) - 1) * 100
        else:
            if buy_price > now_price:
                return (round((buy_price - now_price) / buy_price, 4)) * 100
            else:
                return -(round(now_price / buy_price, 4) - 1) * 100

    def set_default(self,  buy_rate, sell_rate, search_amount, trade_limit):
        self.buy_rate = buy_rate
        self.sell_rate = sell_rate
        self.search_amount = search_amount
        self.trade_limit = trade_limit
        

    def reset_trade_dict(self):
        return {
            'type': "",
            'buy_order_time': "",
            'buy_order_price': 0,
            'amount': "",
            'buy_signal': "",
            'buy_time': "",
            'buy_price': 0,
            'sell_order_time': "",
            'sell_order_price': 0,
            'sell_signal': "",
            'sell_time': "",
            'sell_price': 0,
            'max': 0,
            'min': 0,
            'earning_rate': 0,
        }

    def calculate_earning_rate_list(self, position, trade_list, now_price):
        earning_rate_sum = 0
        for element in trade_list:
            element['earning_rate'] = self.calculate_earning_rate(position, element['buy_price'], now_price)
            if element['earning_rate'] > element['max']:
                element['max'] = element['earning_rate']
            if element['earning_rate'] < element['min']:
                element['min'] = element['earning_rate']
            earning_rate_sum += element['earning_rate'] * (element['amount'] / 100)
        return earning_rate_sum

    def sum_amount(self, trade_list):
        result = 0
        for trade in trade_list:
            result += trade['amount']
        return result

    def set_work(self, element):
        if self.work == "work_one_1_0":
            return element.work_one_1_0
        elif self.work == "work_one_1_5":
            return element.work_one_1_5
        elif self.work == "work_two_1_0":
            return element.work_two_1_0
        elif self.work == "work_two_1_5":
            return element.work_two_1_5

    def simulate(self, position, start_date, end_date):
        long_trade_list = []
        short_trade_list = []
        trade_list = []
        self.long_result_list = []

        trade_dict = self.reset_trade_dict()

        work = "wS1"

        if position == "long":
            flag = True
        else:
            flag = False

        prev_up_down = "UP(U)"

        up_signal_flag = False
        dn_signal_flag = False
        data_set = models.HourData.objects.filter(datetime__range=[start_date, end_date])
        prev_up_time = data_set[0].datetime
        prev_dn_time = data_set[0].datetime
        up_signal_time = data_set[0].datetime
        dn_signal_time = data_set[0].datetime
        prev_up_signal = "fU(U)"
        prev_dn_signal = "fD(D)"
        prev_volume_rate = 0
        prev_continue_up_down = "D1"

        for element in data_set:
            now_work = ""

            volume_flag = False
            if (element.volume_rate > 1) or (prev_volume_rate > 1):
                volume_flag = True

            if self.set_work(element) != "":
                now_work, work = self.set_work(element), self.set_work(element)

            if element.hour_up_down != "":
                prev_up_down = element.hour_up_down

            if element.volume_up_dn == "UP":
                if len(self.max_price_list) > 3:
                    self.min_price_list.pop(0)
                    self.max_price_list.pop(0)
                self.max_price_list.append(element.max_price)
                self.min_price_list.append(element.min_price)

            if not up_signal_flag:
                if element.signal == "fU(U)" and prev_up_time < element.datetime - timedelta(hours=12):
                    up_signal_flag = True
                    up_signal_time = element.datetime

            if not dn_signal_flag:
                if element.signal == "fD(D)" and prev_dn_time < element.datetime - timedelta(hours=12):
                    dn_signal_flag = True
                    dn_signal_time = element.datetime

            if trade_dict['buy_order_time'] == "":
                # work 발생
                if self.trade_option == "close":
                    if flag:
                        if (element.signal == "fU(U)" and prev_dn_time < element.datetime - timedelta(hours=12)) or (len(long_trade_list) == 0 and up_signal_flag and int(prev_continue_up_down[1:]) > 1 and element.continue_up_down == "U1"):
                            if self.can_buy(long_trade_list, int(element.close_price * (1 - (self.buy_rate / 10000))), flag):
                                if up_signal_flag:
                                    up_signal_flag = False
                                buy_flag = False
                                if len(long_trade_list) > self.trade_limit:
                                    if prev_dn_time < element.datetime - timedelta(hours=24):
                                        buy_flag = True
                                else:
                                    buy_flag = True
                                if buy_flag:
                                    trade_dict['type'] = "long"
                                    if len(long_trade_list) > self.trade_limit:
                                        trade_dict['amount'] = 100 if len(long_trade_list) == 0 else self.sum_amount(long_trade_list) * self.re_buy_amount_rate
                                    else:
                                        trade_dict['amount'] = 100 if len(long_trade_list) == 0 else self.sum_amount(long_trade_list) * (self.re_buy_amount_rate * 2)
                                    trade_dict['buy_signal'] = element.signal
                                    trade_dict['buy_order_time'] = element.datetime
                                    trade_dict['buy_order_price'] = int(element.close_price * (1 - (self.buy_rate / 10000)))

                    else:
                        if (element.signal == "fD(D)" and prev_up_time < element.datetime - timedelta(hours=12)) or (len(short_trade_list) == 0 and dn_signal_flag and int(prev_continue_up_down[1:]) > 1 and element.continue_up_down == "D1"):
                            if self.can_buy(short_trade_list, int(element.close_price * (1 + (self.buy_rate / 10000))), flag):
                                if dn_signal_flag:
                                    dn_signal_flag = False
                                buy_flag = False
                                if len(short_trade_list) > self.trade_limit:
                                    if prev_up_time < element.datetime - timedelta(hours=24):
                                        buy_flag = True
                                else:
                                    buy_flag = True
                                if buy_flag:
                                    trade_dict['type'] = "short"
                                    if len(short_trade_list) > self.trade_limit:
                                        trade_dict['amount'] = 100 if len(short_trade_list) == 0 else self.sum_amount(short_trade_list) * self.re_buy_amount_rate
                                    else:
                                        trade_dict['amount'] = 100 if len(short_trade_list) == 0 else self.sum_amount(short_trade_list) * (self.re_buy_amount_rate * 2)
                                    trade_dict['buy_signal'] = element.signal
                                    trade_dict['buy_order_time'] = element.datetime
                                    trade_dict['buy_order_price'] = int(element.close_price * (1 + (self.buy_rate / 10000)))

                elif self.trade_option == "extreme":
                    if now_work != "":
                        if flag:
                            if now_work[1] == "D" and int(now_work[2:]) > self.buy_option and self.can_buy(long_trade_list, int(self.order_price(flag, element) * (1 - (self.buy_rate / 10000))), flag):
                                trade_dict['type'] = "long"
                                trade_dict['buy_signal'] = now_work
                                trade_dict['amount'] = 100 if len(long_trade_list) == 0 else self.sum_amount(long_trade_list) * self.re_buy_amount_rate
                                trade_dict['buy_order_time'] = element.datetime
                                trade_dict['buy_order_price'] = int(self.order_price(flag, element) * (1 - (self.buy_rate / 10000)))
                        else:
                            if now_work[1] == "U" and int(now_work[2:]) > self.buy_option and self.can_buy(short_trade_list, int(self.order_price(flag, element) * (1 + (self.buy_rate / 10000))), flag):
                                trade_dict['type'] = "short"
                                trade_dict['buy_signal'] = now_work
                                trade_dict['amount'] = 100 if len(short_trade_list) == 0 else self.sum_amount(short_trade_list) * self.re_buy_amount_rate
                                trade_dict['buy_order_time'] = element.datetime
                                trade_dict['buy_order_price'] = int(self.order_price(flag, element) * (1 + (self.buy_rate / 10000)))

            if trade_dict['buy_order_time'] != "" and trade_dict['buy_order_time'] != element.datetime and trade_dict['buy_time'] == "":
                if flag:
                    if element.min_price < trade_dict['buy_order_price']:
                        trade_dict['buy_time'] = element.datetime
                        trade_dict['buy_price'] = trade_dict['buy_order_price']
                        long_trade_list.append(trade_dict)

                    elif trade_dict['buy_order_time'] < element.datetime - timedelta(hours=4):
                        trade_dict = self.reset_trade_dict()

                else:
                    if trade_dict['buy_order_price'] < element.max_price:
                        trade_dict['buy_time'] = element.datetime
                        trade_dict['buy_price'] = trade_dict['buy_order_price']
                        short_trade_list.append(trade_dict)

                    elif trade_dict['buy_order_time'] < element.datetime - timedelta(hours=4):
                        trade_dict = self.reset_trade_dict()
            # 판매
            if len(long_trade_list) > 0 or len(short_trade_list) > 0:
                if len(long_trade_list) > 0:
                    trade_list = long_trade_list
                else:
                    trade_list = short_trade_list

                if len(trade_list) > 0 and trade_list[0]['sell_order_time'] == "":
                    trade_sum = self.calculate_earning_rate_list(flag, trade_list, element.close_price)
                    if self.trade_option == "close":
                        if flag:
                            if element.hour_up_down == "DN(U)":
                                if trade_sum > 0:
                                    for dic in trade_list:
                                        dic['sell_signal'] = element.signal
                                        dic['sell_order_time'] = element.datetime
                                        dic['sell_order_price'] = int(element.close_price * (1 + (self.sell_rate / 10000)))

                        else:
                            if element.hour_up_down == "UP(D)":
                                if trade_sum > 0:
                                    for dic in trade_list:
                                        dic['sell_signal'] = element.signal
                                        dic['sell_order_time'] = element.datetime
                                        dic['sell_order_price'] = int(element.close_price * (1 - (self.sell_rate / 10000)))

                    elif self.trade_option == "extreme":
                        if flag:
                            if now_work != "" and now_work[1] == "U" and int(now_work[2:]) > self.sell_option:
                                if trade_sum > 0:
                                    for dic in trade_list:
                                        dic['sell_signal'] = now_work
                                        dic['sell_order_time'] = element.datetime
                                        dic['sell_order_price'] = int(self.order_price(not flag, element) * (1 + (self.sell_rate / 10000)))

                        else:
                            if now_work != "" and now_work[1] == "D" and int(now_work[2:]) > self.sell_option:
                                if trade_sum > 0:
                                    for dic in trade_list:
                                        dic['sell_signal'] = now_work
                                        dic['sell_order_time'] = element.datetime
                                        dic['sell_order_price'] = int(self.order_price(not flag, element) * (1 - (self.sell_rate / 10000)))

                # 판매 호가 완료 및 판매 준비
                if len(trade_list) > 0 and trade_list[0]['sell_order_time'] != "" and trade_list[0]['sell_order_time'] != element.datetime:
                    if flag:
                        if trade_list[0]['sell_order_price'] < element.max_price:
                            self.calculate_earning_rate_list(flag, trade_list, trade_list[0]['sell_order_price'])
                            for dic in trade_list:
                                dic['num'] = trade_list.index(dic)
                                dic['sell_time'] = element.datetime
                                dic['sell_price'] = dic['sell_order_price']
                                self.balance_trade(True, self.long_result_dict, dic)
                                if dic['amount'] >= self.search_amount:
                                    self.long_result_dict['big_amount_count'] += 1
                                del dic['sell_order_price'], dic['buy_order_price'], dic['buy_signal'], dic['sell_signal']
                                self.long_result_list.append(dic)

                            if trade_list[-1]['amount'] >= self.search_amount:
                                self.long_result_dict['single_big_amount_count'] += 1

                            if trade_list[-1]['amount'] <= self.search_amount:
                                for dic in trade_list:
                                    self.balance_trade(False, self.small_long_result_dict, dic)

                            if self.long_result_dict['max_trade_count'] < len(trade_list):
                                self.long_result_dict['max_trade_count'] = len(trade_list)

                            self.long_result_dict['single_trade_count'] += 1
                            trade_dict = self.reset_trade_dict()
                            self.long_result_list.append(self.reset_trade_dict())
                            trade_list.clear()

                        else:
                            if trade_list[0]['sell_order_time'] < element.datetime - timedelta(hours=4):
                                for dic in trade_list:
                                    dic['sell_order_time'] = ""
                                    dic['sell_order_price'] = 0

                    else:
                        if trade_list[0]['sell_order_price'] > element.min_price:
                            self.calculate_earning_rate_list(flag, trade_list, trade_list[0]['sell_order_price'])
                            for dic in trade_list:
                                dic['num'] = trade_list.index(dic)
                                dic['sell_time'] = element.datetime
                                dic['sell_price'] = dic['sell_order_price']
                                self.balance_trade(True, self.long_result_dict, dic)
                                if dic['amount'] >= self.search_amount:
                                    self.long_result_dict['big_amount_count'] += 1
                                del dic['sell_order_price'], dic['buy_order_price'], dic['buy_signal'], dic['sell_signal']
                                self.long_result_list.append(dic)

                            if trade_list[-1]['amount'] >= self.search_amount:
                                self.long_result_dict['single_big_amount_count'] += 1

                            if trade_list[-1]['amount'] <= self.search_amount:
                                for dic in trade_list:
                                    self.balance_trade(False, self.small_long_result_dict, dic)

                            if self.long_result_dict['max_trade_count'] < len(trade_list):
                                self.long_result_dict['max_trade_count'] = len(trade_list)

                            self.long_result_dict['single_trade_count'] += 1
                            trade_dict = self.reset_trade_dict()
                            self.long_result_list.append(self.reset_trade_dict())
                            trade_list.clear()

                        else:
                            if trade_list[0]['sell_order_time'] < element.datetime - timedelta(hours=4):
                                for dic in trade_list:
                                    dic['sell_order_time'] = ""
                                    dic['sell_order_price'] = 0

                if len(trade_list) > 0:
                    if trade_list[-1]['buy_time'] < element.datetime - timedelta(days=self.loss_cut_time):
                        if flag:
                            for dic in trade_list:
                                dic['sell_order_time'] = element.datetime
                                dic['sell_order_price'] = int(element.avg_price * (1 + (self.sell_rate / 10000)))
                                dic['sell_signal'] = "timeout"

                        else:
                            for dic in trade_list:
                                dic['sell_order_time'] = element.datetime
                                dic['sell_order_price'] = int(element.avg_price * (1 - (self.sell_rate / 10000)))
                                dic['sell_signal'] = "timeout"

            if type(trade_dict['buy_order_time']) != str and trade_dict['buy_order_time'] < element.datetime - timedelta(hours=self.re_buy_time) and trade_dict['sell_order_time'] == "":
                trade_dict = self.reset_trade_dict()

            prev_work = now_work
            prev_volume_rate = element.volume_rate
            prev_continue_up_down = element.continue_up_down

            if element.signal == "fU(U)":
                prev_up_signal = element.signal
                prev_up_time = element.datetime

            if element.signal == "fD(D)":
                prev_dn_signal = element.signal
                prev_dn_time = element.datetime

        for dic in short_trade_list:
            self.long_result_list.append(dic)


    def simulate2(self, position, start_date, end_date):
        long_trade_list = []
        short_trade_list = []
        trade_list = []
        self.long_result_list = []
        fu_flag = False
        fd_flag = False
        trade_dict = self.reset_trade_dict()

        work = "wS1"

        if position == "long":
            flag = True
        else:
            flag = False

        last_signal = "UP(U)"

        up_signal_flag = False
        dn_signal_flag = False
        data_set = models.MinuteData.objects.filter(datetime__range=[start_date, end_date])
        prev_up_time = data_set[0].datetime
        prev_dn_time = data_set[0].datetime
        up_signal_time = data_set[0].datetime
        dn_signal_time = data_set[0].datetime
        prev_up_signal = "fU(U)"
        prev_dn_signal = "fD(D)"
        prev_volume_rate = 0
        prev_continue_up_down = "D1"
        down_count = 0
        up_count = 0

        for element in data_set:
            now_work = ""

            volume_flag = False
            if (element.volume_rate > 1) or (prev_volume_rate > 1):
                volume_flag = True

            if self.set_work(element) != "":
                now_work, work = self.set_work(element), self.set_work(element)

            if element.hour_up_down != "":
                prev_up_down = element.hour_up_down
                    
            now_time = element.datetime

            if element.volume_up_dn == "UP":
                if len(self.max_price_list) > 3:
                    self.min_price_list.pop(0)
                    self.max_price_list.pop(0)
                self.max_price_list.append(element.max_price)
                self.min_price_list.append(element.min_price)

            if not up_signal_flag:
                if element.signal == "fU(U)" and prev_up_time < element.datetime - timedelta(hours=12):
                    up_signal_flag = True
                    up_signal_time = element.datetime

            if not dn_signal_flag:
                if element.signal == "fD(D)" and prev_dn_time < element.datetime - timedelta(hours=12):
                    dn_signal_flag = True
                    dn_signal_time = element.datetime

            if trade_dict['buy_order_time'] == "":
                # work 발생
                if self.trade_option == "close":
                    if flag:
                        if last_signal == 'fD(D)' and element.up_down == "U":
                            if self.can_buy(long_trade_list, int(element.close_price * (1 - (self.buy_rate / 10000))), flag):
                                # if up_signal_flag:
                                #     up_signal_flag = False
                                buy_flag = True
                                # if len(long_trade_list) > self.trade_limit:
                                #     if prev_dn_time < element.datetime - timedelta(hours=24):
                                #         buy_flag = True
                                # else:
                                #     buy_flag = True
                                if buy_flag:
                                    trade_dict['type'] = "long"
                                    if len(long_trade_list) > self.trade_limit:
                                        trade_dict['amount'] = 1000 if len(long_trade_list) == 0 else self.sum_amount(long_trade_list) * self.re_buy_amount_rate
                                    else:
                                        trade_dict['amount'] = 1000 if len(long_trade_list) == 0 else self.sum_amount(long_trade_list) * self.re_buy_amount_rate
                                    trade_dict['buy_signal'] = last_signal
                                    trade_dict['buy_order_time'] = element.datetime
                                    trade_dict['buy_order_price'] = int(element.close_price * (1 - (self.buy_rate / 10000)))

                    else:
                        if last_signal == 'fU(U)' and element.up_down == "D":
                            if self.can_buy(short_trade_list, int(element.close_price * (1 + (self.buy_rate / 10000))), flag):
                                # if dn_signal_flag:
                                #     dn_signal_flag = False
                                buy_flag = True
                                # if len(short_trade_list) > self.trade_limit:
                                #     if prev_up_time < element.datetime - timedelta(hours=24):
                                #         buy_flag = True
                                # else:
                                #     buy_flag = True
                                if buy_flag:
                                    trade_dict['type'] = "short"
                                    if len(short_trade_list) > self.trade_limit:
                                        trade_dict['amount'] = 1000 if len(short_trade_list) == 0 else self.sum_amount(short_trade_list) * self.re_buy_amount_rate
                                    else:
                                        trade_dict['amount'] = 1000 if len(short_trade_list) == 0 else self.sum_amount(short_trade_list) * self.re_buy_amount_rate
                                    trade_dict['buy_signal'] = last_signal
                                    trade_dict['buy_order_time'] = element.datetime
                                    trade_dict['buy_order_price'] = int(element.close_price * (1 + (self.buy_rate / 10000)))

                elif self.trade_option == "extreme":
                    if now_work != "":
                        if flag:
                            if now_work[1] == "D" and int(now_work[2:]) > self.buy_option and self.can_buy(long_trade_list, int(self.order_price(flag, element) * (1 - (self.buy_rate / 10000))), flag):
                                trade_dict['type'] = "long"
                                trade_dict['buy_signal'] = now_work
                                trade_dict['amount'] = 100 if len(long_trade_list) == 0 else self.sum_amount(long_trade_list) * self.re_buy_amount_rate
                                trade_dict['buy_order_time'] = element.datetime
                                trade_dict['buy_order_price'] = int(self.order_price(flag, element) * (1 - (self.buy_rate / 10000)))
                        else:
                            if now_work[1] == "U" and int(now_work[2:]) > self.buy_option and self.can_buy(short_trade_list, int(self.order_price(flag, element) * (1 + (self.buy_rate / 10000))), flag):
                                trade_dict['type'] = "short"
                                trade_dict['buy_signal'] = now_work
                                trade_dict['amount'] = 100 if len(short_trade_list) == 0 else self.sum_amount(short_trade_list) * self.re_buy_amount_rate
                                trade_dict['buy_order_time'] = element.datetime
                                trade_dict['buy_order_price'] = int(self.order_price(flag, element) * (1 + (self.buy_rate / 10000)))

            if trade_dict['buy_order_time'] != "" and trade_dict['buy_order_time'] != element.datetime and trade_dict['buy_time'] == "":
                if flag:
                    if element.min_price < trade_dict['buy_order_price']:
                        trade_dict['buy_time'] = element.datetime
                        trade_dict['buy_price'] = trade_dict['buy_order_price']
                        long_trade_list.append(trade_dict)

                    elif trade_dict['buy_order_time'] < element.datetime - timedelta(hours=1):
                        trade_dict = self.reset_trade_dict()

                else:
                    if trade_dict['buy_order_price'] < element.max_price:
                        trade_dict['buy_time'] = element.datetime
                        trade_dict['buy_price'] = trade_dict['buy_order_price']
                        short_trade_list.append(trade_dict)

                    elif trade_dict['buy_order_time'] < element.datetime - timedelta(hours=1):
                        trade_dict = self.reset_trade_dict()
            # 판매
            if len(long_trade_list) > 0 or len(short_trade_list) > 0:
                if len(long_trade_list) > 0:
                    trade_list = long_trade_list
                else:
                    trade_list = short_trade_list

                if len(trade_list) > 0 and trade_list[0]['sell_order_time'] == "":
                    trade_sum = self.calculate_earning_rate_list(flag, trade_list, element.close_price)
                    if self.trade_option == "close":
                        if flag:
                            if True or last_signal == "fU(U)" and element.up_down == "D":
                                if trade_sum > 0:
                                    for dic in trade_list:
                                        dic['sell_signal'] = element.signal
                                        dic['sell_order_time'] = element.datetime
                                        dic['sell_order_price'] = int(element.close_price * (1 + (self.sell_rate / 10000)))

                        else:
                            if True or last_signal == "fD(D)" and element.up_down == "U":
                                if trade_sum > 0:
                                    for dic in trade_list:
                                        dic['sell_signal'] = element.signal
                                        dic['sell_order_time'] = element.datetime
                                        dic['sell_order_price'] = int(element.close_price * (1 - (self.sell_rate / 10000)))

                    elif self.trade_option == "extreme":
                        if flag:
                            if now_work != "" and now_work[1] == "U" and int(now_work[2:]) > self.sell_option:
                                if trade_sum > 0:
                                    for dic in trade_list:
                                        dic['sell_signal'] = now_work
                                        dic['sell_order_time'] = element.datetime
                                        dic['sell_order_price'] = int(self.order_price(not flag, element) * (1 + (self.sell_rate / 10000)))

                        else:
                            if now_work != "" and now_work[1] == "D" and int(now_work[2:]) > self.sell_option:
                                if trade_sum > 0:
                                    for dic in trade_list:
                                        dic['sell_signal'] = now_work
                                        dic['sell_order_time'] = element.datetime
                                        dic['sell_order_price'] = int(self.order_price(not flag, element) * (1 - (self.sell_rate / 10000)))

                # 판매 호가 완료 및 판매 준비
                if len(trade_list) > 0 and trade_list[0]['sell_order_time'] != "" and trade_list[0]['sell_order_time'] != element.datetime:
                    if flag:
                        if trade_list[0]['sell_order_price'] < element.max_price:
                            self.calculate_earning_rate_list(flag, trade_list, trade_list[0]['sell_order_price'])
                            for dic in trade_list:
                                dic['num'] = trade_list.index(dic)
                                dic['sell_time'] = element.datetime
                                dic['sell_price'] = dic['sell_order_price']
                                self.balance_trade(True, self.long_result_dict, dic)
                                if dic['amount'] >= self.search_amount:
                                    self.long_result_dict['big_amount_count'] += 1
                                del dic['sell_order_price'], dic['buy_order_price'], dic['buy_signal'], dic['sell_signal']
                                self.long_result_list.append(dic)

                            if trade_list[-1]['amount'] >= self.search_amount:
                                self.long_result_dict['single_big_amount_count'] += 1

                            if trade_list[-1]['amount'] <= self.search_amount:
                                for dic in trade_list:
                                    self.balance_trade(False, self.small_long_result_dict, dic)

                            if self.long_result_dict['max_trade_count'] < len(trade_list):
                                self.long_result_dict['max_trade_count'] = len(trade_list)

                            self.long_result_dict['single_trade_count'] += 1
                            trade_dict = self.reset_trade_dict()
                            self.long_result_list.append(self.reset_trade_dict())
                            trade_list.clear()

                        else:
                            if trade_list[0]['sell_order_time'] < element.datetime - timedelta(hours=4):
                                for dic in trade_list:
                                    dic['sell_order_time'] = ""
                                    dic['sell_order_price'] = 0

                    else:
                        if trade_list[0]['sell_order_price'] > element.min_price:
                            self.calculate_earning_rate_list(flag, trade_list, trade_list[0]['sell_order_price'])
                            for dic in trade_list:
                                dic['num'] = trade_list.index(dic)
                                dic['sell_time'] = element.datetime
                                dic['sell_price'] = dic['sell_order_price']
                                self.balance_trade(True, self.long_result_dict, dic)
                                if dic['amount'] >= self.search_amount:
                                    self.long_result_dict['big_amount_count'] += 1
                                del dic['sell_order_price'], dic['buy_order_price'], dic['buy_signal'], dic['sell_signal']
                                self.long_result_list.append(dic)

                            if trade_list[-1]['amount'] >= self.search_amount:
                                self.long_result_dict['single_big_amount_count'] += 1

                            if trade_list[-1]['amount'] <= self.search_amount:
                                for dic in trade_list:
                                    self.balance_trade(False, self.small_long_result_dict, dic)

                            if self.long_result_dict['max_trade_count'] < len(trade_list):
                                self.long_result_dict['max_trade_count'] = len(trade_list)

                            self.long_result_dict['single_trade_count'] += 1
                            trade_dict = self.reset_trade_dict()
                            self.long_result_list.append(self.reset_trade_dict())
                            trade_list.clear()

                        else:
                            if trade_list[0]['sell_order_time'] < element.datetime - timedelta(hours=4):
                                for dic in trade_list:
                                    dic['sell_order_time'] = ""
                                    dic['sell_order_price'] = 0

                if len(trade_list) > 0:
                    if trade_list[-1]['buy_time'] < element.datetime - timedelta(days=self.loss_cut_time):
                        if flag:
                            for dic in trade_list:
                                dic['sell_order_time'] = element.datetime
                                dic['sell_order_price'] = int(element.avg_price * (1 + (self.sell_rate / 10000)))
                                dic['sell_signal'] = "timeout"

                        else:
                            for dic in trade_list:
                                dic['sell_order_time'] = element.datetime
                                dic['sell_order_price'] = int(element.avg_price * (1 - (self.sell_rate / 10000)))
                                dic['sell_signal'] = "timeout"

            if type(trade_dict['buy_order_time']) != str and trade_dict['buy_order_time'] < element.datetime - timedelta(hours=self.re_buy_time) and trade_dict['sell_order_time'] == "":
                trade_dict = self.reset_trade_dict()
                
            last_signal = element.signal

        for dic in short_trade_list:
            self.long_result_list.append(dic)

    def simulate3(self, position, start_date, end_date):
        long_trade_list = []
        short_trade_list = []
        trade_list = []
        self.long_result_list = []
        fu_flag = False
        fd_flag = False
        trade_dict = self.reset_trade_dict()

        work = "wS1"

        if position == "long":
            flag = True
        else:
            flag = False

        last_signal = "UP(U)"

        data_set = models.MinuteData.objects.filter(datetime__range=[start_date, end_date])
        down_count = 0
        up_count = 0
        last_fu_time = ""
        last_fu_flag = False
        last_fd_time = ""
        last_fd_flag = False

        for element in data_set:
            now_work = ""

            if self.set_work(element) != "":
                now_work, work = self.set_work(element), self.set_work(element)

            if element.volume_up_dn == "UP":
                if len(self.max_price_list) > 3:
                    self.min_price_list.pop(0)
                    self.max_price_list.pop(0)
                self.max_price_list.append(element.max_price)
                self.min_price_list.append(element.min_price)
                
            if last_fu_time != "":
                if element.datetime - last_fu_time >= timedelta(minutes=60):
                    last_fu_flag = True
                    if element.up_down == "U":
                        up_count += 1
            
            if last_fd_time != "":
                if element.datetime - last_fd_time >= timedelta(minutes=60):
                    last_fd_flag = True
                    if element.up_down == "D":
                        down_count += 1

            if trade_dict['buy_order_time'] == "":
                # work 발생
                if self.trade_option == "close":
                    if flag:
                        if last_fu_flag and up_count > 2:
                            if self.can_buy(long_trade_list, int(element.close_price * (1 - (self.buy_rate / 10000))), flag):
                                buy_flag = True
                                if buy_flag:
                                    trade_dict['type'] = "long"
                                    if len(long_trade_list) > self.trade_limit:
                                        trade_dict['amount'] = 1000 if len(long_trade_list) == 0 else self.sum_amount(long_trade_list) * self.re_buy_amount_rate
                                    else:
                                        trade_dict['amount'] = 1000 if len(long_trade_list) == 0 else self.sum_amount(long_trade_list) * self.re_buy_amount_rate
                                    trade_dict['buy_signal'] = last_signal
                                    trade_dict['buy_order_time'] = element.datetime
                                    trade_dict['buy_order_price'] = int(element.close_price * (1 - (self.buy_rate / 10000)))

                    else:
                        if last_fd_flag and down_count > 2:
                            if self.can_buy(short_trade_list, int(element.close_price * (1 + (self.buy_rate / 10000))), flag):
                                # if dn_signal_flag:
                                #     dn_signal_flag = False
                                buy_flag = True
                                # if len(short_trade_list) > self.trade_limit:
                                #     if prev_up_time < element.datetime - timedelta(hours=24):
                                #         buy_flag = True
                                # else:
                                #     buy_flag = True
                                if buy_flag:
                                    trade_dict['type'] = "short"
                                    if len(short_trade_list) > self.trade_limit:
                                        trade_dict['amount'] = 1000 if len(short_trade_list) == 0 else self.sum_amount(short_trade_list) * self.re_buy_amount_rate
                                    else:
                                        trade_dict['amount'] = 1000 if len(short_trade_list) == 0 else self.sum_amount(short_trade_list) * self.re_buy_amount_rate
                                    trade_dict['buy_signal'] = last_signal
                                    trade_dict['buy_order_time'] = element.datetime
                                    trade_dict['buy_order_price'] = int(element.close_price * (1 + (self.buy_rate / 10000)))

                elif self.trade_option == "extreme":
                    if now_work != "":
                        if flag:
                            if now_work[1] == "D" and int(now_work[2:]) > self.buy_option and self.can_buy(long_trade_list, int(self.order_price(flag, element) * (1 - (self.buy_rate / 10000))), flag):
                                trade_dict['type'] = "long"
                                trade_dict['buy_signal'] = now_work
                                trade_dict['amount'] = 100 if len(long_trade_list) == 0 else self.sum_amount(long_trade_list) * self.re_buy_amount_rate
                                trade_dict['buy_order_time'] = element.datetime
                                trade_dict['buy_order_price'] = int(self.order_price(flag, element) * (1 - (self.buy_rate / 10000)))
                        else:
                            if now_work[1] == "U" and int(now_work[2:]) > self.buy_option and self.can_buy(short_trade_list, int(self.order_price(flag, element) * (1 + (self.buy_rate / 10000))), flag):
                                trade_dict['type'] = "short"
                                trade_dict['buy_signal'] = now_work
                                trade_dict['amount'] = 100 if len(short_trade_list) == 0 else self.sum_amount(short_trade_list) * self.re_buy_amount_rate
                                trade_dict['buy_order_time'] = element.datetime
                                trade_dict['buy_order_price'] = int(self.order_price(flag, element) * (1 + (self.buy_rate / 10000)))

            if trade_dict['buy_order_time'] != "" and trade_dict['buy_order_time'] != element.datetime and trade_dict['buy_time'] == "":
                if flag:
                    if element.min_price < trade_dict['buy_order_price']:
                        trade_dict['buy_time'] = element.datetime
                        trade_dict['buy_price'] = trade_dict['buy_order_price']
                        last_fu_time = ""
                        long_trade_list.append(trade_dict)

                    elif trade_dict['buy_order_time'] < element.datetime - timedelta(hours=1):
                        trade_dict = self.reset_trade_dict()

                else:
                    if trade_dict['buy_order_price'] < element.max_price:
                        trade_dict['buy_time'] = element.datetime
                        trade_dict['buy_price'] = trade_dict['buy_order_price']
                        last_fd_time = ""
                        short_trade_list.append(trade_dict)

                    elif trade_dict['buy_order_time'] < element.datetime - timedelta(hours=1):
                        trade_dict = self.reset_trade_dict()
            # 판매
            if len(long_trade_list) > 0 or len(short_trade_list) > 0:
                if len(long_trade_list) > 0:
                    trade_list = long_trade_list
                else:
                    trade_list = short_trade_list

                if len(trade_list) > 0 and trade_list[0]['sell_order_time'] == "":
                    trade_sum = self.calculate_earning_rate_list(flag, trade_list, element.close_price)
                    if self.trade_option == "close":
                        if flag:
                            if True or last_signal == "fU(U)" and element.up_down == "D":
                                if trade_sum > 0:
                                    for dic in trade_list:
                                        dic['sell_signal'] = element.signal
                                        dic['sell_order_time'] = element.datetime
                                        dic['sell_order_price'] = int(element.close_price * (1 + (self.sell_rate / 10000)))

                        else:
                            if True or last_signal == "fD(D)" and element.up_down == "U":
                                if trade_sum > 0:
                                    for dic in trade_list:
                                        dic['sell_signal'] = element.signal
                                        dic['sell_order_time'] = element.datetime
                                        dic['sell_order_price'] = int(element.close_price * (1 - (self.sell_rate / 10000)))

                    elif self.trade_option == "extreme":
                        if flag:
                            if now_work != "" and now_work[1] == "U" and int(now_work[2:]) > self.sell_option:
                                if trade_sum > 0:
                                    for dic in trade_list:
                                        dic['sell_signal'] = now_work
                                        dic['sell_order_time'] = element.datetime
                                        dic['sell_order_price'] = int(self.order_price(not flag, element) * (1 + (self.sell_rate / 10000)))

                        else:
                            if now_work != "" and now_work[1] == "D" and int(now_work[2:]) > self.sell_option:
                                if trade_sum > 0:
                                    for dic in trade_list:
                                        dic['sell_signal'] = now_work
                                        dic['sell_order_time'] = element.datetime
                                        dic['sell_order_price'] = int(self.order_price(not flag, element) * (1 - (self.sell_rate / 10000)))

                # 판매 호가 완료 및 판매 준비
                if len(trade_list) > 0 and trade_list[0]['sell_order_time'] != "" and trade_list[0]['sell_order_time'] != element.datetime:
                    if flag:
                        if trade_list[0]['sell_order_price'] < element.max_price:
                            self.calculate_earning_rate_list(flag, trade_list, trade_list[0]['sell_order_price'])
                            for dic in trade_list:
                                dic['num'] = trade_list.index(dic)
                                dic['sell_time'] = element.datetime
                                dic['sell_price'] = dic['sell_order_price']
                                self.balance_trade(True, self.long_result_dict, dic)
                                if dic['amount'] >= self.search_amount:
                                    self.long_result_dict['big_amount_count'] += 1
                                del dic['sell_order_price'], dic['buy_order_price'], dic['buy_signal'], dic['sell_signal']
                                self.long_result_list.append(dic)

                            if trade_list[-1]['amount'] >= self.search_amount:
                                self.long_result_dict['single_big_amount_count'] += 1

                            if trade_list[-1]['amount'] <= self.search_amount:
                                for dic in trade_list:
                                    self.balance_trade(False, self.small_long_result_dict, dic)

                            if self.long_result_dict['max_trade_count'] < len(trade_list):
                                self.long_result_dict['max_trade_count'] = len(trade_list)

                            self.long_result_dict['single_trade_count'] += 1
                            trade_dict = self.reset_trade_dict()
                            self.long_result_list.append(self.reset_trade_dict())
                            trade_list.clear()

                        else:
                            if trade_list[0]['sell_order_time'] < element.datetime - timedelta(hours=4):
                                for dic in trade_list:
                                    dic['sell_order_time'] = ""
                                    dic['sell_order_price'] = 0

                    else:
                        if trade_list[0]['sell_order_price'] > element.min_price:
                            self.calculate_earning_rate_list(flag, trade_list, trade_list[0]['sell_order_price'])
                            for dic in trade_list:
                                dic['num'] = trade_list.index(dic)
                                dic['sell_time'] = element.datetime
                                dic['sell_price'] = dic['sell_order_price']
                                self.balance_trade(True, self.long_result_dict, dic)
                                if dic['amount'] >= self.search_amount:
                                    self.long_result_dict['big_amount_count'] += 1
                                del dic['sell_order_price'], dic['buy_order_price'], dic['buy_signal'], dic['sell_signal']
                                self.long_result_list.append(dic)

                            if trade_list[-1]['amount'] >= self.search_amount:
                                self.long_result_dict['single_big_amount_count'] += 1

                            if trade_list[-1]['amount'] <= self.search_amount:
                                for dic in trade_list:
                                    self.balance_trade(False, self.small_long_result_dict, dic)

                            if self.long_result_dict['max_trade_count'] < len(trade_list):
                                self.long_result_dict['max_trade_count'] = len(trade_list)

                            self.long_result_dict['single_trade_count'] += 1
                            trade_dict = self.reset_trade_dict()
                            self.long_result_list.append(self.reset_trade_dict())
                            trade_list.clear()

                        else:
                            if trade_list[0]['sell_order_time'] < element.datetime - timedelta(hours=4):
                                for dic in trade_list:
                                    dic['sell_order_time'] = ""
                                    dic['sell_order_price'] = 0

                if len(trade_list) > 0:
                    if trade_list[-1]['buy_time'] < element.datetime - timedelta(days=self.loss_cut_time):
                        if flag:
                            for dic in trade_list:
                                dic['sell_order_time'] = element.datetime
                                dic['sell_order_price'] = int(element.avg_price * (1 + (self.sell_rate / 10000)))
                                dic['sell_signal'] = "timeout"

                        else:
                            for dic in trade_list:
                                dic['sell_order_time'] = element.datetime
                                dic['sell_order_price'] = int(element.avg_price * (1 - (self.sell_rate / 10000)))
                                dic['sell_signal'] = "timeout"

            if type(trade_dict['buy_order_time']) != str and trade_dict['buy_order_time'] < element.datetime - timedelta(hours=self.re_buy_time) and trade_dict['sell_order_time'] == "":
                trade_dict = self.reset_trade_dict()
                
            last_signal = element.signal
            
            if element.signal == "fU(U)":
                last_fu_flag = False
                last_fu_time = element.datetime
                up_count = 0
                
            if element.signal == "fD(D)":
                last_fd_flag = False
                last_fd_time = element.datetime
                down_count = 0
            

        for dic in short_trade_list:
            self.long_result_list.append(dic)