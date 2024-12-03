import { useEffect, useState } from "react";
import axios from 'axios';
import { Button } from "react-bootstrap";

const Admin = ({ token }) => {
    const [userRole, setUserRole] = useState(null);
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchAdminData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/admin', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                //set data and role from the response
                setData(response.data)
                setUserRole(response.data.role);

                
            } catch (error) {
                console.error('Access denied:',  error.response?.data?.message)
            }
        };

        fetchAdminData();
        
    }, [token]);

    const handleModification = async () => {
        try {
            await axios.post(
                'http://127.0.0.1:5000/admin/modify',
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert('Successful');
        } catch (error) {
            alert('You do not have permission to modify.')
        }
    };

    return (
        <div>
            <h1>Admin Dashboard</h1>
            {data && <p>Data: {data}</p>}
            {userRole === 'admin' && (
                <Button onClick={handleModification}> Modify data </Button>    
        )}
        {userRole === 'staff' && <p>You have read access only</p>}
        </div>
    )
};

export default Admin