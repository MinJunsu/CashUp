import { Switch, Route, HashRouter as Router } from "react-router-dom";
import styled from "styled-components";

import Home from 'Pages/Home';
import Headers from "Components/Header";

const Container = styled.div`

`;

export default () => {
    return (
        <Container>
            <Router>
                <Headers/>
                <Switch>
                    <Route path='/'         exact component={Home}/>
                </Switch>
            </Router>
        </Container>
    );
};