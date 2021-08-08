import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';

const Container = styled.div`
    width: 100%;
    height: 80px;
`;

const Logo = styled.span`
    padding: 15px;
`;

const List = styled.ul`
  display: flex;
`;

const Element = styled(Link)`
    padding: 10px 10px;
    margin-left: 5px;
    margin-right: 5px;
    font-size: 20px;
    text-align: center;
    text-decoration: none;
    color: black;
    :hover {
        border-bottom: 2px solid;
        color: #c79110;
        transition: border-bottom 0.5s ease-in-out;    
    }
`;

function Headers() {
    return (
        <Container>
            <List>
                <Logo>CashUp</Logo>
                <Element>내 정보</Element>
                <Element>가상 거래 확인</Element>
                <Element>실전 거래 확인</Element>
            </List>
        </Container>
    );
};

export default Headers;