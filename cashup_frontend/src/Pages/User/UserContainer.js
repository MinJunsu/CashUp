import React from 'react';
import styled from 'styled-components';

import UserPresenter from 'Pages/User/UserPresenter';

const Container = styled.div`

`;

function UserContainer() {
    return (
        <Container>
            <UserPresenter></UserPresenter>
        </Container>
    );
}

export default UserContainer;