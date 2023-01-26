import React from 'react'; 
import SearchIcon from './SearchIcon.png'; 
import {useState} from 'react';

const Search = ({myFunction}) => { 
    const [searchTerm,setSearchTerm]=useState('');
    return (
            <div className="search"> 
                    <input  
                        type="text" 
                        placeholder="Search for movies" 
                        value={searchTerm} 
                        onChange= {(e) => setSearchTerm(e.target.value)}  
                    /> 
                    <img 
                        src={SearchIcon} 
                        alt="search" 
                        onClick = { () => myFunction(searchTerm)}  
                    /> 
            </div> 
    );
}

export default Search; 
