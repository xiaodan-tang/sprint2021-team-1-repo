import React, {useState, useEffect} from 'react';
import "./YelpReview.css";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStar } from '@fortawesome/free-solid-svg-icons'

const DEFAULT_AVATAR = 'https://s3-media3.fl.yelpcdn.com/photo/O8CmQtEeOUvMTFk0iMn5sw/o.jpg';

const formatDate = d => {
    d = new Date(d);
    return `${d.getFullYear()}-${(d.getMonth() + 1).toString().padStart(2, '0')}-${d.getDate().toString().padStart(2, '0')} ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}:${d.getSeconds().toString().padStart(2, '0')}`;
};
function YelpReview({ review, isInternal }) {
    const data = {
        userId: isInternal ? review.user : null,
        userName: isInternal ? review.user__username : (review.user ? review.user.name : null),
        profilePic: isInternal ? review.user__user_profile__photo : (review.user ? review.user.image_url : null),
        reviewId: isInternal ? null : review.id,
        reviewUrl: isInternal ? null : review.url,
        rating: review.rating,
        time: formatDate(isInternal ? review.time : review.time_created),
        content: isInternal ? review.content : review.text,
        image1: isInternal ?  review.image1 : null,
        image2: isInternal ?  review.image2 : null,
        image3: isInternal ?  review.image3 : null,
        hidden: isInternal ? review.hidden : false,
        comments: review.comments
    }

    const [showDropdown, setShowDropdown] = useState(false);
    return (
        <div className="yelp__root" onMouseLeave={() => setShowDropdown(false)}>
            <div className="yelp__body d-block d-sm-flex">
                <div className="yelp__pic_date">
                    <div>
                        <img src={data.profilePic || DEFAULT_AVATAR} className="yelp__pic p-2"/>
                    </div>
                    <div className="yelp__date text-muted">
                        {data.time}
                    </div>
                </div>
                <div className = "yelp__name_rating_text mt-2 mb-1 text-muted">
                    <div className="yelp__name">
                        <a href={data.reviewUrl}>
                            {data.userName}
                        </a>
                    </div>
                    <div className="yelp__rating">
                        { Array(data.rating).fill(0).map((_, i) => 
                            <FontAwesomeIcon key={i} icon={faStar} className="text-primary text-sm" /> ) 
                        }
                    </div>
                    <div className="yelp__text text-sm">
                        {data.content}
                    </div>
                    <div className="d-flex">
                        { data.image1 ? <img className="review__image" src={data.image1} /> : null }
                        { data.image2 ? <img className="review__image" src={data.image2} /> : null }
                        { data.image3 ? <img className="review__image" src={data.image3} /> : null }
                    </div>
                    
                </div>
                <div className="dropdown" >
                    <svg viewBox="0 0 24 24" preserveAspectRatio="xMidYMid meet" className="dropdown-toggle dropdown__icon" type="button" onClick={() => setShowDropdown(true)}><g><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"></path></g></svg>
                    <div className={`dropdown-menu p-0 ${showDropdown ? 'show' : ''}`}>
                        <a className="dropdown-item small py-2" href="#">Edit</a>
                        <a className="dropdown-item small py-2" href="#">Delete</a>
                        <a className="dropdown-item small py-2" href="#">Reply</a>
                        <a className="dropdown-item small py-2" href="#">Report</a>
                    </div>
                </div>
            </div>      
        </div>
    )
}

export default YelpReview
