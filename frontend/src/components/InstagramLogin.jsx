import React, { useState } from 'react';
import { instagramLogin, instagramSessionLogin } from '../services/api';

const InstagramLogin = ({ onLoginSuccess }) => {
    const [loginMethod, setLoginMethod] = useState('credentials'); // 'credentials' or 'session'
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [sessionid, setSessionid] = useState('');
    const [csrftoken, setCsrftoken] = useState('');
    const [userId, setUserId] = useState('');
    const [proxy, setProxy] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            if (loginMethod === 'credentials') {
                await instagramLogin({ username, password, proxy });
            } else {
                await instagramSessionLogin({ sessionid, csrftoken, user_id: userId, proxy });
            }
            onLoginSuccess();
        } catch (err) {
            setError('خطا در اتصال به اینستاگرام. اطلاعات وارد شده را بررسی کنید.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const renderCredentialForm = () => (
        <form onSubmit={handleSubmit}>
            <p>برای شروع، لطفا با حساب اینستاگرام خود وارد شوید. اطلاعات شما ذخیره نخواهد شد.</p>
            <div>
                <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="نام کاربری اینستاگرام" required style={{ width: '300px' }} />
            </div>
            <div>
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="رمز عبور اینستاگرام" required style={{ width: '300px' }} />
            </div>
            <div>
                <input type="text" value={proxy} onChange={(e) => setProxy(e.target.value)} placeholder="پراکسی (اختیاری) e.g., http://user:pass@host:port" style={{ width: '300px' }} />
            </div>
            <button type="submit" disabled={loading}>{loading ? 'در حال اتصال...' : 'اتصال با رمز'}</button>
        </form>
    );

    const renderSessionForm = () => (
        <form onSubmit={handleSubmit}>
            <p>مقادیر زیر را از کوکی‌های مرورگر خود در سایت اینستاگرام کپی کنید.</p>
            <div>
                <input type="text" value={sessionid} onChange={(e) => setSessionid(e.target.value)} placeholder="sessionid" required style={{ width: '300px' }} />
            </div>
            <div>
                <input type="text" value={csrftoken} onChange={(e) => setCsrftoken(e.target.value)} placeholder="csrftoken" required style={{ width: '300px' }} />
            </div>
            <div>
                <input type="text" value={userId} onChange={(e) => setUserId(e.target.value)} placeholder="ds_user_id" required style={{ width: '300px' }} />
            </div>
            <div>
                <input type="text" value={proxy} onChange={(e) => setProxy(e.target.value)} placeholder="پراکسی (اختیاری) e.g., http://user:pass@host:port" style={{ width: '300px' }} />
            </div>
            <button type="submit" disabled={loading}>{loading ? 'در حال اتصال...' : 'اتصال با Session'}</button>
        </form>
    );

    return (
        <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '5px', marginTop: '20px' }}>
            <h2>اتصال به اکانت اینستاگرام</h2>
            <div>
                <button onClick={() => setLoginMethod('credentials')} disabled={loginMethod === 'credentials'}>ورود با رمز عبور</button>
                <button onClick={() => setLoginMethod('session')} disabled={loginMethod === 'session'}>ورود با Session</button>
            </div>
            <hr />
            {loginMethod === 'credentials' ? renderCredentialForm() : renderSessionForm()}
            {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
        </div>
    );
};

export default InstagramLogin;