import React from "react";
import HomePresenter from "Pages/Home/HomePresenter";

interface IProps {

}

interface IState {

}

function HomeContainer({}: IProps, {}: IState) {
    return(
        <div>
            <HomePresenter/>
        </div>
    );
}

export default HomeContainer;