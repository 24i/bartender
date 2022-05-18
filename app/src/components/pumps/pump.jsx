import React, { useEffect, useState, useRef } from 'react';
import listOfDrinks from '../../drinks';
import Cocktail from '../icons/cocktail';

const findIconOrDefault = (drink) => {
    const Component = listOfDrinks[drink]?.icon || Cocktail;
    return <Component />;
}

const drinks = Object.keys(listOfDrinks).map(id => {
    return { id, ...listOfDrinks[id] };
});

const Pump = ({ value }) => {

    const [ selectedDrink, setSelectedDrink ] = useState(value.drink);

    const onChangeDrink = (e) => {
        const drink = e.target.value;

        // Set internal state
        setSelectedDrink(drink);
    }

    const first = useRef(false);
    useEffect(() => {

        // Skip on first load
        if (!first.current) {
            first.current = true;
            return;
        }

        const wait = setTimeout(() => { 
            fetch('http://localhost:8080/pumps', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id: value.id,
                    drink: selectedDrink
                })
            });
        }, 1000);

        return () => clearTimeout(wait);
    }, [selectedDrink]);

    return (
        <div className="max-w-sm rounded-lg border shadow-md bg-gray-800 border-gray-700 mb-8">
            <div className="flex flex-col items-center pb-10 pt-10">
                <div className="mb-3 w-24 h-24 rounded-full shadow-lg flex justify-center items-center">
                    {findIconOrDefault(selectedDrink)}
                </div>
                <h3 className="mb-1 text-xl font-medium text-gray-900 dark:text-white">Pump {value.id}</h3>
                <input list={`drinks-${value.id}`} type="text" className='rounded' value={selectedDrink} onChange={onChangeDrink} />
                <datalist id={`drinks-${value.id}`}>
                    {drinks.map(drink => (
                        <option key={drink.id} value={drink.id}>{drink.name}</option>
                    ))}
                </datalist>
            </div>
        </div>
    )

};

export default Pump;