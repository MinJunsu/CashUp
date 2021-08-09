import React, { useEffect } from 'react';
import styled from 'styled-components';

const Container = styled.div`
    width: 20%;
`;

const Text = styled.p`
    text-align: left;
    padding: 5px;
`;

function SimulationResult(props) {
    const result = props.result;
    return (
        <Container>
            <Text>총 거래수: {result.trade_count}</Text>
            <Text>총 거래 수 (단일): {result.single_trade_count}</Text>
            <Text>최대 계약 수: {result.max_amount}({result.max_trade_count})</Text>
            <Text>최대 수익률: { result.max_earning_rate } </Text>
            <Text>최소 수익률: { result.min_earning_rate } </Text>
            <Text>최대: { result.max } </Text>
            <Text>최소: { result.min }</Text>
            <Text>총 거래 수익률: { result.sum_earning_rate }</Text>
        </Container>
    );
}

export default SimulationResult;
