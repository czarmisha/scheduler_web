import TelegramLoginButton from "react-telegram-login";
import { useState, useEffect } from "react";


export default function Auth() {
  const [user, setUser] = useState();
  const [loginData, setLoginData] = useState({});
  const handleTelegramResponse = (response) => {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(response)
    };
    fetch('/api/login', requestOptions)
        .then(response => response.json())
        .then(data => setLoginData(data));
  };
  useEffect(() => {
    const loggedInUser = localStorage.getItem("user");
    if (loggedInUser) {
      // console.log(loggedInUser);
      const foundUser = JSON.parse(loggedInUser);
      setUser(foundUser);
    }
  }, []);
  useEffect(() => {
    if(loginData['success']){
      setUser(loginData.user);
      localStorage.setItem("user", JSON.stringify(loginData.user));
      window.location.reload()
    }
  }, [loginData]);

  const handleLogout = () => {
    setUser(null);
    setLoginData({})
    localStorage.removeItem("user");
    window.location.reload()
  };
  return (
    <div className="App">
      {user && (
        <div>
          <p>{user.first_name} is logged in</p>
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}
      {!user && (
        <TelegramLoginButton
          dataOnauth={handleTelegramResponse}
          botName="uzinfocom_scheduler_bot"
          language="en"
          buttonSize="medium"
          className="telegram-button"
        />
      )}
    </div>
  );
}
