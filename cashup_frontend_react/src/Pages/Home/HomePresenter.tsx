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
    flex: 3;
    background-color: red;
`;

const DBData = styled.div`
    flex: 7;
    display: flex;
    min-height: 450px;
`;

interface IProps {
    loading: boolean,
    isMinute: boolean,
    setIsMinute: Function,
    upFlow: IFlow[] | null,
    downFlow: IFlow[] | null,
    elementData: ICandleData[] | null,
}

function HomePresenter({ loading, isMinute, setIsMinute, upFlow, downFlow, elementData }: IProps) {
    return(
        <Container>
            <SummaryData>
                sadfasdfaåß
            </SummaryData>
            <DBData>
                <Flow loading={loading} title="상승" flow={upFlow}/>
                <Flow loading={loading} title="하락" flow={downFlow}/>
                <CandleData loading={loading} isMinute={isMinute} setIsMinute={setIsMinute} elementData={elementData}/>
            </DBData>
        </Container>
    );
}

export default HomePresenter;