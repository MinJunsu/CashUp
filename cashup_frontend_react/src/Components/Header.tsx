import React from 'react';
import styled from 'styled-components';
import { Link, withRouter } from 'react-router-dom';

interface IProps {
    location: {
        pathname: string
    }
}

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

const Element = styled(Link)<{ current: boolean }>`
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
    border-bottom: 2px solid ${props => props.current ? '#c79110' : 'transparent'};
`;



function Headers({ location: { pathname } }: IProps) {
    return (
        <Container>
            <List>
                <Logo to='/'>CashUp</Logo>
                <Element to='/status' current={pathname === "/status"}>내 정보</Element>
                <Element to='/simulate' current={pathname === "/simulate"}>가상 거래 확인</Element>
                <Element to='/trade' current={pathname === "/trade"}>실전 거래 확인</Element>
            </List>
        </Container>
    );
};

export default withRouter(Headers);