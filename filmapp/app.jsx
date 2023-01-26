import {useState,useEffect} from 'react';
import './App.css'; 
import AppTitle from './AppTitle';
import Search from './Search';
import ListOfMovies from './ListOfMovies';

const API_URL = 'http://www.omdbapi.com?apikey=c032e2d7';  

const App = () => { 
    const [movies,setMovies]=useState([]);
    useEffect( ()=>{
        searchMovies('Spiderman');
    }, []);

    const searchMovies = (title) => { 
        fetch(`${API_URL}&s=${title}`) 
        .then( response => response.json()) 
        .then (data => setMovies(data.Search)) 
    }; 
    return ( 
        <div className="app"> 
            <AppTitle /> 
            <Search myFunction = {searchMovies} /> 
            <ListOfMovies movies={movies} /> 
        </div> 
    ); 
    
} 
 
export default App; 
 
