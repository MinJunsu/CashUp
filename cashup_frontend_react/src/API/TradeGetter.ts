import { TradeRequest } from "API/TradeAPI";

export const RequestGetter = {
    getTestTrade: async(version: number, setter: any) => {
        setter({
            loading: true,
            long: [],
            long_finished: [],
            short: [],
            short_finished: []
        })
        const { data: { long, long_finished, short, short_finished } } = await TradeRequest.testResult(version);
        setter({
            loading: true,
            long: long,
            long_finished: long_finished,
            short: short,
            short_finished: short_finished
        })
    }
}