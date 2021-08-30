import React from "react";
import styled from "styled-components";

import TradeResult from "Components/TradeResult";

const Container = styled.div`
    display: flex;
    flex-direction: column;
`;

function TestTradePresenter() {
    
    return(
        <Container>
            <TradeResult version={1}/>
            <TradeResult version={2}/>
            <TradeResult version={3}/>
        </Container>
    );
}

export default TestTradePresenter;