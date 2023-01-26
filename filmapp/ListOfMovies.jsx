import React from 'react';
import MovieCard from './MovieCard'; 

const ListOfMovies=({movies}) => { 
    return (
            movies?.length > 0 ? 
            ( 
                <div className="container"> 
                    {movies.map((movie) => <MovieCard movie={movie} />)} 
                </div> 
            ) : ( 
                <div className="empty"> 
                    <h2> No movies found </h2> 
                </div> 
            ) 
    );
}

export default ListOfMovies; 
