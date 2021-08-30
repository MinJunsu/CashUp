import { Switch, Route, HashRouter as Router } from "react-router-dom";
import styled from "styled-components";

import Headers from "Components/Header";
import Home from 'Pages/Home';
import TestTrade from "Pages/TestTrade";

const Container = styled.div`

`;

export default () => {
    return (
        <Container>
            <Router>
                <Headers/>
                <Switch>
                    <Route path='/'         exact component={Home}/>
                    <Route path='/test'     exact component={TestTrade}/>
                </Switch>
            </Router>
        </Container>
    );
};