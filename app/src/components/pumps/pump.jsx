import React, { useState } from 'react';
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
        console.log(e.target.value)
        setSelectedDrink(e.target.value);
    }

    console.log(selectedDrink);
    return (
        <div className="max-w-sm rounded-lg border shadow-md bg-gray-800 border-gray-700">
            <div className="flex flex-col items-center pb-10 pt-10">
                <div className="mb-3 w-24 h-24 rounded-full shadow-lg flex justify-center items-center">
                    {findIconOrDefault(selectedDrink)}
                </div>
                <h3 className="mb-1 text-xl font-medium text-gray-900 dark:text-white">Pump {value.id}</h3>
                <select className='rounded' value={selectedDrink} onChange={onChangeDrink}>
                    <option value="UNKNOWN">-- Not Set --</option>
                    {drinks.map(drink => (
                        <option value={drink.id}>{drink.name}</option>
                    ))}
                </select>
            </div>
        </div>
    )

};

export default Pump;