import {useEffect, useState} from "react";
import jwt_Decode from "jwt-decode";

export default function G_login() {
  const [ user , setUser] = useState({});

  function handleCallbackResponse(response) {
    console.log("Encoded JWT ID token : " + response.credential);
    var userObject = jwt_Decode(response.credential);
    console.log(userObject);
    setUser(userObject);
    document.getElementById("signInDiv").hidden = true;
  }
  function handleSignOut(){
    setUser({});
    document.getElementById("signInDiv").hidden = false;
  }
  useEffect(() => {
  /*global google*/
    google.accounts.id.initialize({
      client_id : '138640372450-e85pkrmnflipgal3uf7rosjok6vc6fov.apps.googleusercontent.com',
      callback : handleCallbackResponse
    });

    google.accounts.id.renderButton(
        document.getElementById("signInDiv"),
        {theme:"outline",size:"large"}
    );

    google.accounts.id.prompt();
    },[]);
  
  return (
    
    <div className="Google">

      <div id = "signInDiv"></div>
      {
        Object.keys(user).length != 0 &&
        <button onClick = {(e) => handleSignOut(e)}>Sign Out</button>
      }

      { user &&
      <div>
        <img src={user.picture}></img>
        <h3>{user.name}</h3>
      </div>
      }
    </div>
    
  );
}
