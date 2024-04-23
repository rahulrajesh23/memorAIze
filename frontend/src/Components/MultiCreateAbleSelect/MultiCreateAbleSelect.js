import React from 'react';
import CreatableSelect from 'react-select/creatable';

const customStyles = {
    control: (base, state) => ({
        ...base,
        height: '60px',
        minHeight: '60px',
        borderRadius: '.7em',
        backgroundColor: '#c6e3fa61'

    }),
    container: (provided) => ({
        ...provided,
        width: '100%',
        borderRadius: '.7em'
    }),
    valueContainer: (provided) => ({
        ...provided,
        height: '55px',
        overflow: 'auto'
    }),
    placeholder: (provided) => ({
        ...provided,
        color: '#9ca3af'
    })
};

export function MultiCreateAbleSelect(props) {

    const { 
        value,
        onChange,
        options,
        onCreateOption,
        menuPlacement = 'top',
        placeholder = 'Select...'
     } = props
    return (
        <CreatableSelect
            isMulti
            styles={customStyles}
            value={value}
            onChange={onChange}
            options={options}
            onCreateOption={onCreateOption}
            formatCreateLabel={inputValue => `Add "${inputValue}"`}
            menuPlacement={menuPlacement}
            placeholder={placeholder}
        />
    );
}

export default MultiCreateAbleSelect;
