import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, register } from '../services/api';

const LoginPage = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const { data } = isLogin
                ? await login({ username, password })
                : await register({ username, password });

            localStorage.setItem('accessToken', data.access);
            localStorage.setItem('refreshToken', data.refresh);
            navigate('/dashboard');
        } catch (err) {
            setError(isLogin ? 'نام کاربری یا رمز عبور اشتباه است.' : 'خطا در ثبت‌نام. لطفا دوباره تلاش کنید.');
            console.error(err);
        }
    };

    return (
        <div style={{ direction: 'rtl', textAlign: 'center', fontFamily: 'sans-serif', padding: '50px' }}>
            <h1>{isLogin ? 'ورود به سامانه' : 'ثبت‌نام در سامانه'}</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="نام کاربری"
                        required
                        style={{ padding: '10px', margin: '10px', width: '300px' }}
                    />
                </div>
                <div>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="رمز عبور"
                        required
                        style={{ padding: '10px', margin: '10px', width: '300px' }}
                    />
                </div>
                <button type="submit" style={{ padding: '10px 20px', cursor: 'pointer' }}>
                    {isLogin ? 'ورود' : 'ثبت‌نام'}
                </button>
                {error && <p style={{ color: 'red' }}>{error}</p>}
            </form>
            <button onClick={() => setIsLogin(!isLogin)} style={{ marginTop: '20px', background: 'none', border: 'none', color: 'blue', cursor: 'pointer' }}>
                {isLogin ? 'حساب کاربری ندارید؟ ثبت‌نام کنید' : 'قبلا ثبت‌نام کرده‌اید؟ وارد شوید'}
            </button>
        </div>
    );
};

export default LoginPage;