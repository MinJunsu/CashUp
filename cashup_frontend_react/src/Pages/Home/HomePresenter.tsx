import React from "react";
import styled from "styled-components";

import Flow from "Components/Flow";
import { ISateFlow, ISateCandle } from "Types/DBTypes";
import CandleData from "Components/CandleData";

const Container = styled.div`
    display: flex;
    flex-direction: column;
`;

const SummaryData = styled.div`
    flex: 3;
    background-color: red;
`;

const DBData = styled.div`
    flex: 7;
    display: flex;
    min-height: 450px;
`;

interface IProps {
    isMinute: boolean,
    setIsMinute: Function,
    upFlow: ISateFlow,
    downFlow: ISateFlow,
    elementData: ISateCandle,
}

function HomePresenter({ isMinute, setIsMinute, upFlow, downFlow, elementData }: IProps) {
    return(
        <Container>
            <SummaryData>
                sadfasdfaåß
            </SummaryData>
            <DBData>
                <Flow title="상승" flow={upFlow}/>
                <Flow title="하락" flow={downFlow}/>
                <CandleData isMinute={isMinute} setIsMinute={setIsMinute} elementData={elementData}/>
            </DBData>
        </Container>
    );
}

export default HomePresenter;