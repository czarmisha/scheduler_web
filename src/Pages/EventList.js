import { Table } from 'antd';
import React from 'react';
import { useEffect, useState } from 'react';

export const EventList = (props) => {
    const [events, setEvents] = useState([])
    const [interval, setFetchInterval] = useState()
    
    useEffect(()=>{
        clearInterval(interval)
        fetch(`/api/get-events/${props.period}`).then(response => {
            if(response.ok){
                return response.json()
            }
        }).then(data => setEvents(data))
        let fetchInterval = setInterval(() => {
            fetch(`/api/get-events/${props.period}`).then(response => {
                if(response.ok){
                    return response.json()
                }
            }).then(data => setEvents(data))
        }, 30000);
        setFetchInterval(fetchInterval)
    },[props])
    const columns = [
        {
          title: 'time',
          dataIndex: 'time',
          key: 'time',
        },
        {
          title: 'name',
          dataIndex: 'name',
          key: 'name',
        },
        {
          title: 'description',
          dataIndex: 'description',
          key: 'description',
        },
      ];
      const dataSource = events.map(function(event, index){
        return {'key': index, 'time': `${event.start.slice(17, 22)}-${event.end.slice(17, 22)}`, 'name': event.author_firstname, 'description': event.description, rowSpan: 6}
      });
    return <Table dataSource={dataSource} columns={columns} />;
}