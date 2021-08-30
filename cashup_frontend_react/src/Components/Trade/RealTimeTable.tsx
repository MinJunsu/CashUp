import React, { useState } from "react";
import Loader from "react-loader-spinner";
import styled from "styled-components";
import { ITradeResult } from "Types/TradeTypes";

interface IProps {
    loading: boolean,
    isLong: boolean,
    trade: ITradeResult[]
}



function RealTimeTable({ loading, isLong, trade }: IProps) {
    return(
        <Container>
            <Section>
                <SectionHeader>
                    <SectionHeaderElement>호가 시간</SectionHeaderElement>
                    <SectionHeaderElement>구매 시간</SectionHeaderElement>
                    <SectionHeaderElement>구매량</SectionHeaderElement>
                    <SectionHeaderElement>구매 가격</SectionHeaderElement>
                    <SectionHeaderElement>판매 가격</SectionHeaderElement>
                    <SectionHeaderElement>수익률</SectionHeaderElement>
                </SectionHeader>
                <SectionBody>
                {
                    trade.length > 0 && trade.map((element) => {
                        return(
                            <SectionBodyContainer key={element.buy_order_time.replace("T", " ").substring(0, 16)}>
                                <SectionBodyElement>{element.buy_order_time.replace("T", " ").substring(8, 16)}</SectionBodyElement>
                                <SectionBodyElement>{element.buy_time ? element.buy_time.replace("T", " ").substring(8, 16) : ""}</SectionBodyElement>
                                <SectionBodyElement>{element.amount}</SectionBodyElement>
                                <SectionBodyElement>{element.buy_price}</SectionBodyElement>
                                <SectionBodyElement>{element.sell_price}</SectionBodyElement>
                                <SectionBodyElement>{element.earning_rate}</SectionBodyElement>
                            </SectionBodyContainer>
                        )
                    })
                }
                {
                    trade.length === 0 && (
                        <LoaderCotainer>
                            Nothing Here!
                        </LoaderCotainer>
                    )
                }
                </SectionBody>
            </Section>            
        </Container>
    );
}

export default RealTimeTable;

const Container = styled.div``;

const LoaderCotainer = styled.div`
    display: block;
    padding: 60px 0;
    text-align: center;
    align-items: center;
    justify-content: center;
`;

const Section = styled.section`
    text-align: center;
    padding-right: 5px;
    padding-left: 5px;
`;

const SectionHeader = styled.div`
    font-size: 15px;
    display: flex;
`;
const SectionHeaderElement = styled.h5`
    margin-top: 2px;
    margin-bottom: 2px;
    flex: 1;
`;
const SectionBody = styled.div`
    font-size: 14px;
    overflow-y: scroll;
    min-height: 150px;
    max-height: 150px;
`;

const SectionBodyContainer = styled.div`
    display: flex;
    border-bottom: 1px solid;
    cursor: default;
    :hover {
        background-color: skyblue;
    }
`;

const SectionBodyElement = styled.span`
    justify-content: center;
    padding-left: 1px;
    padding-right: 1px;
    flex: 1;
`;