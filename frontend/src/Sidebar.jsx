import React from 'react';
import { render } from 'react-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import OpeningHours from './components/OpeningHours/OpeningHours';


console.log('i am the sidebar.')
render(<OpeningHours 
            // restaurantId={restaurantId} 
        />, 
            
        document.getElementById('sidebar')
        
        );
