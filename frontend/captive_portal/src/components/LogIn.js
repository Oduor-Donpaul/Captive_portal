import React, { useState } from "react";
import { Button } from "react-bootstrap";


const LogIn = () => {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleEmailChange = (e) => {
        setEmail(e.target.value)
    }

    const handlePasswordChange = (e) => {
        setPassword(e.target.value)
    }
    //console.log(JSON.stringify({ email, password }))

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://127.0.0.1:5000/admin/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: "test@example.com",
                    password: "password123"
                })
            })
            console.log('response:', response)

            if (!response.ok) {
                const error = await response.json();
                alert(error.message || 'Login failed');
                return;
            }

            const data = await response.json();
            //store token in Local storage
            localStorage.setItem('token', data.access_token);
            alert('Login successful')
            console.log('data:', data)
        } catch (error) {
            alert('Network error or server is unavailable')
            console.error(error)
        }
    }

    return (
        <div style={{textAlign: 'center'}}>
            <div style={{textAlign: 'center'}}>
                <h1><b>Welcome to Techpoint</b></h1>
                <p>Your One Stop for all Things Tech</p>
            </div>
            <div>
                <h2 style={{fontSize: '25px'}}><b>Log In</b></h2>
            </div>
            <div>
                <label htmlFor="email">
                    Email:
                </label>
                <br></br>
                <input 
                    name="email"
                    type="email"
                    value={email}
                    onChange={handleEmailChange}
                    placeholder="Enter Email"
                    style={{
                        marginTop: '5px',
                        marginBottom: '20px'
                    }}
                />
                <br></br>
                <label htmlFor="password">
                    Enter your Password:
                </label>
                <br></br>
                <input 
                    name="password"
                    type="password"
                    value={password}
                    onChange={handlePasswordChange}
                    placeholder="password"
                    style={{
                        marginTop: '5px',
                        marginBottom: '5px'
                    }}
                />
                <br></br>
                <Button type="submit" onClick={handleSubmit}>Log In</Button>
            </div>


        </div>
    )
};

export default LogIn;