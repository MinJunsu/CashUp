import React from "react";
import styled from "styled-components";

import { ITradeResult } from "Types/TradeTypes";
import RealTimeTable from "Components/Trade/RealTimeTable";

interface IProps {
    loading: boolean,
    version: number,
    long: ITradeResult[],
    short: ITradeResult[]
}

function RealTimeResult({ loading, version, long, short }: IProps) {
    return (
        <Container>
            <TradeSection>
                <Header>V{version} 공매수</Header>
                <RealTimeTable loading={loading} isLong={true} trade={long}/>
            </TradeSection>
            <ResultSection>
                
            </ResultSection>
            <TradeSection>
                <Header>V{version} 공매도</Header>
                <RealTimeTable loading={loading} isLong={false} trade={short}/>
            </TradeSection>
        </Container>
    );
}

export default RealTimeResult;

const Container = styled.div`
    display: flex;
    flex: 5;
    gap: 5;
`;

const Header = styled.h5`
    margin-top: 3px;
    margin-bottom: 3px;
    text-align: center;
`;

const TradeSection = styled.section`
    flex: 3;
`;

const ResultSection = styled.section`
    flex: 1;
`;
