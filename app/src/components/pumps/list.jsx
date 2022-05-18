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
                <div className='lg:columns-3 md:columns-2 sm:columns-1 sm:items-center gap-8'>
                    {pumps.map(pump => <Pump key={pump.id} value={pump} />)}
                </div>
            </div>
        </>
    )

}

export default PumpList;