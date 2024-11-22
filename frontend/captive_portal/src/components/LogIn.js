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
                <Button type="submit">Log In</Button>
            </div>
        </div>
    )
};

export default Log In;