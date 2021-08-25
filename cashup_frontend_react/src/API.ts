import axios, { AxiosPromise } from "axios";

import { IFlow, ICandleData } from "Types/DBTypes";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000"
})

interface IDataResponse {
    hour: ICandleData[],
    minute: ICandleData[],
    up_flow: IFlow[],
    down_flow: IFlow[]
}

export const DataRequest = {
    data: (term: number): AxiosPromise<IDataResponse> => api.get('/data/data'),
}