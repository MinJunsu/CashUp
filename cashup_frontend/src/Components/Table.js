import React from 'react';
import styled from 'styled-components';

const Div = styled.div`
    width: 100%;
    height: 500px;
    overflow-x: auto;
`;

const STable = styled.table`
    width: 100%;
    min-width: 500px;
    white-space: nowrap;
    background-color: rgba(0, 0, 0, 0);
    text-align: center;
`;

const TR = styled.tr`
`;

const Header = styled.th`
    border: 1px solid;
`;

const Data = styled.td`
    margin-right: 2px;
    opacity: 0.8;
`;

const NullData = styled.td`
    padding: 1px;
    height: 1px;
    background-color: black;
    opacity: 0.3;

`;

function Table({ columns, data }) {
    return (
        <Div>
            <STable>
                <thead>
                    <TR>{columns.map((column) => <Header>{column}</Header>)}</TR>
                </thead>
                <tbody>
                    {
                        data.map((row) => {
                            if(row.type) {
                                return (
                                    <TR>{Object.values(row).map((element, idx) => {
                                        if(idx !== Object.values(row).length - 1) {
                                            return (
                                                <Data>{element}</Data>
                                            );
                                        }
                                    })}</TR>
                                );
                            } else {
                                return (
                                    <TR>{Object.values(row).map((element) => <NullData></NullData>)}</TR>
                                );
                            }
                        })
                    }
                </tbody>
            </STable>
        </Div>
    );
}

export default Table;