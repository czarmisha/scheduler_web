import React from 'react';
import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from 'react';
import { Button, DatePicker, Form, Input } from 'antd';
import moment from 'moment';

const { TextArea } = Input;

export const EditEvent = () => {
    var {id} = useParams()
    const [events, setEvents] = useState([])
    const [response, setResponse] = useState([])
    const [user, setUser] = useState({});
    const [initialData, setInitialData] = useState({});
    const navigate = useNavigate()

    useEffect(()=>{
      const loggedInUser = localStorage.getItem("user");
      if (loggedInUser) {
          const foundUser = JSON.parse(loggedInUser);
          setUser(foundUser);
          fetch(`/api/get-event-detail/${id}`).then(response => {
              if(response.ok){
                  return response.json()
              }
          }).then(function(data){
              setEvents(data)
              console.log('data', data);
              const start = new Date(data.start)
              const end = new Date(data.end)
              const startStr = `${start.getFullYear()}-${(start.getMonth()+1)<10 ? '0'+(start.getMonth()+1) : (start.getMonth()+1)}-${start.getDate()<10 ? '0'+start.getDate() : start.getDate()} ${data.start.slice(17, 19)}:${data.start.slice(20, 22)}`
              const endStr = `${end.getFullYear()}-${(end.getMonth()+1)<10 ? '0'+(end.getMonth()+1) : (end.getMonth()+1)}-${end.getDate()<10 ? '0'+end.getDate() : end.getDate()} ${data.end.slice(17, 19)}:${data.end.slice(20, 22)}`
              setInitialData({start: startStr, end: endStr})
            })
      }
    },[])

    if(Object.keys(user).length === 0){<p></p>
        return <p>Вы не авторизованы</p>
    }
    else{
        const formItemLayout = {
            labelCol: {
              xs: {
                span: 24,
              },
              sm: {
                span: 8,
              },
            },
            wrapperCol: {
              xs: {
                span: 24,
              },
              sm: {
                span: 16,
              },
            },
          };
          const config = {
            rules: [
              {
                type: 'object',
                required: true,
                message: 'Пожалуйста, введите дату и время',
              },
            ],
          };
          const configTextarea = {
            rules: [
              {
                type: 'string',
                required: true,
                message: 'Пожалуйста, введите описание',
              },
            ],
          };


        const onFinish = (fieldsValue) => {
            const values = {
                ...fieldsValue,
                'start': fieldsValue['start'].format('YYYY-MM-DD HH:mm'),
                'end': fieldsValue['end'].format('YYYY-MM-DD HH:mm'),
                'description': fieldsValue['description'],
                };
            console.log('Received values of form: ', values);
            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({...values, u_id: user.id, u_name: user.username, u_firstname: user.first_name})
            };
            fetch(`/api/edit-event/${id}`, requestOptions)
                .then(response => response.json())
                .then(data => setResponse(data));
        };
    console.log(response);
    if(response['success'] === true)navigate(`/my-events/${id}`);

    return <>{events.length !== 0 ?
        <>
          <div className='ant-form-item-explain-error'>
              {response['error'] === true ? `${response['message']}` : ``}
          </div>
          <Form name="create-event-form" {...formItemLayout} onFinish={onFinish} initialValues={{start: moment(initialData.start), end: moment(initialData.end), description: events.description}}>
          <Form.Item name="start" label="Дата и время начала" {...config}>
              <DatePicker showTime format="YYYY-MM-DD HH:mm" />
          </Form.Item>
          <Form.Item name="end" label="Дата и время окончания" {...config}>
              <DatePicker showTime format="YYYY-MM-DD HH:mm" />
          </Form.Item>
          <Form.Item name="description" label="Описание" {...configTextarea}>
            <TextArea rows={4} allowClear={true} />
          </Form.Item>
          <Form.Item
              wrapperCol={{
              xs: {
                  span: 24,
                  offset: 0,
              },
              sm: {
                  span: 16,
                  offset: 8,
              },
              }}
          >
              <Button type="primary" htmlType="submit">
              Submit
              </Button>
          </Form.Item>
          </Form>
        </> : <></>}
    </>;
    }
}