import React, { useState } from 'react';
import RuleManager from './RuleManager';

const PostList = ({ posts }) => {
    const [selectedPost, setSelectedPost] = useState(null);

    if (!posts.length) {
        return <p>پستی برای نمایش وجود ندارد. لطفا دکمه دریافت پست‌ها را بزنید.</p>;
    }

    return (
        <div style={{ marginTop: '20px' }}>
            <h2>پست‌های شما</h2>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px' }}>
                {posts.map(post => (
                    <div key={post.pk} style={{ border: '1px solid #ddd', borderRadius: '5px', padding: '10px', width: '200px', textAlign: 'center' }}>
                        <img src={post.thumbnail_url} alt={post.caption_text.substring(0, 50)} style={{ width: '100%', height: 'auto' }} />
                        <p>{post.caption_text.substring(0, 50)}...</p>
                        <button onClick={() => setSelectedPost(post)}>مدیریت ربات</button>
                    </div>
                ))}
            </div>
            {selectedPost && (
                <div style={{
                    position: 'fixed', top: '0', left: '0', width: '100%', height: '100%',
                    backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex',
                    justifyContent: 'center', alignItems: 'center'
                }}>
                    <div style={{ background: 'white', padding: '20px', borderRadius: '5px', width: '80%', maxHeight: '90vh', overflowY: 'auto' }}>
                        <button onClick={() => setSelectedPost(null)} style={{ float: 'left' }}>بستن</button>
                        <RuleManager post={selectedPost} />
                    </div>
                </div>
            )}
        </div>
    );
};

export default PostList;