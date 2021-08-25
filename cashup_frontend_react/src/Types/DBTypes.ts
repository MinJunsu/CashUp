export interface IFlow {
    datetime: string,
    base_price: number,
    flow: string,
    flow_confirm: string,
    flow_trade: string
};

export interface ICandleData {
    datetime: string,
    open_price: number,
    min_price: number,
    max_price: number,
    close_price: number,
    avg_price: number,
    volume: number,
    volume_rate: number,
    volume_up_dn: string,
    up_down: string,
    continue_up_down: string
    hour_up_down: string,
    signal: string, 
    work_two_1_0: string,
    work_two_1_5: string,
    work_one_1_0: string,
    work_one_1_5: string
};