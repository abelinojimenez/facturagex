import logo from '../logo.svg';
import '../App.css';
import {useEffect } from 'react';
import {Routes,Route,Navigate} from "react-router-dom";
import Wizard from '../components/wizard';
import Cookies from 'universal-cookie';

import ReactGA from 'react-ga';
  const TRACKING_ID = "G-WWNR2R31EP"; // OUR_TRACKING_ID
  ReactGA.initialize(TRACKING_ID);


const App=()=> {  
  const cookies = new Cookies();
  useEffect(() => {
    ReactGA.pageview(window.location.pathname + window.location.search);
  }, []);  
  return (
      <Routes>
        <Route exact path="/" element={<Wizard/>} />
        <Route exact path="/postProduct" element={<Wizard/>} />

        <Route  path="/">
           <Route  path=":idFactura"  element={<Wizard action="initial" />}  />
        </Route>

        </Routes>
     );
    
}


export default App;
