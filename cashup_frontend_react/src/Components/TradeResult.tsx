import React from "react";
import styled from "styled-components";

const Container = styled.div`
    flex: 1;
`;

const Header = styled.h1`
`

interface IProps {
    version: number
}

function TradeResult({ version }: IProps) {
    return (
        <Container>
            <Header>Version {version} 가상거래</Header>
        </Container>
    );
}

export default TradeResult;