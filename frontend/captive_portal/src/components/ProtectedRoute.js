import React from "react";
import { Navigate, useLocation } from "react-router-dom";

const ProtectedRoute = ({children}) => {
    const authToken = localStorage.getItem('authToken') 
    const location = useLocation()

    if(!authToken) {
        return <Navigate to='/admin/signin' state={{from: location}} replace/>;
    }

    return children;

}

export default ProtectedRoute;