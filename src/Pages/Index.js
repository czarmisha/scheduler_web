import React, {useState, useEffect} from "react";
import { Card } from "../Components/card";

export const Index = () => {

    const [tmp, setTmp] = useState([])

    useEffect(()=>{
        fetch('/events/today').then(response => {
            if(response.ok){
                return response.json()
            }
        }).then(data => setTmp(data))
    })

    return(
        <>
            <Card listOfEvents={tmp}/>
        </>
    )
}