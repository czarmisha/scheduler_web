import { Table } from 'antd';
import { Link } from "react-router-dom";
import React from 'react';
import { useEffect, useState } from 'react';

export const MyEvents = () => {
    const [events, setEvents] = useState([])
    const [interval, setFetchInterval] = useState()
    const [user, setUser] = useState({});

    useEffect(()=>{
        clearInterval(interval)

        const loggedInUser = localStorage.getItem("user");
        if (loggedInUser) {
            const foundUser = JSON.parse(loggedInUser);
            setUser(foundUser);

            fetch(`/api/get-events-by-id/${foundUser['id']}`).then(response => {
                if(response.ok){
                    return response.json()
                }
            }).then(data => setEvents(data))
            let fetchInterval = setInterval(() => {
                fetch(`/api/get-events-by-id/${foundUser['id']}`).then(response => {
                    if(response.ok){
                        return response.json()
                    }
                }).then(data => setEvents(data))
            }, 30000);
            setFetchInterval(fetchInterval)
        }
    },[])

    if(Object.keys(user).length === 0){<p></p>
        return <p>Вы не авторизованы</p>
    }
    else{

        const columns = [
            {
            title: 'time',
            dataIndex: 'time',
            key: 'time',
            render: (text, record) => <Link to={'/my-events/'+record.key}>{text}</Link>,
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
        const dataSource = events ? events.map(function(event){
            return {'key': Number(event.id), 'time': `${event.start.slice(5, 11)} ${event.start.slice(17, 22)}-${event.end.slice(17, 22)}`, 'name': event.author_firstname, 'description': event.description, rowSpan: 6}
        }) : []
        return <Table dataSource={dataSource} columns={columns} />;
    }
}