import React, { useState, useEffect } from 'react';
import { getAutomationRules, createAutomationRule, updateAutomationRule, deleteAutomationRule } from '../services/api';
import TaskLogViewer from './TaskLogViewer';

const RuleManager = ({ post }) => {
    const [rules, setRules] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [editingRule, setEditingRule] = useState(null); // State for the rule being created or edited

    const fetchRules = async () => {
        setLoading(true);
        try {
            // The backend needs to know how to associate the post from the frontend (post.id)
            // with a MonitoredPost instance. Let's assume we need to create a MonitoredPost first
            // if it doesn't exist. This logic should be on the backend, but we'll need to send the post details.
            const { data } = await getAutomationRules(post.pk);
            setRules(data);
        } catch (err) {
            setError('خطا در دریافت قوانین.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRules();
    }, [post]);

    const handleSaveRule = async (e) => {
        e.preventDefault();
        const ruleData = {
            post_pk: post.pk,
            post_url: `https://www.instagram.com/p/${post.code}/`,
            keywords: editingRule.keywords,
            reply_text: editingRule.reply_text,
            reply_type: editingRule.reply_type,
            is_active: editingRule.is_active,
        };

        try {
            if (editingRule.id) { // Existing rule
                // The update operation in a standard ViewSet might not support custom logic like this easily.
                // We will assume for now the update will work with the standard serializer.
                // A better implementation might require a custom update method in the ViewSet.
                await updateAutomationRule(editingRule.id, ruleData);
            } else { // New rule
                await createAutomationRule(ruleData);
            }
            setEditingRule(null);
            fetchRules(); // Refresh the list
        } catch (err) {
            setError('خطا در ذخیره قانون.');
        }
    };

    const handleDeleteRule = async (ruleId) => {
        if (window.confirm('آیا از حذف این قانون مطمئن هستید؟')) {
            try {
                await deleteAutomationRule(ruleId);
                fetchRules();
            } catch (err) {
                setError('خطا در حذف قانون.');
            }
        }
    };

    const startNewRule = () => {
        setEditingRule({
            keywords: '',
            reply_text: '',
            reply_type: 'comment',
            is_active: true
        });
    };

    return (
        <div>
            <h3>مدیریت قوانین برای پست: "{post.caption_text.substring(0, 50)}..."</h3>
            <button onClick={startNewRule}>ایجاد قانون جدید</button>
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {editingRule && (
                <form onSubmit={handleSaveRule} style={{ border: '1px solid #eee', padding: '15px', margin: '15px 0', borderRadius: '5px' }}>
                    <h4>{editingRule.id ? 'ویرایش قانون' : 'قانون جدید'}</h4>
                    <label>کلمات کلیدی (با کاما جدا کنید):</label>
                    <input type="text" value={editingRule.keywords} onChange={(e) => setEditingRule({...editingRule, keywords: e.target.value})} required style={{width: '90%', padding: '8px', margin: '5px 0'}} />

                    <label>متن پاسخ:</label>
                    <textarea value={editingRule.reply_text} onChange={(e) => setEditingRule({...editingRule, reply_text: e.target.value})} required style={{width: '90%', padding: '8px', margin: '5px 0', height: '80px'}} />

                    <label>نوع پاسخ:</label>
                    <select value={editingRule.reply_type} onChange={(e) => setEditingRule({...editingRule, reply_type: e.target.value})} style={{padding: '8px', margin: '5px 0'}}>
                        <option value="comment">کامنت</option>
                        <option value="direct">دایرکت (پیام خصوصی)</option>
                    </select>

                    <label>
                        <input type="checkbox" checked={editingRule.is_active} onChange={(e) => setEditingRule({...editingRule, is_active: e.target.checked})} />
                        فعال
                    </label>

                    <div style={{marginTop: '10px'}}>
                        <button type="submit">ذخیره</button>
                        <button type="button" onClick={() => setEditingRule(null)}>انصراف</button>
                    </div>
                </form>
            )}

            <h4>قوانین موجود</h4>
            {loading ? <p>در حال بارگذاری...</p> : (
                rules.length > 0 ? rules.map(rule => (
                    <div key={rule.id} style={{ border: '1px solid #ddd', padding: '10px', marginBottom: '10px' }}>
                        <p><strong>کلمات کلیدی:</strong> {rule.keywords}</p>
                        <p><strong>پاسخ:</strong> {rule.reply_text}</p>
                        <p><strong>نوع:</strong> {rule.reply_type === 'comment' ? 'کامنت' : 'دایرکت'}</p>
                        <p><strong>وضعیت:</strong> {rule.is_active ? 'فعال' : 'متوقف'}</p>
                        <button onClick={() => setEditingRule(rule)}>ویرایش</button>
                        <button onClick={() => handleDeleteRule(rule.id)}>حذف</button>
                        <TaskLogViewer ruleId={rule.id} />
                    </div>
                )) : <p>هیچ قانونی برای این پست تعریف نشده است.</p>
            )}
        </div>
    );
};

export default RuleManager;