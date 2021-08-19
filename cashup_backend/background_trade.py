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
        self.version_2_long_flag = False
        self.version_2_short_flag = False
        self.version_3_long_flag = False
        self.version_3_short_flag = False
        self.version_4_long_flag = False
        self.version_4_short_flag = False
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
                             MinuteData.objects.last().datetime])
        self.now_price = minute_data.last().close_price
        self.min_price = minute_data.last().min_price
        self.max_price = minute_data.last().max_price
        self.get_accounts()
        self.version_2_is_buy(minute_data)
        self.version_3_is_buy(minute_data)
        self.version_4_is_buy()
        print(f'version2: ({self.version_2_long_flag}, {self.version_2_short_flag}) , version3: ({self.version_3_long_flag}, {self.version_3_short_flag}), version4: ({self.version_4_long_flag}, {self.version_4_short_flag})')

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
        up_flow = UpFlow.objects.filter(up_flow_trade='S#3').last()
        down_flow = DownFlow.objects.filter(down_flow_trade='B#3').last()
        # Sell Order
        if up_flow.datetime > down_flow.datetime:
            self.version_4_short_flag = True
            self.version_4_short_datetime = up_flow.datetime
        # BuyOrder
        else:
            self.version_4_long_flag = True
            self.version_4_long_datetime = down_flow.datetime

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
            if account['version'] != 4:
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

            if buy_flag:
                if account['version'] == 4:
                    if self.flag:
                        if self.version_4_long_flag:
                            if not TradeResult.objects.filter(signal_time=self.version_4_long_datetime):
                                print(f"version: {account['version']}, position: {self.flag} 매수 주문 실행")
                                query = TradeResult.objects.filter(Q(position=self.flag), Q(user=account['user']), Q(buy_time=None))
                                for element in query:
                                    element.delete()
                                order_list = []
                                for rate in [20, 40, 60, 80, 100]:
                                    order_list.append(
                                        TradeResult(
                                            position=self.flag,
                                            signal_time=self.version_4_long_datetime,
                                            user=account['user'],
                                            version=account['version'],
                                            buy_order_time=datetime.now(),
                                            amount=100,
                                            buy_price=self.get_order_price(True, rate)
                                        )
                                    )
                                TradeResult.objects.bulk_create(order_list)
                    else:
                        if self.version_4_short_flag:
                            print(TradeResult.objects.filter(signal_time=self.version_4_short_datetime))
                            if not TradeResult.objects.filter(signal_time=self.version_4_short_datetime):
                                print(f"version: {account['version']}, position: {self.flag} 매수 주문 실행")
                                query = TradeResult.objects.filter(Q(position=self.flag), Q(user=account['user']), Q(buy_time=None))
                                for element in query:
                                    element.delete()
                                order_list = []
                                for rate in [20, 40, 60, 80, 100]:
                                    order_list.append(
                                        TradeResult(
                                            position=self.flag,
                                            signal_time=self.version_4_short_datetime,
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
                        prev_trade = result_query.last()
                        prev_amount, prev_price = prev_trade.amount, prev_trade.buy_price
                        print(f"version: {account['version']}, position: {self.flag} 추가 매수 주문 실행")

                        if self.flag:
                            if self.now_price * (1 - (account['buy_rate_option'] / 10000)) < prev_price:
                                TradeResult.objects.create(
                                    position=self.flag,
                                    user=account['user'],
                                    version=account['version'],
                                    buy_order_time=datetime.now(),
                                    amount=prev_amount,
                                    buy_price=self.get_order_price(True, account['buy_rate_option'])
                                )
                        else:
                            if self.now_price * (1 + (account['buy_rate_option'] / 10000)) < prev_price:
                                TradeResult.objects.create(
                                    position=self.flag,
                                    user=account['user'],
                                    version=account['version'],
                                    buy_order_time=datetime.now(),
                                    amount=prev_amount,
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
                                                         Q(buy_time=None)).last()
            if buy_check_query:
                if self.flag:
                    if buy_check_query.buy_price > self.min_price:
                        print(f"version: {account['version']}, position: {self.flag} 매수 실행")
                        buy_check_query.buy_time = datetime.now()
                        buy_check_query.save()

                    elif datetime.now() - buy_check_query.buy_order_time > timedelta(hours=1):
                        if account['version'] != 4:
                            print(f"version: {account['version']}, position: {self.flag} 매수 주문 취소 실행")
                            buy_check_query.delete()
                else:
                    if buy_check_query.buy_price < self.max_price:
                        print(f"version: {account['version']}, position: {self.flag} 매수 실행")
                        buy_check_query.buy_time = datetime.now()
                        buy_check_query.save()

                    elif datetime.now() - buy_check_query.buy_order_time > timedelta(hours=1):
                        if account['version'] != 4:
                            print(f"version: {account['version']}, position: {self.flag} 매수 주문 취소 실행")
                            buy_check_query.delete()

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
                if account['version'] == 4:
                    if self.flag:
                        if self.version_4_short_flag:
                            print(f"version: {account['version']}, position: {self.flag} 매도 주문 실행")
                            for element in sell_query:
                                element.sell_order_time = datetime.now()
                                element.sell_price = self.get_order_price(False, account['sell_rate_option'])
                                element.save()
                    else:
                        if self.version_4_long_flag:
                            print(f"version: {account['version']}, position: {self.flag} 매도 주문 실행")
                            for element in sell_query:
                                element.sell_order_time = datetime.now()
                                element.sell_price = self.get_order_price(False, account['sell_rate_option'])
                                element.save()
                else:
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
