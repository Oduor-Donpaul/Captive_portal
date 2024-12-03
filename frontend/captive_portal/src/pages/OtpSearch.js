import React, { use, useState } from "react";

const OtpSearch = () => {
    const [phoneNumber, setPhoneNumber] = useState('');

    const handleInputChange = (e) => {
        setPhoneNumber(e.target.value)
    }



    return (
        <div style={{textAlign: 'center'}}>
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
    )
}

export default OtpSearch;