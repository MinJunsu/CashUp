import React, { useState, useEffect } from "react";

import HomePresenter from "Pages/Home/HomePresenter";
import { DataRequest } from "API/DBAPI";
import { ISateFlow, ISateCandle } from "Types/DBTypes";
import { RequestGetter } from "API/DBGetter";
import { clearInterval } from "timers";

interface IProps {

}

function HomeContainer({}: IProps) {
    const [ range, setRange ] = useState<number>(7);
    const [ hourData, setHourData ] = useState<ISateCandle>({ loading: true, data: [] });
    const [ minuteData, setMinuteDate ] = useState<ISateCandle>({ loading: true, data: [] });
    const [ upFlow, setUpFlow ] = useState<ISateFlow>({ loading: true, data: [] });
    const [ downFlow, setDownFlow ] = useState<ISateFlow>({ loading: true, data: [] });
    const [ isMinute, setIsMinute ] = useState<boolean>(true);
    const [ elementData, setElementData ] = useState<ISateCandle>({ loading: true, data: [] });

    useEffect(() => {
        RequestGetter.getHourData(setHourData);
        RequestGetter.getMinuteData(setMinuteDate); 
        RequestGetter.getUpFlowData(setUpFlow);
        RequestGetter.getDownFlowData(setDownFlow);
        const getFlag = setInterval(async () => { updateData(); }, 1000 * 60);
        return () => clearInterval(getFlag);
    }, [])

    useEffect(() => {
        if(isMinute) {
            setElementData({
                loading: minuteData.loading,
                data: minuteData.data
            })
        } else {
            setElementData({
                loading: hourData.loading,
                data: hourData.data
            })
        }
    }, [ isMinute ])

    const updateData = async () => {
        const { data: { hour_flag, minute_flag, upflow_flag, downflow_flag } } = await DataRequest.flagData();
        console.log(hour_flag, minute_flag, upflow_flag, downflow_flag);
        const minute = new Date().getMinutes();
        if(hour_flag) {
            if(0 <= minute && minute <= 5) {
                RequestGetter.getHourData(setHourData);
            }
        }
        if (minute_flag) {
            if(0 <= (minute % 5) && (minute % 5) <= 1)
            RequestGetter.getMinuteData(setMinuteDate); 
        }
        if (upflow_flag) {
            RequestGetter.getUpFlowData(setUpFlow);
        }
        if (downflow_flag) {
            RequestGetter.getDownFlowData(setDownFlow);
        }
    }

    return(
        <div>
            <HomePresenter upFlow={upFlow} downFlow={downFlow} isMinute={isMinute} setIsMinute={setIsMinute} elementData={elementData}/>
        </div>
    );
}

export default HomeContainer;