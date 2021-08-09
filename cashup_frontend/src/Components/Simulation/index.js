import React from 'react';
import styled from 'styled-components';
import { ClipLoader } from 'react-spinners';

import Table from 'Components/Table';
import SimulateForm from 'Components/Simulation/SimulateForm';
import SimulationResult from 'Components/Simulation/SimulateResult';

const Container = styled.div`
    border: 1px solid;
    border-radius: 5px;
    width: 100%;
    min-height: 300px;
`;

const Result = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    position: relative;
`;

const Form = styled.div`
    padding-left: 5px;
`;

function Simulation(props) {
    return (
        <Container>
            <Form>
                <SimulateForm setFormData={props.setFormData}></SimulateForm>
            </Form>
            <Result>
                {
                    props.loading ? <ClipLoader loading={props.loading} size={200}/> :
                    <Result>
                        <Table columns={props.columns} data={props.data}></Table>
                        <SimulationResult result={props.result}></SimulationResult>
                    </Result>
                }
            </Result>
        </Container>  
    );
}

export default Simulation;