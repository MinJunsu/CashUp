import React, { useEffect, useState } from 'react';
import SimulatePresenter from 'Pages/Simulate/SimulatePresenter';
import { getSimulateData } from 'api';

function SimulateContainer() {
    const [ loading, setLoading ] = useState(false);
    const [ formData, setFormData ] = useState();
    const [ data, setData ] = useState([]);
    const [ result, setResult ] = useState({});
    const columns = [
        '구매 방식',
        '구매 호가 시간',
        '구매량',
        '구매 시간',
        '구매 가격',
        '판매 호가 시간',
        '판매 시간',
        '판매 가격',
        '최대',
        '최소',
        '손익률'
    ]
    useEffect(
        async () => {
            if(formData) {
                try {
                    setLoading(true);
                    const { data: { data: results, result: result } } = await getSimulateData(formData);
                    setResult(result);
                    setData(results);
                } catch (e){
                    console.log(e);
                } finally {
                    setLoading(false);
                }
            }
        }, [formData]
    );
    return (
        <SimulatePresenter setFormData={setFormData} result={result} columns={columns} data={data} loading={loading}/>
    );
};

export default SimulateContainer;