import { useParams, useNavigate } from "react-router-dom";
import { Table, Button, Modal  } from 'antd';
import React from 'react';
import { useEffect, useState } from 'react';

export const EventDetail = ()=>{
    var {id} = useParams()

    const [events, setEvents] = useState([])
    const [interval, setFetchInterval] = useState()
    const [user, setUser] = useState({});
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [response, setResponse] = useState();
    const navigate = useNavigate()

    const showModal = () => {
        setIsModalOpen(true);
    };

    const handleOk = () => {
        setIsModalOpen(false);
        fetch(`/api/delete-event/${id}`).then(response => {
            if(response.ok){
                return response.json()
            }
        }).then(function (data){
                setResponse(data);
                console.log(data);
                if(data['success'] === true)navigate("/my-events");
            })
    };

    const handleCancel = () => {
        setIsModalOpen(false);
    };

    const editEvent = () => {
        navigate(`/edit-event/${id}`)
    }

    useEffect(()=>{
        clearInterval(interval)

        const loggedInUser = localStorage.getItem("user");
        if (loggedInUser) {
            const foundUser = JSON.parse(loggedInUser);
            setUser(foundUser);
            fetch(`/api/get-event-detail/${id}`).then(response => {
                if(response.ok){
                    return response.json()
                }
            }).then(data => setEvents(data))
            let fetchInterval = setInterval(() => {
                fetch(`/api/get-event-detail/${id}`).then(response => {
                    if(response.ok){
                        return response.json()
                    }
                }).then(data => setEvents(data))
            }, 30000);
            setFetchInterval(fetchInterval)
        }
    },[])

    if(Object.keys(user).length == 0){
        return <p>Вы не авторизованы</p>
    }
    else{
        const columns = [
            {
            title: 'date',
            dataIndex: 'date',
            key: 'date',
            },
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
        const dataSource = events.length !== 0 ? [{'key': Number(events.id), 'date': `${events.start.slice(0, 16)}`, 'time': `${events.start.slice(17, 22)}-${events.end.slice(17, 22)}`, 'name': events.author_firstname, 'description': events.description, rowSpan: 6}] : []
        const modalTitle = events.length !== 0 ? `Удалить ${events.start.slice(0, 22) + '-' + events.end.slice(17, 22) + ' ' + events.description}` : 'Удаление события'
        return <>
                <Table dataSource={dataSource} columns={columns} pagination={false} />
                <Button className="my_btn" type="primary" onClick={showModal}>
                    Delete
                </Button>
                <Button className="my_btn" type="primary" onClick={editEvent}>
                    Edit
                </Button>
                <Modal title={modalTitle} open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
                    <p>Вы уверены?</p>
                </Modal>
            </>
    }
}