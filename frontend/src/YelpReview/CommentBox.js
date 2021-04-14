import React, { useRef } from 'react';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBackspace, faFlag } from '@fortawesome/free-solid-svg-icons';

import './CommentBox.css';

const DEFAULT_PROFILE_PIC = 'https://s3-media3.fl.yelpcdn.com/photo/O8CmQtEeOUvMTFk0iMn5sw/o.jpg';

export default ({ text, userId, author, restaurantId, reviewId, profile, commentId, hidden, onClose, onReport }) => {
  const textInput = useRef(null);
  const onDeleteClick = e => {
    fetch(`/restaurant/profile/${restaurantId}/comment_delete/${commentId}`).then(res => {
      if (res.ok) location.reload();
    });
  };
  const onReplyClick = e => {
    fetch(`/restaurant/profile/${restaurantId}/comment_edit/${reviewId}?text=${textInput.current.value}`).then(res => {
      if (res.ok) location.reload();
    })
  };
  const isAuthor = userId === author;

  // new comment edit box
  if (!commentId) {
    return (
      <div className="comment__wrapper">
        <div className="comment__alignment"></div>
        <div className="comment__container">
          <input type="text" name="text" className="form-control form-control-sm w-50 d-inline-block" ref={textInput}/>
          <button type="submit" className="btn btn-sm btn-primary ml-2" onClick={onReplyClick}>Submit</button>
          <button type="button" className="btn btn-sm btn-secondary ml-2" onClick={onClose}>Cancel</button>
        </div>
      </div>
    );
  }

  if (hidden && !isAuthor) return null;

  return (
    <div className="d-flex" className="comment__wrapper">
      <div className="comment__alignment"></div>
      <div className="comment__container">
        <img className="comment__profile__pic" style={{opacity: hidden ? 0.5 : 1}} src={profile ? profile : DEFAULT_PROFILE_PIC} />
        <div className="text-muted text-sm text-truncate comment__text" style={{opacity: hidden ? 0.5 : 1}}>
          <span className="d-inline-block text-truncate" style={{width: hidden ? '20%' : '100%'}}>{ text }</span>
          { hidden ? 
            <em className="text-danger d-inline-block ml-1" style={{fontSize: '0.6rem', lineHeight: '0.8rem', verticalAlign: 'text-top'}}>
              This comment is only visible to you
            </em> : null
          }
        </div>
        {
          isAuthor ? (
            <i className="text-primary btn btn-sm ml-1" onClick={onDeleteClick}>
              <FontAwesomeIcon icon={faBackspace} />
            </i>
          ) : (
            <i className="text-secondary btn btn-sm ml-1" onClick={e => { onReport(e); __data__.reportAbuse.type = REPORT_TYPE.COMEMNT; }}>
              <FontAwesomeIcon icon={faFlag} />
            </i>
          )
        }
      </div>
    </div>
  );
};
