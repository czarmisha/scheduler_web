import React from 'react';
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from 'react';
import { Button, DatePicker, Form, Input, Modal } from 'antd';

const { TextArea } = Input;

export const CreateEvent = () => {
    const [response, setResponse] = useState([])
    const [user, setUser] = useState({});
    const [isModalOpen, setIsModalOpen] = useState(false);
    const navigate = useNavigate()

    useEffect(()=>{
        const loggedInUser = localStorage.getItem("user");
        if (loggedInUser) {
            const foundUser = JSON.parse(loggedInUser);
            setUser(foundUser);
        }
    },[])
  
    const handleOk = () => {
      setIsModalOpen(false);
    };
  
    const handleCancel = () => {
      setIsModalOpen(false);
    };

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
            fetch('/api/create-event', requestOptions)
                .then(response => response.json())
                .then(function(data) {
                  setResponse(data);
                  if(data['error']===true) setIsModalOpen(true)
                });
        };
    if(response['success'] === true)navigate("/my-events")

    return <>
        <Modal title="Error" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
          <div className='ant-form-item-explain-error'>
              {response['error'] === true ? `${response['message']}` : ``}
          </div>
        </Modal>
        <Form name="create-event-form" {...formItemLayout} onFinish={onFinish}>
        <Form.Item name="start" label="Дата и время начала" {...config}>
            <DatePicker showTime format="YYYY-MM-DD HH:mm" />
        </Form.Item>
        <Form.Item name="end" label="Дата и время окончания" {...config}>
            <DatePicker showTime format="YYYY-MM-DD HH:mm" />
        </Form.Item>
        <Form.Item name="description" label="Описание" {...configTextarea}>
          <TextArea rows={4} />
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
    </>;
    }
}