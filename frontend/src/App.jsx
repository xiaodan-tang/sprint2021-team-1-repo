import { hot } from 'react-hot-loader';
import React, {useState, useEffect} from 'react';
import './App.css';

import YelpReview from "./YelpReview";

const App = ({ yelpReviews, internalReviews, restaurantId, userId }) => {
  const initialFormData = Object.freeze({
    email: "",
  });
  const [formData, updateFormData] = useState(initialFormData)
  const handleChange = (e) => {
    updateFormData({
      ...formData,
      [e.target.name] : e.target.value
    });
  };
  const [email, setEmail] = useState("");
  const handleSubmit = (e) => {
    console.log(formData);
  };
  return (
    <div className="App">
        <div className="sharebutton">
            <h2> Share this restaurant! </h2>
              <input  type="text" default="Email" name="Email" placeholder="Email" label="Email" variant="outlined" multiline rows={4} onChange={(e) => setEmail(e.target.value)}  />
              <a href={`mailto:${email}?subject=Check out this Restaurant on DineLine &body=The restaurant is: ${yelp_info.name}%0D%0A${window.location.href}`}  type="button" onClick={handleSubmit}> 
                        Share
              </a>
        </div>

      <h6>
        <span className="text-primary">YELP</span> REVIEWS
      </h6>
      {yelpReviews.reviews.map((review, idx) => <YelpReview key={idx} review={review} restaurantId={restaurantId} userId={userId}/>)}
      <hr/>
      <h6>
        <span className="text-primary">DINELINE</span> REVIEWS
      </h6>
      {internalReviews.map((review, idx) => <YelpReview key={idx} review={review} restaurantId={restaurantId} userId={userId} isInternal/>)}
  </div>
  )
  };

export default hot(module)(App);
