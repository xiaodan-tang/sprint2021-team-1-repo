import { hot } from 'react-hot-loader';
import React, {useState, useEffect} from 'react';
import './App.css';

import YelpReview from "./YelpReview";
// import yelpReviews from "../../yelp_data.json";

const App = ({yelpReviews, internalReviews}) => (
  <div className="App">
    <h6>
      <span class="text-primary">YELP</span> REVIEWS
    </h6>
    {yelpReviews.reviews.map((review, idx) => <YelpReview key={idx} review={review}/>)}
    <hr/>
    <h6>
      <span class="text-primary">INTERNAL</span> REVIEWS
    </h6>
    {internalReviews.map((review, idx) => <YelpReview key={idx} review={review} isInternal/>)}
  </div>
);

// export default hot(module)(App);
export default App;
