import axios from "axios";
import React, { useState } from "react";
import { Button } from "react-bootstrap";

const GenerateOtp = () => {

    const [PhoneNumber, setPhoneNumber] = useState('');
    const [otp, setOtp] = useState('');
    const [loading, setLoading] = useState(false);

    const handleInputChange = (e) => {
        setPhoneNumber(e.target.value)
    };

    const getOtp = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/mpesa-callback', 
                {
                    PhoneNumber: PhoneNumber
                }
            );

            setLoading(true)

            const message = response.data.message
            alert(message)
        } catch (error) {
            console.error('Error getting otp:', error)
        } finally {
            setLoading(false)
        }
    }

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
                <Button onClick={getOtp}><b>{loading ? 'Generating...' : 'Generate'}</b></Button>
            </div>

        </div>
    )
};

export default GenerateOtp;