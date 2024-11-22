import React, { useState } from "react";
import { Button } from "react-bootstrap";

const GenerateOtp = () => {

    const [PhoneNumber, setPhoneNumber] = useState('');
    const [otp, setOtp] = useState('');

    const handleInputChange = (e) => {
        setPhoneNumber(e.target.value)
    };

    return (
        <div style={{textAlign: "center", marginTop: '10px'}}>
            <div>
                <p><b>Enter phone number to generate OTP</b></p>
                <input
                    name="phone_number"
                    type="tel"
                    value={PhoneNumber}
                    onChange={handleInputChange}
                    placeholder='Enter phone number in the format "254712345678"'
                    style={{
                        padding: '10px',
                        width: '80%',
                        border: '1px solid #ccc',
                        borderRadius: '5px',
                        fontSize: '16px'
                    }}
                />
                
            </div>
            <div style={{margin: '20px'}}>
                <Button type="submit"><b>Generate</b></Button>
            </div>
            <div>
                <p>Dear {PhoneNumber} enter {otp} as your OTP. Please Do not share it with anyone.<br></br> Techpoint</p>
            </div>
        </div>
    )
};

export default GenerateOtp;