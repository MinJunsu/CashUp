import React, { useState, useEffect } from "react";
import styled from "styled-components";

import { IStateTrade } from "Types/TradeTypes";
import { RequestGetter } from "API/TradeGetter"
import RealTimeResult from "Components/Trade/RealTimeResult";

interface IProps {
    version: number,
}

function TradeResult({ version }: IProps) {
    const [ tradeResult, setTradeResult ] = useState<IStateTrade>({ loading: true, long: [], long_finished: [], short: [], short_finished: [] });
    useEffect(() => {
        const interval = setInterval( async () => RequestGetter.getTestTrade(version, setTradeResult), 10000);
        // return clearInterval(interval);
    }, [])
    return (
        <Container>
            <MainContainer>
                <LeftContainer>
                    <RealTimeResult loading={tradeResult.loading} version={version} long={tradeResult.long} short={tradeResult.short}/>
                </LeftContainer>
                <RightContainer>
                </RightContainer>
            </MainContainer>
        </Container>
    );
}

export default TradeResult;

const Container = styled.div`
    flex: 1;
`;

const MainContainer = styled.div`
    display: flex;
`;

const LeftContainer = styled.div`
    flex: 6;
`;

const RightContainer = styled.div`
    flex: 4;
`;

const Header = styled.h1`
    margin-top: 5px;
    margin-bottom: 5px;
    display: block;
`

