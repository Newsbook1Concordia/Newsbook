import {useEffect} from "react";
import jwt_Decode from "jwt-decode";




export default function GoogleLoginnew() {

  function handleCallbackResponse(response) {
    console.log("Encoded JWT ID token : " + response.credential);
    var userObject = jwt_Decode(response.credential);
    console.log(userObject);
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
    },[]);
  return (
    <div className="App">
      <div id = "signInDiv"></div>
    </div>
  );
}
