import React, { useState, useEffect } from "react";

import TestTradePresenter from "Pages/TestTrade/TestTradePresenter";
import { RequestGetter } from "API/TradeGetter";

interface IProps {

}

function TestTradeContainer({}: IProps) {
    return(
        <TestTradePresenter/>
    );
}

export default TestTradeContainer;