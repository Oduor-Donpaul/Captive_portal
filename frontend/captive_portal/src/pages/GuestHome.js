import React, { useState } from "react";
import { Button } from "react-bootstrap";

const GuestHome = () => {

    const [PhoneNumber, setPhoneNumber] = useState('');
    const [otp, setOtp] = useState("");

    const handlePhoneNumberChange = (e) => {
        setPhoneNumber(e.target.value)
    }

    const handleOtpChange = (e) => {
        setOtp(e.target.value)
    }
    return (
        <div style={{textAlign: 'center', alignItems: 'center', justifyContent: 'center'}}>
            <div style={{textAlign: 'center'}}>
                <h1><b>Welcome to Techpoint</b></h1>
                <p>Your One Stop for all Things Tech.</p>
            </div>
            <div>
                <div style={{
                    border: '5px solid blue',
                    width: '40%',
                    padding: '40px',
                    margin: '0 auto'}}>
                    <h2><b>Sign in To Network</b></h2>
                    <label htmlFor="phone_number">
                        Enter <b>M-Pesa</b> Phone Number:
                    </label>
                    <input
                        name="phone_number"
                        type="tel"
                        value={PhoneNumber}
                        onChange={handlePhoneNumberChange}
                        placeholder="Example    254712345678"
                        style={{
                            marginBottom: '20px',
                            borderRadius: '5px'
                        }}
                    />
                    <br></br>
                    <label htmlFor="otp">
                        Enter a valid OTP:
                    </label>
                    <input 
                        name="otp"
                        type="otp"
                        value={otp}
                        onChange={handleOtpChange}
                        placeholder="OTP  123456"
                        style={{
                            marginBottom: '10px',
                            borderRadius: '5px'
                        }}
                    />
                    <br></br>
                    <Button>Sign In</Button>              
                </div>
            </div>
        </div>
    )
}

export default GuestHome;