import axios, { AxiosPromise } from "axios";

import { ITradeResult } from "Types/TradeTypes";

const api = axios.create({
    baseURL: "http://121.147.38.28:8000"
})

export const TradeRequest = {
    testResult: (version: number): AxiosPromise<{ long: ITradeResult, long_finished: ITradeResult, short: ITradeResult, short_finished: ITradeResult }> => api.get('/trade/test', {
        params: {
            version: version
        }
    })
}