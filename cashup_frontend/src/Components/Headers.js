import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';

const Container = styled.div`
    width: 100%;
    min-height: 60px;
`;

const Logo = styled(Link)`
    padding: 15px;
`;

const List = styled.ul`
  display: flex;
`;

const Element = styled(Link)`
    padding-top: 10px;
    margin-left: 5px;
    margin-right: 5px;
    font-size: 20px;
    text-align: center;
    text-decoration: none;
    color: black;
    :hover {
        border-bottom: 2px solid;
        color: #c79110;
        transition: border-bottom 0.3s ease-in-out;    
    }
`;

function Headers() {
    return (
        <Container>
            <List>
                <Logo to='/'>CashUp</Logo>
                <Element to='/status'>내 정보</Element>
                <Element to='/simulate'>가상 거래 확인</Element>
                <Element to='/trade'>실전 거래 확인</Element>
            </List>
        </Container>
    );
};

export default Headers;