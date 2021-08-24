import os
import time

import django
from datetime import timedelta, datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'cashup_backend.settings'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

django.setup()

from data.models import HourData, MinuteData, UpFlow, DownFlow
from trade.models import TradeResult, TradeSetting
from django.db.models import Q


class AutoTrade:
    def __init__(self, flag):
        self.flag = flag
        self.version_1_long_flag = False
        self.version_1_short_flag = False
        self.version_1_long_datetime = None
        self.version_1_short_datetime = None
        self.version_2_long_flag = False
        self.version_2_short_flag = False
        self.version_3_long_flag = False
        self.version_3_short_flag = False
        self.version_4_long_flag = False
        self.version_4_short_flag = False
        self.version_5_long_flag = False
        self.version_5_short_flag = False
        self.version_4_long_datetime = None
        self.version_4_short_datetime = None
        self.now_price = 0
        self.min_price = 0
        self.max_price = 0
        self.test_trade_users = []
        self.real_trade_users = []
        self.set_default()

    def set_default(self):
        minute_data = MinuteData.objects.filter(
            datetime__range=[MinuteData.objects.last().datetime - timedelta(hours=6),
                             MinuteData.objects.last().datetime - timedelta(minutes=5)])
        self.now_price = minute_data.last().close_price
        self.min_price = minute_data.last().min_price
        self.max_price = minute_data.last().max_price
        self.get_accounts()
        self.version_1_is_buy(minute_data)
        self.version_2_is_buy(minute_data)
        self.version_3_is_buy(minute_data)
        self.version_4_is_buy()
        self.version_5_is_buy(minute_data)
        print(f'version1: ({self.version_1_long_flag}, {self.version_1_short_flag}) version2: ({self.version_2_long_flag}, {self.version_2_short_flag}) , version3: ({self.version_3_long_flag}, {self.version_3_short_flag}), version4: ({self.version_4_long_flag}, {self.version_4_short_flag}), version5: ({self.version_5_long_flag}, {self.version_5_short_flag})')

    def get_accounts(self):
        user_query = TradeSetting.objects.all()
        for element in user_query:
            if element.test_trade:
                self.test_trade_users.append({
                    'user': element.user,
                    'version': element.version,
                    'buy_rate_option': element.buy_rate_option,
                    'sell_rate_option': element.sell_rate_option
                })
            if element.real_trade:
                self.real_trade_users.append({
                    'user': element.user,
                    'version': element.version,
                    'buy_rate_option': element.buy_rate_option,
                    'sell_rate_option': element.sell_rate_option
                })

    def version_1_is_buy(self, data):
        last_data = data.last()
        if last_data.signal == "fU(D)":
            last_fud_time = last_data.datetime
            last_fuu_time = MinuteData.objects.filter(signal="fU(U)").last().datetime
            prev_query = MinuteData.objects.filter(datetime__range=[last_fuu_time, last_fud_time])
            min_price = 0
            for element in prev_query:
                if element.signal == "fD(D)":
                    min_list = [element.min_price, MinuteData.objects.filter(
                        datetime=element.datetime - timedelta(minutes=5)).last().min_price]
                    min_price = min(min_list)
            if min_price == 0:
                self.version_1_short_flag = True
                self.version_1_short_datetime = last_data.datetime

            else:
                if min_price >= last_data.min_price:
                    self.version_1_short_flag = True
                    self.version_1_short_datetime = last_data.datetime
        else:
            last_fud_time = MinuteData.objects.filter(signal="fU(D)").last().datetime
            last_fuu_time = MinuteData.objects.filter(signal="fU(U)").last().datetime
            prev_query = MinuteData.objects.filter(datetime__range=[last_fuu_time, last_fud_time])
            min_price = 0
            for element in prev_query:
                if element.signal == "fD(D)":
                    min_list = [element.min_price, MinuteData.objects.filter(
                        datetime=element.datetime - timedelta(minutes=5)).last().min_price]
                    min_price = min(min_list)
            prev_query = MinuteData.objects.filter(datetime__gt=last_fud_time)
            if min_price != 0:
                for element in prev_query:
                    if min_price >= element.min_price:
                        self.version_1_short_flag = True
                        self.version_1_short_datetime = element.datetime

        if last_data.signal == "fD(U)":
            last_fdu_time = last_data.datetime
            last_fdd_time = MinuteData.objects.filter(signal="fD(D)").last().datetime
            prev_query = MinuteData.objects.filter(datetime__gt=[last_fdd_time, last_fdu_time])
            max_price = 0
            for element in prev_query:
                if element.signal == "fU(U)":
                    max_list = [element.max_price, MinuteData.objects.filter(
                        datetime=element.datetime - timedelta(minutes=5)).last().max_price]
                    max_price = min(max_list)
            if max_price == 0:
                self.version_1_long_flag = True
                self.version_1_long_datetime = last_data.datetime

            else:
                if max_price <= last_data.max_price:
                    self.version_1_long_flag = True
                    self.version_1_long_datetime = last_data.datetime
        else:
            last_fdu_time = MinuteData.objects.filter(signal="fD(U)").last().datetime
            last_fdd_time = MinuteData.objects.filter(signal="fD(D)").last().datetime
            prev_query = MinuteData.objects.filter(datetime__range=[last_fdd_time, last_fdu_time])
            max_price = 0
            for element in prev_query:
                if element.signal == "fU(U)":
                    max_list = [element.max_price, MinuteData.objects.filter(
                        datetime=element.datetime - timedelta(minutes=5)).last().max_price]
                    max_price = max(max_list)
            prev_query = MinuteData.objects.filter(datetime__gt=last_fdu_time)
            if max_price != 0:
                for element in prev_query:
                    if max_price <= element.max_price:
                        self.version_1_long_flag = True
                        self.version_1_long_datetime = element.datetime

    def version_2_is_buy(self, data):
        last_signal = ""
        last_up_down = ""
        for element in data:
            if element.signal != "":
                last_signal = element.signal
            last_up_down = element.up_down

        if last_signal == 'fD(D)' and last_up_down == "U":
            self.version_2_long_flag = True

        if last_signal == 'fU(U)' and last_up_down == "D":
            self.version_2_short_flag = True

    def version_3_is_buy(self, data):
        up_count = 0
        down_count = 0
        last_fu_time = ""
        last_fu_flag = False
        last_fd_time = ""
        last_fd_flag = False

        for element in data:
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

            if element.signal == "fU(U)":
                last_fu_flag = False
                last_fu_time = element.datetime
                up_count = 0

            if element.signal == "fD(D)":
                last_fd_flag = False
                last_fd_time = element.datetime
                down_count = 0

        if last_fu_flag and up_count > 2:
            self.version_3_long_flag = True

        if last_fd_flag and down_count > 2:
            self.version_3_short_flag = True

    def version_4_is_buy(self):
        last_up_flow = UpFlow.objects.last()
        last_down_flow = DownFlow.objects.last()
        if last_up_flow.up_flow_confirm == "UP":
            prev_up_flow_list = UpFlow.objects.order_by('-id').all()[:4]
            flag = False
            for element in prev_up_flow_list:
                if element.up_flow_confirm != "UP":
                    flag = True
                if element.up_flow_trade == "B#4":
                    flag = True
                    self.version_4_short_flag = True
                    self.version_4_short_datetime = element.datetime
                    break

            if not flag:
                self.version_4_long_flag = True
                self.version_4_long_datetime = last_up_flow.datetime

        elif last_up_flow.up_flow_confirm is None:
            tmp_up_flow = UpFlow.objects.exclude(id=last_up_flow.id).filter(up_flow_confirm=None).last()
            if 1 <= UpFlow.objects.filter(id__range=[tmp_up_flow.id, last_up_flow.id], up_flow_confirm='UP').count() <= 2:
                self.version_4_short_flag = True
                self.version_4_short_datetime = last_up_flow.datetime

        if last_down_flow.down_flow_confirm == "DN":
            prev_down_flow_list = DownFlow.objects.order_by('-id').all()[:4]
            flag = False
            for element in prev_down_flow_list:
                if element.down_flow_confirm != "DN":
                    flag = True
                if element.down_flow_confirm == "S#4":
                    flag = True
                    self.version_4_long_flag = True
                    self.version_4_long_datetime = element.datetime
                    break
            if not flag:
                self.version_4_short_flag = True
                self.version_4_short_datetime = last_down_flow.datetime

        elif last_down_flow.down_flow_confirm is None:
            tmp_down_flow = DownFlow.objects.exclude(id=last_down_flow.id).filter(down_flow_confirm=None).last()
            if 1 <= DownFlow.objects.filter(id__range=[tmp_down_flow.id, last_down_flow.id], down_flow_confirm='DN').count() <= 2:
                self.version_4_long_flag = True
                self.version_4_long_datetime = last_down_flow.datetime

        work_query = HourData.objects.order_by('-id').exclude(work_two_1_0='')[:30]
        for element in work_query:
            if int(element.work_two_1_0[2:]) > 1:
                last_work = element.work_two_1_0
                break
        if self.version_4_long_flag:
            if last_work[1] == "D" and int(last_work[2:]) > 1:
                pass
            else:
                self.version_4_long_flag = False
                self.version_4_long_datetime = None

        elif self.version_4_short_flag:
            if last_work[1] == "U" and int(last_work[2:]) > 1:
                pass
            else:
                self.version_4_short_flag = False
                self.version_4_short_datetime = None

    def version_5_is_buy(self, data):
        last_data = data.last()
        if last_data.signal == "fU(D)":
            last_fu_time = MinuteData.objects.filter(signal="fU(U)").last().datetime
            if last_data.datetime - last_fu_time > timedelta(minutes=45):
                prev_query = MinuteData.objects.filter(datetime__range=[last_fu_time, last_data.datetime])
                flag = True
                for element in prev_query:
                    if element.signal == "fD(D)":
                        flag = False
                if flag:
                    self.version_5_long_flag = True

        if last_data.signal == "fD(U)":
            last_fd_time = MinuteData.objects.filter(signal="fD(D)").last().datetime
            if last_data.datetime - last_fd_time > timedelta(minutes=45):
                prev_query = MinuteData.objects.filter(datetime__range=[last_fd_time, last_data.datetime])
                flag = True
                for element in prev_query:
                    if element.signal == "fU(U)":
                        flag = False
                if flag:
                    self.version_5_short_flag = True

    def get_order_price(self, is_buy, rate_option):
        if is_buy:
            if self.flag:
                price = self.now_price * (1 - (rate_option / 10000))
                return int(price) + 0.5 if price - int(price) > 0.5 else int(price)
            else:
                price = self.now_price * (1 + (rate_option / 10000))
                return int(price) + 0.5 if price - int(price) > 0.5 else int(price)
        else:
            if self.flag:
                price = self.now_price * (1 + (rate_option / 10000))
                return int(price) + 0.5 if price - int(price) > 0.5 else int(price)
            else:
                price = self.now_price * (1 - (rate_option / 10000))
                return int(price) + 0.5 if price - int(price) > 0.5 else int(price)

    def buy_order(self):
        for account in self.test_trade_users:
            if account['version'] != 1:
                if TradeResult.objects.filter(Q(position=self.flag), Q(user=account['user']), Q(buy_time=None), ~Q(buy_order_time=None)):
                    continue
            result_query = TradeResult.objects.filter(Q(position=self.flag), Q(user=account['user']), ~Q(buy_time=None), Q(sell_order_time=None))
            buy_flag = False
            if self.flag:
                if account['version'] == 1:
                    if self.version_1_long_flag:
                        buy_flag = True
                if account['version'] == 2:
                    if self.version_2_long_flag:
                        buy_flag = True
                elif account['version'] == 3:
                    if self.version_3_long_flag:
                        buy_flag = True
                elif account['version'] == 4:
                    if self.version_4_long_flag:
                        buy_flag = True
                elif account['version'] == 5:
                    if self.version_5_long_flag:
                        buy_flag = True
            else:
                if account['version'] == 1:
                    if self.version_1_short_flag:
                        buy_flag = True
                if account['version'] == 2:
                    if self.version_2_short_flag:
                        buy_flag = True
                elif account['version'] == 3:
                    if self.version_3_short_flag:
                        buy_flag = True
                elif account['version'] == 4:
                    if self.version_4_short_flag:
                        buy_flag = True
                elif account['version'] == 5:
                    if self.version_5_short_flag:
                        buy_flag = True

            if buy_flag:
                if account['version'] == 1:
                    if self.flag:
                        if not TradeResult.objects.filter(signal_time=self.version_1_long_datetime):
                            query = TradeResult.objects.filter(Q(position=self.flag), Q(user=account['user']),
                                                               Q(buy_time=None))
                            for element in query:
                                element.delete()
                            order_list = []
                            for rate in [10, 20, 30, 40, 50]:
                                order_list.append(
                                    TradeResult(
                                        position=self.flag,
                                        signal_time=self.version_1_long_datetime,
                                        user=account['user'],
                                        version=account['version'],
                                        buy_order_time=datetime.now(),
                                        amount=100,
                                        buy_price=self.get_order_price(True, rate)
                                    )
                                )
                            TradeResult.objects.bulk_create(order_list)
                    else:
                        if not TradeResult.objects.filter(signal_time=self.version_1_short_datetime):
                            query = TradeResult.objects.filter(Q(position=self.flag), Q(user=account['user']),
                                                               Q(buy_time=None))
                            for element in query:
                                element.delete()
                            order_list = []
                            for rate in [10, 20, 30, 40, 50]:
                                order_list.append(
                                    TradeResult(
                                        position=self.flag,
                                        signal_time=self.version_1_short_datetime,
                                        user=account['user'],
                                        version=account['version'],
                                        buy_order_time=datetime.now(),
                                        amount=100,
                                        buy_price=self.get_order_price(True, rate)
                                    )
                                )
                            TradeResult.objects.bulk_create(order_list)
                else:
                    if len(result_query) == 0:
                        print(f"version: {account['version']}, position: {self.flag} 매수 주문 실행")
                        if self.flag:
                            TradeResult.objects.create(
                                position=self.flag,
                                user=account['user'],
                                version=account['version'],
                                buy_order_time=datetime.now(),
                                amount=100,
                                buy_price=self.get_order_price(True, account['buy_rate_option'])
                            )
                        else:
                            TradeResult.objects.create(
                                position=self.flag,
                                user=account['user'],
                                version=account['version'],
                                buy_order_time=datetime.now(),
                                amount=100,
                                buy_price=self.get_order_price(True, account['buy_rate_option'])
                            )
                    elif len(result_query) > 0:
                        prev_trade = result_query
                        prev_amount_sum = 0
                        for idx, element in enumerate(prev_trade):
                            prev_amount_sum += element.amount
                            if idx == len(prev_trade) - 1:
                                prev_price = element.buy_price
                        print(f"version: {account['version']}, position: {self.flag} 추가 매수 주문 실행")

                        if self.flag:
                            if self.now_price * (1 - (account['buy_rate_option'] / 10000)) < prev_price:
                                TradeResult.objects.create(
                                    position=self.flag,
                                    user=account['user'],
                                    version=account['version'],
                                    buy_order_time=datetime.now(),
                                    amount=prev_amount_sum,
                                    buy_price=self.get_order_price(True, account['buy_rate_option'])
                                )
                        else:
                            if self.now_price * (1 + (account['buy_rate_option'] / 10000)) > prev_price:
                                TradeResult.objects.create(
                                    position=self.flag,
                                    user=account['user'],
                                    version=account['version'],
                                    buy_order_time=datetime.now(),
                                    amount=prev_amount_sum,
                                    buy_price=self.get_order_price(True, account['buy_rate_option'])
                                )

    def check_price(self):
        for account in self.test_trade_users:
            sell_query = TradeResult.objects.filter(Q(position=self.flag), Q(user=account['user']), ~Q(buy_time=None), Q(sell_time=None))
            if sell_query:
                for element in sell_query:
                    element.calculate_earning_rate(now_price=self.now_price)
                    element.save()

            buy_check_query = TradeResult.objects.filter(Q(position=self.flag), Q(user=account['user']), ~Q(buy_order_time=None),
                                                         Q(buy_time=None))
            if buy_check_query.last():
                if self.flag:
                    for element in buy_check_query:
                        if element.buy_price > self.min_price:
                            print(f"version: {account['version']}, position: {self.flag} 매수 실행")
                            element.buy_time = datetime.now()
                            element.save()

                        elif datetime.now() - element.buy_order_time > timedelta(hours=1):
                            if account['version'] != 4:
                                print(f"version: {account['version']}, position: {self.flag} 매수 주문 취소 실행")
                                element.delete()
                else:
                    for element in buy_check_query:
                        if element.buy_price < self.max_price:
                            print(f"version: {account['version']}, position: {self.flag} 매수 실행")
                            element.buy_time = datetime.now()
                            element.save()

                        elif datetime.now() - element.buy_order_time > timedelta(hours=1):
                            if account['version'] != 4:
                                print(f"version: {account['version']}, position: {self.flag} 매수 주문 취소 실행")
                                element.delete()

            sell_check_query = TradeResult.objects.filter(Q(position=self.flag), Q(user=account['user']), ~Q(sell_order_time=None),
                                                          Q(sell_time=None))
            if sell_check_query:
                if self.flag:
                    if sell_check_query.last().sell_price < self.max_price:
                        print(f"version: {account['version']}, position: {self.flag} 매도 실행")
                        for element in sell_check_query:
                            element.sell_time = datetime.now()
                            element.calculate_earning_rate(now_price=element.sell_price)
                            element.save()
                else:
                    if sell_check_query.last().sell_price > self.min_price:
                        print(f"version: {account['version']}, position: {self.flag} 매도 실행")
                        for element in sell_check_query:
                            element.sell_time = datetime.now()
                            element.calculate_earning_rate(now_price=element.sell_price)
                            element.save()

    def sell_order(self):
        for account in self.test_trade_users:
            sell_query = TradeResult.objects.filter(Q(position=self.flag), Q(user=account['user']), ~Q(buy_time=None), Q(sell_order_time=None))
            earning_rate_sum = 0
            if sell_query:
                for element in sell_query:
                    earning_rate_sum += element.earning_rate
                    element.save()

            if earning_rate_sum > 0:
                print(f"version: {account['version']}, position: {self.flag} 매도 주문 실행")
                for element in sell_query:
                    element.sell_order_time = datetime.now()
                    element.sell_price = self.get_order_price(False, account['sell_rate_option'])
                    element.save()


if __name__ == "__main__":
    trade_list = [AutoTrade(True), AutoTrade(False)]
    for trade in trade_list:
        trade.check_price()
        if datetime.now().minute % 5 == 0:
            trade.buy_order()
            trade.sell_order()

