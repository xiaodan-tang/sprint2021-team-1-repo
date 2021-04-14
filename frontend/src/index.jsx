import React from 'react';
import { render } from 'react-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import App from './App';

render(<App 
            yelpReviews={yelpReviews} 
            internalReviews={internalReviews} 
            restaurantId={restaurantId} 
            userId={userId} 
        />, 
        document.getElementById('root')
);
