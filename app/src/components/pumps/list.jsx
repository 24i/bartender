import React, { useState, useEffect } from 'react';
import Pump from './pump';

const PumpList = () => {

    const [ pumps, setPumps ] = useState([]);

    useEffect(() => {
        const fetchPumps = async () => {
            const response = await fetch('http://localhost:8080/pumps');
            const body = await response.json();

            setPumps(body);
        }
        fetchPumps();
    }, []);

    if (!pumps.length) {
        return <div />;
    }

    return (
        <>
            <div className='container mb-10'>
                <div className='columns-3'>
                    {pumps.slice(0, 3).map(pump => <Pump key={pump.id} value={pump} />)}
                </div>
            </div>
            <div className='container'>
                <div className='columns-3'>
                {pumps.slice(3).map(pump => <Pump key={pump.id} value={pump} />)}
                </div>
            </div>
        </>
    )

}

export default PumpList;