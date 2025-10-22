import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import InstagramLogin from '../components/InstagramLogin';
import PostList from '../components/PostList';
import { getInstagramPosts, getInstagramAccounts, deleteInstagramAccount } from '../services/api';

const DashboardPage = () => {
    const [accounts, setAccounts] = useState([]);
    const [selectedAccount, setSelectedAccount] = useState(null);
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [showAddAccount, setShowAddAccount] = useState(false);
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        navigate('/login');
    };

    const fetchAccounts = async () => {
        try {
            const { data } = await getInstagramAccounts();
            setAccounts(data);
            if (data.length > 0) {
                setSelectedAccount(data[0].id);
                fetchPosts(data[0].id);
            }
        } catch (err) {
            console.error("Failed to fetch accounts", err);
        }
    };

    const fetchPosts = async (accountId) => {
        if (!accountId) return;
        setLoading(true);
        setError('');
        setPosts([]);
        try {
            const { data } = await getInstagramPosts(accountId);
            setPosts(data);
        } catch (err) {
            setError('خطا در دریافت پست‌ها.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteAccount = async (accountId) => {
        if (window.confirm('آیا از حذف این اکانت مطمئن هستید؟ تمام قوانین مربوط به آن نیز حذف خواهد شد.')) {
            try {
                await deleteInstagramAccount(accountId);
                fetchAccounts();
            } catch (err) {
                setError('خطا در حذف اکانت.');
            }
        }
    };

    useEffect(() => {
        fetchAccounts();
    }, []);

    useEffect(() => {
        fetchPosts(selectedAccount);
    }, [selectedAccount]);


    return (
        <div style={{ direction: 'rtl', fontFamily: 'sans-serif', padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h1>داشبورد مدیریت</h1>
                <button onClick={handleLogout} style={{ padding: '10px' }}>خروج از حساب</button>
            </div>

            <hr />

            <div style={{ background: '#eee', padding: '15px', borderRadius: '5px' }}>
                <h2>اکانت‌های اینستاگرام</h2>
                <select onChange={(e) => setSelectedAccount(e.target.value)} value={selectedAccount || ''}>
                    {accounts.map(acc => (
                        <option key={acc.id} value={acc.id}>{acc.username}</option>
                    ))}
                </select>
                {selectedAccount && (
                    <button onClick={() => handleDeleteAccount(selectedAccount)} style={{backgroundColor: 'red', marginLeft: '10px'}}>حذف اکانت فعلی</button>
                )}
                <button onClick={() => setShowAddAccount(!showAddAccount)}>{showAddAccount ? 'انصراف' : 'افزودن اکانت جدید'}</button>
                {showAddAccount && <InstagramLogin onLoginSuccess={() => {
                    setShowAddAccount(false);
                    fetchAccounts();
                }} />}
            </div>

            <div style={{marginTop: '20px'}}>
                <h3>پست‌های اکانت: {accounts.find(acc => acc.id === selectedAccount)?.username}</h3>
                {loading ? <p>در حال بارگذاری پست‌ها...</p> : <PostList posts={posts} />}
                {error && <p style={{ color: 'red' }}>{error}</p>}
            </div>
        </div>
    );
};

export default DashboardPage;