import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import InstagramLogin from '../components/InstagramLogin';
import PostList from '../components/PostList';
import { getInstagramPosts } from '../services/api';

const DashboardPage = () => {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [isInstagramLoggedIn, setIsInstagramLoggedIn] = useState(false); // This would ideally be checked from the backend
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        navigate('/login');
    };

    const fetchPosts = async () => {
        setLoading(true);
        setError('');
        try {
            const { data } = await getInstagramPosts();
            setPosts(data);
        } catch (err) {
            setError('خطا در دریافت پست‌ها. آیا به اکانت اینستاگرام خود متصل شده‌اید؟');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        // If we assume the user needs to fetch posts manually, we can call fetchPosts on a button click.
        // Or, if we want to fetch automatically, we need a way to know if the Instagram account is connected.
        // For now, let's provide a button to fetch posts.
    }, []);


    return (
        <div style={{ direction: 'rtl', fontFamily: 'sans-serif', padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h1>داشبورد مدیریت</h1>
                <button onClick={handleLogout} style={{ padding: '10px' }}>خروج از حساب</button>
            </div>

            <hr />

            {!isInstagramLoggedIn ? (
                <InstagramLogin onLoginSuccess={() => {
                    setIsInstagramLoggedIn(true);
                    fetchPosts();
                }} />
            ) : (
                <div>
                    <button onClick={fetchPosts} disabled={loading}>
                        {loading ? 'در حال بارگذاری...' : 'دریافت و به‌روزرسانی پست‌ها'}
                    </button>
                    {error && <p style={{ color: 'red' }}>{error}</p>}
                    <PostList posts={posts} />
                </div>
            )}
        </div>
    );
};

export default DashboardPage;