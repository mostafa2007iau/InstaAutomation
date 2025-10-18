import React, { useState } from 'react';
import { instagramLogin } from '../services/api';

const InstagramLogin = ({ onLoginSuccess }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            await instagramLogin({ username, password });
            onLoginSuccess();
        } catch (err) {
            setError('خطا در اتصال به اینستاگرام. نام کاربری یا رمز عبور اشتباه است.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '5px', marginTop: '20px' }}>
            <h2>اتصال به اکانت اینستاگرام</h2>
            <p>برای شروع، لطفا با حساب اینستاگرام خود وارد شوید. اطلاعات شما ذخیره نخواهد شد.</p>
            <form onSubmit={handleSubmit}>
                <div>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="نام کاربری اینستاگرام"
                        required
                        style={{ padding: '10px', margin: '10px 0', width: '300px' }}
                    />
                </div>
                <div>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="رمز عبور اینستاگرام"
                        required
                        style={{ padding: '10px', margin: '10px 0', width: '300px' }}
                    />
                </div>
                <button type="submit" disabled={loading} style={{ padding: '10px 20px', cursor: 'pointer' }}>
                    {loading ? 'در حال اتصال...' : 'اتصال'}
                </button>
                {error && <p style={{ color: 'red' }}>{error}</p>}
            </form>
        </div>
    );
};

export default InstagramLogin;