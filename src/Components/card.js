import React from "react";

export const Card = ({listOfEvents}) => {
    return (
        <>
            {listOfEvents.map(event => {
                return(
                    <ul>
                        <li>{event.start} - {event.end}</li>
                    </ul>
                )
            })}
        </>
    )
}