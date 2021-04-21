import React from 'react'
import "./OpeningHours.css"

const OpeningHours = () => {
    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    function changeTime(time) {
        time = time.substring(0, time.length-2).concat(":00")
        time = new Date("1/1/20 " + time)
        return time.toLocaleString('en-US', {hour : 'numeric', minute: 'numeric', hour12: true})
    }

    return (
        <div>
            <div className="card border-0 shadow mb-5">
                <div className="card-header bg-gray-100 py-4 border-0">
                    <div className="media align-items-center">
                        <div className="media-body">
                            <h4 className="mb-0">Opening Hours </h4> </div>
                            <svg className="svg-icon svg-icon svg-icon-light w-3rem h-3rem ml-3 text-muted">
                                <use xlinkHref="#wall-clock-1"> </use>
                            </svg>
                        </div>
                    </div>
                <div className="card-body">
                <table id="res_open_hours" className="table text-sm mb-0">
                    {
                        yelp_info.hours[0].open.map((elem, idx) => {
                          return (  <tr>
                                <th className="pl-0" rowspan="1">
                                    {days[elem["day"]]}
                                </th>
                                <td className="pr-0 text-right">
                                    { changeTime(elem["start"]) + "-" + changeTime(elem["end"])}
                                </td>
                            </tr>
                        )})
                    }
                </table>
            </div>
        </div>
    </div>
    )
}

export default OpeningHours;
