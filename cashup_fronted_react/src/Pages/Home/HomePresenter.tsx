import React from "react";
import styled from "styled-components";

import Flow from "Components/Flow";
import { IFlow, ICandleData } from "Types/DBTypes";
import CandleData from "Components/CandleData";

const Container = styled.div`
    display: flex;
    flex-direction: column;
`;

const SummaryData = styled.div`
    flex-basis: 30%;
`;

const DBData = styled.div`
    flex-basis: 70%;
    display: flex;
    height: 450px;
`;

interface IProps {
    loading: boolean,
    upFlow: IFlow[] | null,
    downFlow: IFlow[] | null,
    hourData: ICandleData[] | null,
    minuteData: ICandleData[] | null,
}



function HomePresenter({ loading, upFlow, downFlow, hourData, minuteData }: IProps) {
    return(
        <Container>
            <SummaryData>
                
            </SummaryData>
            <DBData>
                <Flow loading={loading} title="상승" flow={upFlow}/>
                <Flow loading={loading} title="하락" flow={downFlow}/>
                <CandleData loading={loading} hour={hourData} minute={minuteData} />
            </DBData>
        </Container>
    );
}

export default HomePresenter;