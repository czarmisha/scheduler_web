import { Outlet, Link } from "react-router-dom";
import {
  AppstoreOutlined,
  AppstoreAddOutlined,
  UnorderedListOutlined,
  CalendarOutlined,
  FieldNumberOutlined,
} from '@ant-design/icons';
import { Layout, Menu } from 'antd';
import React from 'react';
import Auth from "../Components/Authorization";
const { Content, Footer, Sider } = Layout;
const menuItems = [
  {key: 1, icon: React.createElement(CalendarOutlined), label: <Link to="/">Календарь</Link>},
  {key: 2, icon: React.createElement(UnorderedListOutlined), label: 'Список событий', children: [
    {key: 2.1, icon: React.createElement(FieldNumberOutlined), label: <Link to="event-list/today/">На сегодня</Link>},
    {key: 2.2, icon: React.createElement(FieldNumberOutlined), label: <Link to="event-list/tomorrow/">На завтра</Link>},
    // {key: 2.3, icon: React.createElement(FieldNumberOutlined), label: <Link to="event-list/thisweek/">На неделю</Link>},
  ]},
  {key: 3, icon: React.createElement(AppstoreAddOutlined), label: <Link to="/my-events">Мои события</Link>},
  {key: 4, icon: React.createElement(AppstoreOutlined), label: <Link to="/create-event">Создать событие</Link>},
]

export const Base = () => {
  return (<Layout hasSider>
      <Sider
        style={{
          overflow: 'auto',
          height: '100vh',
          position: 'fixed',
          left: 0,
          top: 0,
          bottom: 0,
        }}
      >
        <div className="logo" />
        <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']} items={menuItems} />
        <Auth/>
      </Sider>
      <Layout
        className="site-layout"
        style={{
          marginLeft: 200,
        }}
      >
        <Content
          style={{
            margin: '24px 16px 0',
            overflow: 'initial',
          }}
        >
          <Outlet/>
        </Content>
        <Footer
          style={{
            textAlign: 'center',
          }}
        >
          Ant Design ©2018 Created by Ant UED
        </Footer>
      </Layout>
    </Layout>
)}


