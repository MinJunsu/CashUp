import React from "react";
import styled from "styled-components";
import Loader from "react-loader-spinner";

import { ISateCandle } from "Types/DBTypes";

const Container = styled.div`
    text-align: center;
    flex: 3;
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
    border-bottom: 1px solid;
`;

const HeaderElement = styled.div<{ flag: boolean }>`
    flex: 1;
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
    display: flex;
`;
const SectionHeaderElement = styled.h5<{ basis: number }>`
    flex: ${(props) => props.basis};
    margin-top: 2px;
    margin-bottom: 2px;
`;
const SectionBody = styled.div`
    font-size: 14px;
    overflow-y: scroll;
    max-height: 400px;
`;

const SectionBodyContainer = styled.div`
    display: flex;
    border-bottom: 1px solid;
    cursor: default;
    :hover {
        background-color: skyblue;
    }
`;

const SectionBodyElement = styled.span<{ basis: number }>`
    flex: ${(props) => props.basis};
    align-items: center;
`;

interface IProps {
    isMinute: boolean,
    setIsMinute: Function,
    elementData: ISateCandle
}


function CandleData({ isMinute, setIsMinute, elementData }: IProps) {
    return(
        <Container>
            <Header>
                <HeaderElement id="minute" onClick={(event) => setIsMinute(true)} flag={isMinute}><h4>5분 데이터</h4></HeaderElement>
                <HeaderElement id="hour"   onClick={(event) => setIsMinute(false)} flag={!isMinute}><h4>1시간 데이터</h4></HeaderElement>
            </Header>
            {
                elementData.loading ? <LoaderCotainer><Loader type="TailSpin" color="#a9eef5" height={100} width={100}/></LoaderCotainer> :
                <Frame>
                    <Section>
                        <SectionHeader>
                            <SectionHeaderElement basis={4}>시간</SectionHeaderElement>
                            <SectionHeaderElement basis={1}>시가</SectionHeaderElement>
                            <SectionHeaderElement basis={1}>고가</SectionHeaderElement>
                            <SectionHeaderElement basis={1}>저가</SectionHeaderElement>
                            <SectionHeaderElement basis={1}>종가</SectionHeaderElement>
                            <SectionHeaderElement basis={1}>평균</SectionHeaderElement>
                            <SectionHeaderElement basis={1}>UP/DN</SectionHeaderElement>
                            <SectionHeaderElement basis={1}>Signal</SectionHeaderElement>
                            <SectionHeaderElement basis={1}>2개 1.0</SectionHeaderElement>
                            <SectionHeaderElement basis={1}>2개 1.5</SectionHeaderElement>
                            <SectionHeaderElement basis={1}>1개 1.0</SectionHeaderElement>
                            <SectionHeaderElement basis={1}>1개 1.5</SectionHeaderElement>
                        </SectionHeader>
                        <SectionBody>
                        {
                            elementData.data?.map((element) => {
                                return(
                                    <SectionBodyContainer key={element.datetime.replace("T", " ").substring(0, 16)} id={element.datetime.replace("T", " ").substring(0, 16)}>
                                        <SectionBodyElement basis={4}>{element.datetime.replace("T", " ").substring(0, 16)}</SectionBodyElement>
                                        <SectionBodyElement basis={1}>{element.open_price}</SectionBodyElement>
                                        <SectionBodyElement basis={1}>{element.max_price}</SectionBodyElement>
                                        <SectionBodyElement basis={1}>{element.min_price}</SectionBodyElement>
                                        <SectionBodyElement basis={1}>{element.close_price}</SectionBodyElement>
                                        <SectionBodyElement basis={1}>{element.avg_price}</SectionBodyElement>
                                        <SectionBodyElement basis={1}>{element.continue_up_down}</SectionBodyElement>
                                        <SectionBodyElement basis={1}>{element.signal}</SectionBodyElement>
                                        <SectionBodyElement basis={1}>{element.work_one_1_0}</SectionBodyElement>
                                        <SectionBodyElement basis={1}>{element.work_one_1_5}</SectionBodyElement>
                                        <SectionBodyElement basis={1}>{element.work_two_1_0}</SectionBodyElement>
                                        <SectionBodyElement basis={1}>{element.work_two_1_5}</SectionBodyElement>
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