import React from 'react';
import styled from 'styled-components';

import Simulation from 'Components/Simulation';

const Container = styled.div`

`;

function SimulatePresenter(props) {
    return (
        <Container>
            <Simulation setFormData={props.setFormData} result={props.result} columns={props.columns} data={props.data} loading={props.loading}/>
        </Container>
    );
};

export default SimulatePresenter;