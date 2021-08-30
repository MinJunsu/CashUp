import axios, { AxiosPromise } from "axios";

import { ITradeResult } from "Types/DBTypes";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000"
})

export const TradeRequest = {
    testResult: (version: number): AxiosPromise<{ long: ITradeResult, long_finished: ITradeResult, short: ITradeResult, short_finished: ITradeResult }> => api.get('/trade/test', {
        params: {
            verision: version
        }
    })
}