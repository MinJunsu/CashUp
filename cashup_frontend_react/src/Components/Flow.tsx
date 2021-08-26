import React from "react";
import styled from "styled-components";
import Loader from "react-loader-spinner";

import { IFlow } from "Types/DBTypes";

const Container = styled.div`
    text-align: center;
    flex: 1;
    border: 1px solid;
`;

const LoaderCotainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 95%;
`;

const Header = styled.h4`
    vertical-align: middle;
    margin-top: 4px;
    margin-bottom: 4px;
    border-bottom: 1px solid;
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
    margin-top: 2px;
    margin-bottom: 2px;
    flex: ${(props) => props.basis};
`;
const SectionBody = styled.div`
    font-size: 14px;
    overflow-y: scroll;
    max-height: 400px;
`;

const SectionBodyContainer = styled.div`
    display: flex;
    border-bottom: 1px solid;
`;

const SectionBodyElement = styled.span<{ basis: number }>`
    flex: ${(props) => props.basis};
    justify-content: center;
    padding-left: 1px;
    padding-right: 1px;
`;

interface IProps {
    loading: boolean,
    title: string,
    flow: IFlow[] | null
}

function Flow({ loading, title, flow }: IProps) {
    return(
        <Container>
            <Header>{title} 흐름 데이터</Header>
            {
                loading ? <LoaderCotainer><Loader type="TailSpin" color="#a9eef5" height={100} width={100}/></LoaderCotainer>:
                <Frame>
                    <Section>
                        <SectionHeader>
                            <SectionHeaderElement basis={4}>시간</SectionHeaderElement>
                            <SectionHeaderElement basis={1}>가격</SectionHeaderElement>
                            <SectionHeaderElement basis={1}>흐름</SectionHeaderElement>
                            <SectionHeaderElement basis={1}>확인</SectionHeaderElement>
                            <SectionHeaderElement basis={1}>거래</SectionHeaderElement>
                        </SectionHeader>
                        <SectionBody>
                        {
                            flow?.map((element) => {
                                return(
                                    <SectionBodyContainer>
                                        <SectionBodyElement basis={4}>{element.datetime.replace("T", " ").substring(0, 16)}</SectionBodyElement>
                                        <SectionBodyElement basis={1}>{element.base_price}</SectionBodyElement>
                                        <SectionBodyElement basis={1}>{element.flow}</SectionBodyElement>
                                        <SectionBodyElement basis={1}>{element.flow_confirm}</SectionBodyElement>
                                        <SectionBodyElement basis={1}>{element.flow_trade}</SectionBodyElement>
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

export default Flow;