import axios, { AxiosPromise } from "axios";

import { IFlow, ICandle, IModifyFlag } from "Types/DBTypes";

const api = axios.create({
    baseURL: "http://121.147.38.28:8000"
})

export const DataRequest = {
    hourData: (term: number): AxiosPromise<{ candle: ICandle[] }> => api.get('/data/hour'),
    minuteData: (term: number): AxiosPromise<{ candle: ICandle[] }> => api.get('/data/minute'),
    upFlowData: (term: number): AxiosPromise<{ flow: IFlow[] }> => api.get('/data/upflow'),
    downFlowData: (term: number): AxiosPromise<{ flow: IFlow[] }> => api.get('/data/downflow'),
    flagData: (): AxiosPromise<IModifyFlag> => api.get('/data/flag'),
}