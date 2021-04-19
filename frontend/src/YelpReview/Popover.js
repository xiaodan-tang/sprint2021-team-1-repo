import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStar } from '@fortawesome/free-solid-svg-icons';

const Ratings = ({ r }) => {
  return (
    <>
      {
        Array(5).fill(0).map((el, i) => <i key={i}><FontAwesomeIcon icon={faStar} className={`${i < r ? 'text-primary' : 'text-muted'} text-sm`} /></i>)
      }
    </>
  )
};

export default ({ rating_safety, rating_door, rating_table, rating_bathroom, rating_path }) => {
  return (
    <div
      className="popover fade bs-popover-bottom show"
      role="tooltip"
      style={{willChange: 'transform', position: 'absolute', top: '1.3rem', left: '-5rem' }}
      x-placement="right"
    >
      <div className="arrow" style={{left: '50%', transform: 'translate(-50%)'}}></div>
      <h3 className="popover-header"></h3>
      <div className="popover-body">
        <div>
          <span style={{ width: '5rem' }} className="d-inline-block">Safety</span>
          <Ratings r={rating_safety}/>
        </div>
        <h6 className="border-bottom mt-3 mb-0 pb-1">Accessibility</h6>
        <div>
          <span style={{ width: '5rem' }} className="d-inline-block">Doors</span>
          <Ratings r={rating_door}/>
        </div>
        <div>
          <span style={{ width: '5rem' }} className="d-inline-block">Tables</span>
          <Ratings r={rating_table}/>
        </div>
        <div>
          <span style={{ width: '5rem' }} className="d-inline-block">Bathroom</span>
          <Ratings r={rating_bathroom}/>
        </div>
        <div>
          <span style={{ width: '5rem' }} className="d-inline-block">Pathways</span>
          <Ratings r={rating_path}/>
        </div>
      </div>
    </div>
  );
};
