import { Switch, Route, HashRouter as Router } from "react-router-dom";
import styled from "styled-components";


import Home from 'Pages/Home';
import Simulate from 'Pages/Simulate';
import Headers from "Components/Headers";

const Container = styled.div`

`;

export default () => {
    return (
        <Container>
            <Router>
                <Headers/>
                <Switch>
                    <Route path='/'         exact component={Home}/>
                    <Route path='/simulate' exact component={Simulate}/>
                </Switch>
            </Router>
        </Container>
    );
};