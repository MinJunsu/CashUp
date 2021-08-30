import { DataRequest } from "API/DBAPI";

export const RequestGetter = {
    getHourData: async (setHourData: any) => {
        setHourData({
            loading: true,
            data: []
        })
        const { data: { candle } } = await DataRequest.hourData(14);
        setHourData({
            loading: false,
            data: candle
        })
    },
    getMinuteData: async (setMinuteDate: any) => {
        setMinuteDate({
            loading: true,
            data: []
        });
        const { data: { candle } } = await DataRequest.minuteData(14);
        setMinuteDate({
            loading: false,
            data: candle
        });
    },
    getUpFlowData: async (setUpFlow: any) => {
        setUpFlow({
            loading: true,
            data: []
        })
        const { data: { flow } } = await DataRequest.upFlowData(14);
        setUpFlow({
            loading: false,
            data: flow
        })
    },
    getDownFlowData: async (setDownFlow: any) => {
        setDownFlow({
            loading: true,
            data: []
        });
        const { data: { flow } } = await DataRequest.downFlowData(14);
        setDownFlow({
            loading: false,
            data: flow
        })
    }
}