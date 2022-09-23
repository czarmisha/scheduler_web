import { BrowserRouter, Routes, Route } from "react-router-dom";
import {Base} from "./Layouts/Base";
import {CalendarView} from "./Pages/Calendar";
import {MyEvents} from "./Pages/MyEvents";
import {EventList} from "./Pages/EventList";
import { EventDetail } from "./Pages/EventDetail";
import { CreateEvent } from "./Pages/CreateEvent";
import { EditEvent } from "./Pages/EditEvent";
// import NoPage from "./pages/NoPage";
import 'antd/dist/antd.css'
import './index.css'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Base />}>
          <Route index element={<CalendarView />} />
          <Route path="my-events/" element={<MyEvents />} />
          <Route path="my-events/:id" element={<EventDetail />} />
          <Route path="event-list/today/" element={<EventList period='today'/>} />
          <Route path="event-list/tomorrow/" element={<EventList period='tomorrow'/>} />
          <Route path="create-event/" element={<CreateEvent />} />
          <Route path="edit-event/:id" element={<EditEvent />} />
          {/* <Route path="event-list/thisweek/" element={<EventList period='thisweek'/>} /> */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

