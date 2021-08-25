import React, { useState, useEffect } from "react";
import styled from "styled-components";
import Loader from "react-loader-spinner";

import { ICandleData } from "Types/DBTypes";

const Container = styled.div`
    text-align: center;
    flex-basis: 60%;
    border: 1px solid;
`;

const LoaderCotainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 95%;
`;

const Header = styled.div`
    display: flex;
    width: 100%;
    border-bottom: 1px solid;
`;

const HeaderElement = styled.div<{ flag: boolean }>`
    flex-basis: 50%;
    background-color: ${(props) => props.flag ? "rgba(209, 207, 207, 0.6)" : "transparent"};
    :hover {
        background-color: rgba(209, 207, 207, 0.2);
    }
    h4 {
        margin-top: 2px;
        margin-bottom: 2px;
    }
`;

const Frame = styled.div`
    height: 95%;
`;

const Section = styled.section`
    padding-right: 5px;
    padding-left: 5px;
`;

const SectionHeader = styled.div`
    font-size: 15px;
    display: grid;
    gap: 10px;
    grid-template-columns: 3fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
`;
const SectionHeaderElement = styled.h5`
    margin-top: 2px;
    margin-bottom: 2px;
    padding-left: 5px;
    padding-right: 5px;
`;
const SectionBody = styled.div`
    font-size: 14px;
    overflow-y: scroll;
    max-height: 400px;
`;

const SectionBodyContainer = styled.div`
    display: grid;
    gap: 10px;
    grid-template-columns: 3fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
    border-bottom: 1px solid;
`;

const SectionBodyElement = styled.span`
    display: flex;
    align-items: center;
`;

interface IProps {
    loading: boolean,
    minute: ICandleData[] | null,
    hour: ICandleData[] | null,
}


function CandleData({ loading, minute, hour }: IProps) {
    const [ isMinute, setIsMinute ] = useState<boolean>(true);
    const [ elementData, setElementData ] = useState<ICandleData[] | null>(minute);
    useEffect(() => {
        if(isMinute) {
            setElementData(minute);
        } else {
            setElementData(hour);
        }
    }, [ isMinute ])
    return(
        <Container>
            <Header>
                <HeaderElement id="minute" onClick={(event) => setIsMinute(true)} flag={isMinute}><h4>5분 데이터</h4></HeaderElement>
                <HeaderElement id="hour"   onClick={(event) => setIsMinute(false)} flag={!isMinute}><h4>1시간 데이터</h4></HeaderElement>
            </Header>
            {
                loading ? <LoaderCotainer><Loader type="TailSpin" color="#a9eef5" height={100} width={100}/></LoaderCotainer> :
                <Frame>
                    <Section>
                        <SectionHeader>
                            <SectionHeaderElement>시간</SectionHeaderElement>
                            <SectionHeaderElement>시가</SectionHeaderElement>
                            <SectionHeaderElement>고가</SectionHeaderElement>
                            <SectionHeaderElement>저가</SectionHeaderElement>
                            <SectionHeaderElement>종가</SectionHeaderElement>
                            <SectionHeaderElement>평균</SectionHeaderElement>
                            <SectionHeaderElement>UP/DN</SectionHeaderElement>
                            <SectionHeaderElement>Signal</SectionHeaderElement>
                            <SectionHeaderElement>2개 1.0</SectionHeaderElement>
                            <SectionHeaderElement>2개 1.5</SectionHeaderElement>
                            <SectionHeaderElement>1개 1.0</SectionHeaderElement>
                            <SectionHeaderElement>1개 1.5</SectionHeaderElement>
                        </SectionHeader>
                        <SectionBody>
                        {
                            elementData?.map((element) => {
                                return(
                                    <SectionBodyContainer>
                                        <SectionBodyElement>{element.datetime.replace("T", " ").substring(0, 16)}</SectionBodyElement>
                                        <SectionBodyElement>{element.open_price}</SectionBodyElement>
                                        <SectionBodyElement>{element.max_price}</SectionBodyElement>
                                        <SectionBodyElement>{element.min_price}</SectionBodyElement>
                                        <SectionBodyElement>{element.close_price}</SectionBodyElement>
                                        <SectionBodyElement>{element.avg_price}</SectionBodyElement>
                                        <SectionBodyElement>{element.continue_up_down}</SectionBodyElement>
                                        <SectionBodyElement>{element.signal}</SectionBodyElement>
                                        <SectionBodyElement>{element.work_one_1_0}</SectionBodyElement>
                                        <SectionBodyElement>{element.work_one_1_5}</SectionBodyElement>
                                        <SectionBodyElement>{element.work_two_1_0}</SectionBodyElement>
                                        <SectionBodyElement>{element.work_two_1_5}</SectionBodyElement>
                                    </SectionBodyContainer>
                                );
                            })
                        }
                        </SectionBody>
                    </Section>
                </Frame>
            }
        </Container>
    );
}

export default CandleData;