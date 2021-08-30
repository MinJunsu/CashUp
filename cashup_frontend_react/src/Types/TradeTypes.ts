export interface ITradeResult {
    position: boolean,
    buy_order_time: string,
    buy_time: string,
    amount: number,
    buy_price: number,
    version: number,
    sell_order_time: string,
    sell_time: string,
    sell_price: number,
    max_rate: number,
    min_rate: number,
    earning_rate: number
}

export interface IStateTrade {
    loading: boolean,
    long: ITradeResult[],
    long_finished: ITradeResult[],
    short: ITradeResult[],
    short_finished: ITradeResult[],
}