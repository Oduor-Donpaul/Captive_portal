import React, { use, useState } from "react";
import axios from "axios";
import { Button } from "react-bootstrap";

const OtpSearch = () => {
    const [phoneNumber, setPhoneNumber] = useState('');
    const [loading, setLoading] = useState(false)
    const [message, setMessage] = useState('')
    const [otp, setOtp ] = useState('')

    const handleInputChange = (e) => {
        setPhoneNumber(e.target.value)
    }

    const SearchOtp = async () => {

        setLoading(true);
        setMessage('');

        try {
            
            const response = await axios.post('http://127.0.0.1:5000/admin/get-otp', {
                PhoneNumber: phoneNumber
            });
            
            const otpInstance = response.data.otp
            
            setLoading(false)
            setOtp(otp)
            setMessage(`Most recent OTP: ${otpInstance}`)
        } catch (error) {
            const errorMessage = error.response?.data?.message || 'Error retrieving otp'
            setMessage(errorMessage)
            setOtp('');
        } finally {
            setLoading(false)
        }
    }

    return (
        <div style={{textAlign: 'center'}}>
            <div>
                <div style={{marginTop:'15px', fontSize: '20px'}}>
                    <p><b>Enter phone number to Search for OTP</b></p>
                </div>
                <div>
                    <input 
                        name="phone_number"
                        type="tel"
                        value={phoneNumber}
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
            </div>
            <div>
                <Button onClick={SearchOtp}>Search OTP</Button>
            </div>
            {message && (
                <div>
                    {message}
                </div>
            )}
            {otp && (
                <div>
                    <p>The Most recent OTP: {otp}</p>
                </div>
            )}
        </div>
    )
}

export default OtpSearch;