import React, {useState ,useEffect} from 'react';

import { Link,useParams,useNavigate } from 'react-router-dom';

import axios from 'axios'
import Cookies from 'universal-cookie';
var hostapi=process.env.REACT_APP_API_URL;

export default function Wizard(props){

const params= useParams()
const [idFactura,setIdfactura]=useState(params["idFactura"]);
const [name, setName] = useState("");
const [nit, setNit] = useState("");
const [fecha, setFecha] = useState("");
const [detalle, setDetalle] = useState([]);
const [total, setTotal] = useState(0); 


useEffect(async()=>{
        
        await axios({  
            method: 'GET',
            url:hostapi+'/facturaCompleta/'+idFactura,
            headers: {
              'Content-Type': 'application/json'
            },
          }).then(res=>{
            console.log(res.data.detalle);
            var cabeza=res.data.cabeza;
            var detalle=res.data.detalle;
            setName(cabeza.clientNombre);
            setFecha(cabeza.fecha);
            setNit(cabeza.nit);
            setDetalle(detalle);
            console.log(detalle.length)

          })
          
},[]);


function showDetalle(){
  var resultData=[]
  for(var i=0;i<detalle.length;i++){
    resultData.push(   
      <tr>
                        <td>{detalle[i].productoName}</td>
                        <td>{detalle[i].cantidad}</td>
                        <td>{detalle[i].precio}</td>
                        <td>{detalle[i].precio*detalle[i].cantidad}</td>
                    </tr>
      )
  }
  return resultData;
}


 
          return (
<>
<link href="wizard.css" rel="stylesheet"/>
<div class="row featurette center">
      <div class="container-fluid">
      <div class="container">
        <div class="mt-2 mb-2 text-center">
            <h2> Factura ejemplo Agexport</h2>
        </div>
        <ul class="step d-flex flex-nowrap">
     
    </ul> 
        
</div>
      </div>
      <div class={"profilecard  justify-content-around align-items-center visually-hidden-focusable"}>
       
        <form action="" method="post">
            
            <div class="form-group">
              <label>No:</label>
              <label>{idFactura}</label>
            </div>
            <div class="form-group">
                <label>Nit:</label>
                {nit}       
            </div>
            <div class="form-group">
                <label>Nombre:</label>
                {name}       
            </div>
            <div class="form-group">
                <label>Fecha:</label>
                {fecha}       
            </div>
            <div class="form-group">
                  <table>
                    <tr>
                        <td>Producto</td>
                        <td>Cantidad</td>
                        <td>Precio Total</td>
                    </tr>
                    {
                     showDetalle()
                    }
                
                    
                </table>  
            </div>
        </form>
      </div>  
     
      
    </div>
</>
            );
      } 
  