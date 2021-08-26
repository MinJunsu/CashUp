import React, { useState, useEffect } from "react";

import HomePresenter from "Pages/Home/HomePresenter";
import { DataRequest } from "API";
import { IFlow, ICandleData } from "Types/DBTypes";

interface IProps {

}

function HomeContainer({}: IProps) {
    const [ loading, setLoading ] = useState<boolean>(true);
    const [ range, setRange ] = useState<number>(7);
    const [ hourData, setHourData ] = useState<ICandleData[] | null>(null);
    const [ minuteData, setMinuteDate ] = useState<ICandleData[] | null>(null);
    const [ upFlow, setUpFlow ] = useState<IFlow[] | null>(null);
    const [ downFlow, setDownFlow ] = useState<IFlow[] | null>(null);
    const [ isMinute, setIsMinute ] = useState<boolean>(true);
    const [ elementData, setElementData ] = useState<ICandleData[] | null>(null);

    useEffect(() => {
        if(isMinute) {
            setElementData(minuteData);
        } else {
            setElementData(hourData);
        }
    }, [ isMinute ]);

    useEffect(() => {
        getData();
        setInterval(() => getData(), 60000);
    }, [])

    const getData = async() => {
        try {
            setLoading(true);
            const { data: { hour, minute, up_flow, down_flow } } = await DataRequest.data(range);
            setHourData(hour);
            setMinuteDate(minute);
            setUpFlow(up_flow);
            setDownFlow(down_flow);
            setElementData(isMinute ? minuteData : hourData);
        } catch(e) {
            console.log(e);
        } finally {
            setLoading(false);
        }
    }
    return(
        <div>
            <HomePresenter loading={loading} upFlow={upFlow} downFlow={downFlow} isMinute={isMinute} setIsMinute={setIsMinute} elementData={elementData}/>
        </div>
    );
}

export default HomeContainer;