import React from "react"
import { Badge, Calendar } from 'antd';
import { useEffect, useState } from "react"


export const CalendarView = () => {
    const [events, setEvents] = useState([])
    useEffect(()=>{
        fetch('/api/get-all-events').then(response => {
            if(response.ok){
                return response.json()
            }
        }).then(data => setEvents(data))
        setInterval(() => {
            fetch('/api/get-all-events').then(response => {
                if(response.ok){
                    return response.json()
                }
            }).then(data => setEvents(data))
        }, 30000);
    },[])

    const dateCellRender = (value) => {
        let listData = events.length!==0 ? getListData(value) : []

        return (
        <ul className="events">
            {listData.map((item, index) => (
            <li key={index}>
                <Badge status='success' text={item.start.slice(17, 22) + ' ' + item.description.slice(0, 20)} />
            </li>
            ))}
        </ul>
        );
    };
    const getListData = (value) => {
        let listData;
        let date = `${String(value._d).slice(8, 10)} ${String(value._d).slice(4, 7)} ${String(value._d).slice(11, 15)}`
        listData = events.filter(event => event.start.slice(5, 16) === date);
        return listData || [];
      };

    return <Calendar dateCellRender={dateCellRender}/>;
}