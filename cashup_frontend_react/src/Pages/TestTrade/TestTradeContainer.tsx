import React, { useState, useEffect } from "react";

import TestTradePresenter from "Pages/TestTrade/TestTradePresenter";
import { IStateTrade } from "Types/DBTypes";
import { RequestGetter } from "API/TradeGetter";

interface IProps {

}

function TestTradeContainer({}: IProps) {
    const [ version1, setVersion1 ] = useState<IStateTrade>({ loading: true, long: [], long_finished: [], short: [], short_finished: [] });
    const [ version2, setVersion2 ] = useState<IStateTrade>({ loading: true, long: [], long_finished: [], short: [], short_finished: [] });
    const [ version3, setVersion3 ] = useState<IStateTrade>({ loading: true, long: [], long_finished: [], short: [], short_finished: [] });
    return(
        <TestTradePresenter/>
    );
}

export default TestTradeContainer;