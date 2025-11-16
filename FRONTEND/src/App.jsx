import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import api from './componets/api'

function App() {
  const [count, setCount] = useState(0)

  const fetchHolawe = async()=>{
    try{
      const response = await api.get('/hola');
      console.log(response.data.hola)
    }catch(error){
      console.error("error en la api al llamar a hola", error)
    }
  }


  return (
    <>
    <div>
      <h1>Hola putos</h1>
    </div>
    </>
  )
}

export default App
