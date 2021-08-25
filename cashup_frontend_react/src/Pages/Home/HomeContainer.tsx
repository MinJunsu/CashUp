import React, { useState, useEffect } from "react";
import styled from "styled-components";

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

    const getData = async() => {
        try {
            setLoading(true);
            setTimeout(() => {}, 3000);
            const { data: { hour, minute, up_flow, down_flow } } = await DataRequest.data(range);
            setHourData(hour);
            setMinuteDate(minute);
            setUpFlow(up_flow);
            setDownFlow(down_flow);
        } catch(e) {
            console.log(e);
        } finally {
            setLoading(false);
        }
    }
    useEffect(() => {
        getData();
        setInterval(() => getData(), 60000);
    }, [ range ])

    return(
        <div>
            <HomePresenter loading={loading} upFlow={upFlow} downFlow={downFlow} hourData={hourData} minuteData={minuteData}/>
        </div>
    );
}

export default HomeContainer;