import React, { useState } from 'react';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStar, faHeart } from '@fortawesome/free-solid-svg-icons';

import CommentBox from './CommentBox';
import "./YelpReview.css";

const DEFAULT_AVATAR = 'https://s3-media3.fl.yelpcdn.com/photo/O8CmQtEeOUvMTFk0iMn5sw/o.jpg';
const AWS_S3_MDEIA = 'https://dineline.s3.amazonaws.com/media/';

const formatDate = d => {
    d = new Date(d);
    return `${d.getFullYear()}-${(d.getMonth() + 1).toString().padStart(2, '0')}-${d.getDate().toString().padStart(2, '0')} ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}:${d.getSeconds().toString().padStart(2, '0')}`;
};

const RatingFooter = ({ isInternal, onLikeClick, liked, likesCount, isAuthor, hidden }) => {
    if (hidden) {
        return (
            isAuthor ? <em className="text-danger d-inline-block" style={{fontSize: '0.6rem', lineHeight: '0.8rem'}}>
                This post is only visible to you because it violates our terms of service
            </em> : null
        );
    }
    return (
        isInternal ? (
            <div>
                <i className="btn p-0" onClick={onLikeClick}>
                    <FontAwesomeIcon icon={faHeart} className={`${liked ? 'text-primary' : 'text-secondary'}`}/>
                </i>
                <span className="pl-3">{ likesCount }</span>
            </div>
        ) : null
    );
};

export default ({ review, restaurantId, userId, isInternal }) => {
    const data = {
        id: isInternal ? review.id : null,
        userId: isInternal ? review.user : null,
        userName: isInternal ? review.user__username : (review.user ? review.user.name : null),
        profilePic: isInternal ? review.user__user_profile__photo : (review.user ? review.user.image_url : null),
        reviewId: isInternal ? null : review.id,
        reviewUrl: isInternal ? null : review.url,
        rating: review.rating,
        time: formatDate(isInternal ? review.time : review.time_created),
        content: isInternal ? review.content : review.text,
        image1: isInternal ? review.image1 : null,
        image2: isInternal ? review.image2 : null,
        image3: isInternal ? review.image3 : null,
        hidden: isInternal ? review.hidden : false,
        comments: review.comments || []
    };

    const [showDropdown, setShowDropdown] = useState(false);
    const [showCreateComment, setShowCreateComment] = useState(false);
    const [liked, setLiked] = useState(isInternal ? review.liked : null);
    const [likesCount, setLikesCount] = useState(isInternal ? review.likes_num : 0);
    const [commentIndex, setCommentIndex] = useState(3);
    const isAuthor = data.userId === userId;

    const onReplyClick = e => {
        e.preventDefault();
        setShowDropdown(false);
        setShowCreateComment(true);
    };

    const onReportClick = e => {
        e.preventDefault();
        setShowDropdown(false);
        // Add this to communicate with non-react code
        if (typeof $ === 'undefined') return;
        $('#report-abuse-modal').modal('show');
        __data__.reportAbuse.type = REPORT_TYPE.REVIEW;
        __data__.reportAbuse.id = data.id;
    };

    const onEditClick = e => {
        e.preventDefault();
        setShowDropdown(false);
        // Add this to communicate with non-react code
        if (typeof $ === 'undefined') return;
        $('#exampleModal').modal('toggle');
        const rating = document.querySelector('select[name="rating"]');
        rating.value = data.rating;
        rating.dispatchEvent(new Event('change'));
        const content = document.querySelector('textarea[name="content"]');
        content.value = data.content;
        content.dispatchEvent(new Event('change'));
        document.forms['rating-form'].setAttribute('action', `/restaurant/profile/${restaurantId}/review/${data.id}/put/restaurant`);
    };

    const onDeleteClick = e => {
        e.preventDefault();
        setShowDropdown(false);
        fetch(`/restaurant/profile/${restaurantId}/review/${data.id}/delete/restaurant`).then(res => {
            if (res.ok) {
                location.reload();
            }
        });
    };

    const onLikeClick = () => {
        fetch(`/restaurant/like/review/`, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'content-type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]')?.value
            },
            body: `review_id=${Number(data.id)}`
        }).then(r => {
            if (!r.ok) return;
            return r.json();
        }).then(r => {
            setLiked(r.liked);
            setLikesCount(r.likes_num);
        });
    };

    const onImageClick = (img) => {
        const zoomModal = document.getElementById("myModal");
        zoomModal.style.display = "block";
        const modalImg = document.getElementById("img01");
        modalImg.src = img;
    };

    if (data.hidden && !isAuthor) return null;
    return (
        <div className="yelp__root mt-2" onMouseLeave={() => setShowDropdown(false)}>
            <div className="yelp__body d-block d-sm-flex">
                <div className="yelp__pic_date" style={{ opacity: data.hidden ? 0.5 : 1 }}>
                    <div className="text-center">
                        <img src={data.profilePic || DEFAULT_AVATAR} className="yelp__pic p-2" style={{ cursor: 'pointer' }} onClick={() => window.open(`/user/facing_page/${userId}`, '_blank') }/>
                    </div>
                    <div className="yelp__date text-muted text-sm">
                        {data.time}
                    </div>
                </div>
                <div className = "yelp__name_rating_text text-muted" style={{ opacity: data.hidden ? 0.5 : 1 }}>
                    <div className="yelp__name">
                        <a href={`/user/facing_page/${userId}`}>
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
                    <div className="d-flex overflow-auto review__image__container">
                        { data.image1 ? <img className="review__image" src={new URL(data.image1, AWS_S3_MDEIA).href} onClick={() => onImageClick(new URL(data.image1, AWS_S3_MDEIA).href)}/> : null }
                        { data.image2 ? <img className="review__image" src={new URL(data.image2, AWS_S3_MDEIA).href} onClick={() => onImageClick(new URL(data.image2, AWS_S3_MDEIA).href)}/> : null }
                        { data.image3 ? <img className="review__image" src={new URL(data.image3, AWS_S3_MDEIA).href} onClick={() => onImageClick(new URL(data.image3, AWS_S3_MDEIA).href)}/> : null }
                    </div>
                    <RatingFooter
                        isInternal
                        onLikeClick={onLikeClick}
                        liked={liked}
                        likesCount={likesCount}
                        isAuthor
                        hidden={data.hidden}
                    />
                </div>
                {
                    isInternal ? (
                        <div className="dropdown">
                            <svg viewBox="0 0 24 24" preserveAspectRatio="xMidYMid meet" className="dropdown-toggle dropdown__icon" type="button" onClick={() => setShowDropdown(true)}><g><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"></path></g></svg>
                            <div className={`dropdown-menu p-0 ${showDropdown ? 'show' : ''}`}>
                                <a className={`dropdown-item small py-2 ${isAuthor ? '' : 'd-none'}`} href="#" onClick={onEditClick}>Edit</a>
                                <a className={`dropdown-item small py-2 ${isAuthor ? '' : 'd-none'}`} href="#" onClick={onDeleteClick}>Delete</a>
                                <a className={`dropdown-item small py-2 ${data.hidden ? 'd-none' : ''}`} href="#" onClick={onReplyClick}>Reply</a>
                                <a className={`dropdown-item small py-2 ${isAuthor ? 'd-none' : ''}`} href="#" onClick={onReportClick}>Report</a>
                            </div>
                        </div>
                    ) : null
                }
            </div>
            { data.comments.slice(0, commentIndex).map((el, index) => {
                return <CommentBox key={index} {...el} userId={userId} restaurantId={restaurantId} reviewId={data.id} onReport={onReportClick} />;
              })
            }
            {
                commentIndex < data.comments.length ? <div className="text-primary text-sm text-center showmore__button d-flex justify-content-center align-items-center" onClick={() => { setCommentIndex(Math.min(commentIndex + 3, data.comments.length)) }}>show more...</div> : null
            }
            { showCreateComment ? <CommentBox userId={userId} restaurantId={restaurantId} reviewId={data.id} onClose={() => setShowCreateComment(false)} /> : null }
        </div>
    )
};
